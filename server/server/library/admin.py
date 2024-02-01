from django.contrib import admin
from library.models import Staff, Member, Category, Author, Book, Review, BookIssue, Income, Expense


@admin.register(Staff)
class StaffAdminView(admin.ModelAdmin):
    list_display = ['user', 'position', 'date_added']
    list_per_page = 25


@admin.register(Member)
class MemberAdminView(admin.ModelAdmin):
    list_display = ['user', 'address', 'date_added']


@admin.register(Category)
class CategoryAdminView(admin.ModelAdmin):
    list_display = ['name', 'description']


@admin.register(Author)
class AuthorAdminView(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'summary']


@admin.register(Book)
class BookAdminView(admin.ModelAdmin):
    list_display = ['isbn', 'author', 'name', 'category', 'quantity', 'fine']


@admin.register(Review)
class ReviewAdminView(admin.ModelAdmin):
    list_display = ['by', 'book', 'rating', 'comment']


@admin.register(BookIssue)
class BookIssueAminView(admin.ModelAdmin):
    list_display = ['book', 'member', 'issue_date', 'due_date', 'status']


@admin.register(Income)
class IncomeAdminView(admin.ModelAdmin):
    list_display = ['name', 'money', 'date_recorded']


@admin.register(Expense)
class ExpenseAdminView(admin.ModelAdmin):
    list_display = ['name', 'money', 'date_recorded']
