from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator

RATING_VALIDATOR = [MinValueValidator(0), MaxValueValidator(5)]


class Staff(models.Model):
    POSITION_CHOICES = (
        (1, 'LIBRARIAN'),
        (2, 'ADMINISTRATOR')
    )

    user = models.OneToOneField(User, related_name='staff', on_delete=models.CASCADE)
    position = models.IntegerField(default=1, choices=POSITION_CHOICES)
    avatar = models.ImageField(upload_to='avatar', null=True, blank=True)
    date_added = models.DateTimeField(auto_created=True, default=timezone.now)

    @property
    def full_name(self):
        return f'{self.user.get_full_name()}'


class Member(models.Model):
    user = models.OneToOneField(User, related_name='member', on_delete=models.CASCADE)
    address = models.CharField(max_length=100, null=True)
    avatar = models.ImageField(upload_to='avatar', null=True, blank=True)
    date_added = models.DateTimeField(auto_created=True, default=timezone.now)

    def __str__(self):
        return self.user.get_full_name()


class Category(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Author(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    summary = models.CharField(max_length=150)
    pic = models.ImageField(upload_to='authors/', null=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class Book(models.Model):
    name = models.CharField(max_length=50)
    isbn = models.CharField(max_length=50, null=True, blank=True)
    author = models.ForeignKey(Author, related_name='books', on_delete=models.CASCADE)
    category = models.ForeignKey(Category, related_name='books', on_delete=models.CASCADE)
    summary = models.TextField(max_length=500)
    cover_page = models.ImageField(upload_to='covers/')
    date_published = models.DateField(default=timezone.now)
    barcode = models.CharField(max_length=50, null=True)
    quantity = models.IntegerField(default=0)
    fine = models.DecimalField(default=0.0, max_digits=65, decimal_places=2)

    def __str__(self):
        return f'{self.name}@{self.isbn}'


class Review(models.Model):
    comment = models.CharField(max_length=245)
    by = models.ForeignKey(Member, related_name='reviews', on_delete=models.CASCADE)
    book = models.ForeignKey(Book, related_name='reviews', on_delete=models.CASCADE)
    rating = models.DecimalField(max_digits=10, decimal_places=1, validators=RATING_VALIDATOR)
    date_reviewed = models.DateTimeField(auto_created=True, default=timezone.now)


class BookIssue(models.Model):
    book = models.ForeignKey(Book, related_name='issues', on_delete=models.CASCADE)
    member = models.ForeignKey(Member, related_name='issues', on_delete=models.CASCADE)
    issue_date = models.DateField(auto_created=True, default=timezone.now)
    due_date = models.DateField(auto_created=True, default=timezone.now)
    return_date = models.DateField(null=True, blank=True)

    @property
    def returned(self):
        # if the return date is set, the book was returned
        return self.return_date is not None

    @property
    def status_int(self):
        if self.returned:
            # returned
            return 1
        elif self.due_date >= timezone.now().date():
            # days left
            return 2
        else:
            # overdue
            return 3

    @property
    def fine(self):
        if self.returned:
            # if returned, check if returned while overdue or not
            if self.due_date >= self.return_date:
                # member returned it on time
                return '--', 0
            else:
                # member returned it late, charge them
                _hours_left = (self.return_date - self.due_date)
                days, _ = divmod(_hours_left.total_seconds(), 86400)
                _fine = float(days) * float(self.book.fine)
                return f"E {_fine:,.2f}", _fine
        else:
            # else not returned, check if overdue or not

            if self.due_date >= timezone.now().date():
                # not overdue yet
                return '--', 0
            else:
                _hours_left = (timezone.now().date() - self.due_date)
                days, _ = divmod(_hours_left.total_seconds(), 86400)
                _fine = float(days) * float(self.book.fine)
                return f"E {_fine:,.2f}", _fine

    @property
    def status(self):
        if self.return_date:
            if self.due_date >= self.return_date:
                return f'RETURNED {self.return_date.strftime("%m/%d")}'
            else:
                return f'RETURNED LATE{self.return_date.strftime("%m/%d")}'

        try:
            # calculate the number of hours left to due date
            if self.due_date >= timezone.now().date():
                _hours_left = (self.due_date - timezone.now().date())
                days, _ = divmod(_hours_left.total_seconds(), 86400)
                return "{}days LEFT".format(int(days))

            else:
                _hours_left = (timezone.now().date() - self.due_date)
                days, _ = divmod(_hours_left.total_seconds(), 86400)
                return "DUE BY {}days".format(int(days))

        except Exception as error:
            print('FAILED TO CALCULATE DAYS LEFT: ', error)

        return "---"


class Income(models.Model):
    name = models.CharField(max_length=50, blank=False, null=False)
    issue = models.OneToOneField(BookIssue, related_name='receipt', on_delete=models.CASCADE, default=7)
    money = models.DecimalField(max_digits=65, decimal_places=2, blank=False, null=False, default=0)
    date_recorded = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f'{self.name}@{self.money}'

    @property
    def paid(self):
        return f'E {self.money:,.2f}'


class Expense(models.Model):
    name = models.CharField(max_length=50, blank=False, null=False)
    money = models.DecimalField(max_digits=65, decimal_places=2, blank=False, null=False)
    date_recorded = models.DateTimeField(auto_created=True, default=timezone.now)

    def __str__(self) -> str:
        return f'{self.name}@{self.money}'


@receiver(post_delete, sender=Staff)
def post_delete_staff_user(sender, instance, *args, **kwargs):
    try:
        # just in case user is not specified
        if hasattr(instance, 'user') and instance.user:
            instance.user.delete()
    except Exception as e:
        print('post_delete_staff_user_error: ', e)
        pass


@receiver(post_delete, sender=Member)
def post_delete_member_user(sender, instance, *args, **kwargs):
    try:
        # just in case user is not specified
        if hasattr(instance, 'user') and instance.user:
            instance.user.delete()
    except Exception as e:
        print('post_delete_member_user_error: ', e)
        pass
