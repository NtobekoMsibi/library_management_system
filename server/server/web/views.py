import copy

from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Count
from django.db.models.functions import TruncMonth
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.hashers import check_password
from django.views.generic import CreateView
from django.core.paginator import Paginator
from django.contrib.auth.views import LoginView, PasswordResetView, PasswordChangeView, PasswordResetConfirmView

from api.serializers import IncomeSerializer, IncomeDashboardSerializer
from library.forms import SigninForm, UserSetPasswordForm, UserPasswordResetForm, UserPasswordChangeForm, \
    ProfileForm, SignupFormUser, SignupFormMember, BookForm, AuthorForm, CategoryForm, UpdateUserForm, BookIssueForm, \
    SignupFormStaff
from library.models import BookIssue, Member, Book, Staff, Author, Category, Income


@login_required(login_url='/login/')
def dashboard(request):
    books = Book.objects.order_by('-id').all()[:10]
    members = Member.objects.order_by('-id').all()[:10]
    issues = BookIssue.objects.order_by('-id').all()[:10]

    total_books = Book.objects.count()
    total_members = Member.objects.count()

    incomes = Income.objects.annotate(
        month=TruncMonth('date_recorded')  # Truncate to month and add to select list
    ).values(
        'month'  # Group By month
    ).annotate(
        # c=Count('id'),  # Select the count of the grouping
        total=Sum('money')
    ).values('month', 'total')
    total_income = Income.objects.aggregate(Sum('money')).get('money__sum', 0)

    _plot_data = IncomeDashboardSerializer(incomes, many=True).data
    x_data = [i.get('month') for i in _plot_data]
    y_data = [i.get('total') for i in _plot_data]

    return render(request, 'dashboard/index.html', {
        'books': books,
        'members': members,
        'issues': issues,

        'total_books': total_books,
        'total_members': total_members,
        'total_income': f'E {total_income:,.2f}',

        'x_data': x_data,
        'y_data': y_data
    })


class SignInView(LoginView):
    form_class = SigninForm
    template_name = "authentication/sign-in.html"


class SignUpView(CreateView):
    form_class = SignupFormUser
    template_name = "authentication/sign-up.html"
    success_url = "login/"


def logout_view(request):
    logout(request)
    return redirect(reverse('web:login'))


class UserPasswordChangeView(PasswordChangeView):
    template_name = 'authentication/password-change.html'
    form_class = UserPasswordChangeForm


class UserPasswordResetView(PasswordResetView):
    template_name = 'authentication/forgot-password.html'
    form_class = UserPasswordResetForm


class UserPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'authentication/reset-password.html'
    form_class = UserSetPasswordForm


# --------------------- PROFILE URLS -------------------------------

@login_required(login_url='/login/')
def profile(request):
    _profile = get_object_or_404(Staff, user=request.user)
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=_profile)

        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully')
    else:
        form = ProfileForm(instance=_profile)

    context = {
        'form': form,
        'segment': _profile,
    }
    return render(request, 'dashboard/profile.html', context)


def upload_avatar(request):
    _profile = get_object_or_404(Staff, user=request.user)
    if request.method == 'POST':
        _profile.avatar = request.FILES.get('avatar')
        _profile.save()
        messages.success(request, 'Avatar uploaded successfully')
    return redirect(request.META.get('HTTP_REFERER'))


def change_password(request):
    user = request.user
    if request.method == 'POST':
        if check_password(request.POST.get('current_password'), user.password):
            user.set_password(request.POST.get('new_password'))
            user.save()
            messages.success(request, 'Password changed successfully')
        else:
            messages.error(request, "Password doesn't match!")
    return redirect(request.META.get('HTTP_REFERER'))


# --------------------------------- MEMBERS MANAGEMENT --------------------------------

@login_required(login_url='/login/')
def library_members_list(request):
    user_form = SignupFormUser()
    member_form = SignupFormMember()

    if request.method == 'POST':
        user_form = SignupFormUser(request.POST)
        member_form = SignupFormMember(request.POST)

        if user_form.is_valid() and member_form.is_valid():
            user = user_form.save()
            member = member_form.save(commit=False)
            member.user = user
            member.save()

            user_form = SignupFormUser()
            member_form = SignupFormMember()

    members_list = Member.objects.order_by('-id').all()
    page = request.GET.get('page', 1)
    paginator = Paginator(members_list, 25)
    members = paginator.page(page)

    # m_forms = []
    # u_forms = []
    # for _member in members:
    #     m_forms.append(SignupFormMember(instance=_member))
    #     u_forms.append(SignupFormUser(instance=_member.user))

    return render(request, 'pages/library-members.html', {
        'members': members,
        'form': user_form,
        'member_form': member_form,
    })


@login_required(login_url='/login/')
def delete_member(request, pk):
    try:
        member = Member.objects.get(id=pk)
        member.delete()
    except Exception as error:
        print('Failed to delete member: ', str(error))

    return redirect(request.META.get('HTTP_REFERER'))


@login_required(login_url='/login/')
def update_member(request, pk):
    try:
        member = get_object_or_404(Member, id=pk)
        user = member.user
        if request.method == 'POST':
            form = UpdateUserForm(request.POST, instance=user)
            if form.is_valid():
                form.save()
    except Exception as error:
        print('Failed to update library member: ', str(error))

    return redirect(request.META.get('HTTP_REFERER'))


@login_required(login_url='/login/')
def member_change_password(request, pk):
    member = Member.objects.get(id=pk)
    if request.method == 'POST':
        member.user.set_password(request.POST.get('password'))
        member.user.save()
    return redirect(request.META.get('HTTP_REFERER'))


# --------------------------------- AUTHOR MANAGEMENT --------------------------------

@login_required(login_url='/login/')
def books_authors(request):
    form = AuthorForm()
    if request.method == 'POST':
        form = AuthorForm(request.POST)

        if form.is_valid():
            form.save()
            form = AuthorForm()

    authors_list = Author.objects.order_by('-id').all()
    page = request.GET.get('page', 1)
    paginator = Paginator(authors_list, 25)
    authors = paginator.page(page)

    return render(request, 'pages/books-authors.html', {
        'authors': authors,
        'form': form
    })


@login_required(login_url='/login/')
def delete_author(request, pk):
    try:
        author = Author.objects.get(id=pk)
        author.delete()
    except Exception as error:
        print('Failed to delete author: ', str(error))
    return redirect(request.META.get('HTTP_REFERER'))


@login_required(login_url='/login/')
def update_author(request, pk):
    try:
        author = get_object_or_404(Author, id=pk)
        if request.method == 'POST':
            form = AuthorForm(request.POST, instance=author)
            if form.is_valid():
                form.save()
    except Exception as error:
        print('Failed to update author: ', str(error))

    return redirect(request.META.get('HTTP_REFERER'))


# -------------------------------- BOOKS CATEGORIES ---------------------------------

def books_categories(request):
    form = CategoryForm()
    if request.method == 'POST':
        form = CategoryForm(request.POST)

        if form.is_valid():
            form.save()
            form = CategoryForm()

    categories_list = Category.objects.order_by('-id').all()
    page = request.GET.get('page', 1)
    paginator = Paginator(categories_list, 25)
    categories = paginator.page(page)

    return render(request, 'pages/books-categories.html', {
        'categories': categories,
        'form': form
    })


@login_required(login_url='/login/')
def delete_category(request, pk):
    try:
        category = Category.objects.get(id=pk)
        category.delete()
    except Exception as error:
        print('Failed to delete category: ', str(error))
    return redirect(request.META.get('HTTP_REFERER'))


@login_required(login_url='/login/')
def update_category(request, pk):
    try:
        category = get_object_or_404(Category, id=pk)
        if request.method == 'POST':
            form = CategoryForm(request.POST, instance=category)
            if form.is_valid():
                form.save()
    except Exception as error:
        print('Failed to update category: ', str(error))

    return redirect(request.META.get('HTTP_REFERER'))


# --------------------------------- BOOKS MANAGEMENT --------------------------------

def books_list(request):
    form = BookForm()
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            form = BookForm()

    book_list = Book.objects.order_by('-id').all()
    page = request.GET.get('page', 1)
    paginator = Paginator(book_list, 25)
    books = paginator.page(page)

    forms = []
    for _book in books:
        forms.append(BookForm(instance=_book))

    return render(request, 'pages/library-books.html', {
        'books': books,
        'form': form,
        'forms': forms
    })


@login_required(login_url='/login/')
def delete_book(request, pk):
    try:
        book = Book.objects.get(id=pk)
        book.delete()
    except Exception as error:
        print('Failed to delete book: ', str(error))
    return redirect(request.META.get('HTTP_REFERER'))


@login_required(login_url='/login/')
def update_book(request, pk):
    try:
        book = get_object_or_404(Book, id=pk)
        if request.method == 'POST':
            form = BookForm(request.POST, instance=book)
            if form.is_valid():
                form.save()
    except Exception as error:
        print('Failed to update book: ', str(error))

    return redirect(request.META.get('HTTP_REFERER'))


# --------------------------------- BOOKS ISSUES MANAGEMENT --------------------------------

@login_required(login_url='/login/')
def books_issues_list(request):
    form = BookIssueForm()
    if request.method == 'POST':
        form = BookIssueForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            form = BookIssueForm()

    book_issues = BookIssue.objects.order_by('-id').all()
    page = request.GET.get('page', 1)
    paginator = Paginator(book_issues, 25)
    issues = paginator.page(page)

    forms = []
    for _book in issues:
        forms.append(BookIssueForm(instance=_book))

    return render(request, 'pages/book-issues.html', {
        'issues': issues,
        'form': form,
        'forms': forms
    })


@login_required(login_url='/login/')
def delete_book_issue(request, pk):
    try:
        issue = BookIssue.objects.get(id=pk)
        issue.delete()
    except Exception as error:
        print('Failed to delete book issue: ', str(error))
    return redirect(request.META.get('HTTP_REFERER'))


@login_required(login_url='/login/')
def update_book_issue(request, pk):
    try:
        issue = get_object_or_404(BookIssue, id=pk)
        if request.method == 'POST':
            form = BookIssueForm(request.POST, instance=issue)

            if form.is_valid():
                _data = form.cleaned_data
                form.save()

                # print('date', _data.get('return_date', ''), issue.status_int)

                if _data.get('return_date', ''):
                    # print('return date available: ', _data.get('return_date', ''))
                    # if we have return_data, check if this was overdue, then add income
                    if issue.fine[1]:
                        # print('user must pay', issue.fine[1])
                        # if the issue is overdue, calculate fine and add income, assume member has already paid
                        receipt, _ = Income.objects.get_or_create(issue=issue)
                        # print('creating receipt: ', receipt, _)
                        if receipt:
                            # print('created')
                            # update it
                            receipt.name = f"FINE FROM: {issue.member.user.username}"
                            receipt.money = issue.fine[1]
                            receipt.save()
                    else:
                        # print('user returns on time, check if there was a previous entry')
                        # if the fine is 0, check if we previously added a fee,
                        # if we did, remove that fee, since we are updating to an acceptable return date
                        # highly unlikely, but add this branch statement
                        receipt = Income.objects.filter(issue=issue)
                        if receipt.exists():
                            # print('previous entry existed, deleting it')
                            receipt.delete()
                        # else:
                        #     print('were good exiting')

    except Exception as error:
        print('Failed to update book issue: ', str(error))

    return redirect(request.META.get('HTTP_REFERER'))


# --------------------------------- LIBRARY STAFF USERS MANAGEMENT --------------------------------


@login_required(login_url='/login/')
def staff_members_list(request):
    user_form = SignupFormUser()
    staff_form = SignupFormStaff()

    if request.method == 'POST':
        user_form = SignupFormUser(request.POST)
        staff_form = SignupFormStaff(request.POST)

        if user_form.is_valid() and staff_form.is_valid():
            user = user_form.save()
            staff = staff_form.save(commit=False)
            staff.user = user
            staff.save()

            user_form = SignupFormUser()
            staff_form = SignupFormStaff()
        print('errors', user_form.errors, staff_form.errors)

    staff_list = Staff.objects.order_by('-id').all()
    page = request.GET.get('page', 1)
    paginator = Paginator(staff_list, 25)
    staff = paginator.page(page)

    return render(request, 'pages/staff-members.html', {
        'staff': staff,
        'form': user_form,
        'staff_form': staff_form
    })


@login_required(login_url='/login/')
def delete_staff_member(request, pk):
    try:
        staff = Staff.objects.get(id=pk)
        staff.delete()
    except Exception as error:
        print('Failed to delete staff member: ', str(error))

    return redirect(request.META.get('HTTP_REFERER'))


# --------------------------------- FINANCIALS MANAGEMENT --------------------------------


def financials(request):
    receipts_list = Income.objects.order_by('-id').all()
    page = request.GET.get('page', 1)
    paginator = Paginator(receipts_list, 30)
    receipts = paginator.page(page)

    total_received = Income.objects.aggregate(Sum('money'))

    return render(request, 'pages/book-finances.html', {
        'receipts': receipts,
        'total': f"E {total_received.get('money__sum', 0):,.2f}"
    })
