from django.urls import path

from web.views import *

app_name = 'web'
urlpatterns = [
    path('', dashboard, name='dashboard'),

    path('login/', SignInView.as_view(), name="login"),
    path('signup/', SignUpView.as_view(), name="signup"),
    path('logout/', logout_view, name="logout"),

    path('profile/', profile, name='profile'),
    path('upload-avatar/', upload_avatar, name='upload_avatar'),
    path('change-password/', change_password, name='change_password'),

    path('staff-members/', staff_members_list, name='staff_members'),
    path('library-members/', library_members_list, name='library_members'),
    path('financials/', financials, name='financials'),

    path('delete-staff/<int:pk>/', delete_staff_member, name="delete_staff"),

    path('delete-member/<int:pk>/', delete_member, name="delete_member"),
    path('update-member/<int:pk>/', update_member, name="update_member"),
    path('member-change-password/<int:pk>/', member_change_password, name="member_change_password"),

    path('books-categories/', books_categories, name='categories'),
    path('delete-category/<int:pk>/', delete_category, name="delete_category"),
    path('update-category/<int:pk>/', update_category, name="update_category"),

    path('authors/', books_authors, name='authors'),
    path('delete-author/<int:pk>/', delete_author, name="delete_author"),
    path('update-author/<int:pk>/', update_author, name="update_author"),

    path('library-books/', books_list, name='books'),
    path('delete-book/<int:pk>/', delete_book, name="delete_book"),
    path('update-book/<int:pk>/', update_book, name="update_book"),

    path('book-issues/', books_issues_list, name='issues'),
    path('delete-book-issue/<int:pk>/', delete_book_issue, name="delete_book_issue"),
    path('update-book-issue/<int:pk>/', update_book_issue, name="update_book_issue"),

]
