from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UsernameField, PasswordChangeForm, \
    PasswordResetForm, SetPasswordForm
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

from library.models import Staff, Member, Book, Author, Category, BookIssue


class SigninForm(AuthenticationForm):
    username = UsernameField(widget=forms.TextInput(attrs={
        'autofocus': True,
        'class': 'bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-primary-500 '
                 'focus:border-primary-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 '
                 'dark:placeholder-gray-400 dark:text-white dark:focus:ring-primary-500 dark:focus:border-primary-500',
        'placeholder': 'username'
    }))
    password = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={
            'autocomplete': 'current-password',
            'class': 'bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-primary-500 '
                     'focus:border-primary-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 '
                     'dark:placeholder-gray-400 dark:text-white dark:focus:ring-primary-500 '
                     'dark:focus:border-primary-500',
            'placeholder': '••••••••'
        }),
    )


class SignupFormUser(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name')

    def __init__(self, *args, **kwargs):
        super(SignupFormUser, self).__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            self.fields[field_name].widget.attrs['placeholder'] = field.label
            self.fields[field_name].widget.attrs[
                'class'] = 'bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg ' \
                           'focus:ring-primary-500 focus:border-primary-500 block w-full p-2.5 dark:bg-gray-700 ' \
                           'dark:border-gray-600 dark:placeholder-gray-400 dark:text-white ' \
                           'dark:focus:ring-primary-500 dark:focus:border-primary-500'
            self.fields[field_name].widget.attrs['required'] = True


class UpdateUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name')


class SignupFormMember(forms.ModelForm):
    class Meta:
        model = Member
        fields = ('address',)

    def __init__(self, *args, **kwargs):
        super(SignupFormMember, self).__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            self.fields[field_name].widget.attrs['placeholder'] = field.label
            self.fields[field_name].widget.attrs[
                'class'] = 'bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg ' \
                           'focus:ring-primary-500 focus:border-primary-500 block w-full p-2.5 dark:bg-gray-700 ' \
                           'dark:border-gray-600 dark:placeholder-gray-400 dark:text-white ' \
                           'dark:focus:ring-primary-500 dark:focus:border-primary-500'
            self.fields[field_name].widget.attrs['required'] = True


class SignupFormStaff(forms.ModelForm):
    class Meta:
        model = Staff
        fields = ('position',)

    def __init__(self, *args, **kwargs):
        super(SignupFormStaff, self).__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            self.fields[field_name].widget.attrs['placeholder'] = field.label
            self.fields[field_name].widget.attrs[
                'class'] = 'bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg ' \
                           'focus:ring-primary-500 focus:border-primary-500 block w-full p-2.5 dark:bg-gray-700 ' \
                           'dark:border-gray-600 dark:placeholder-gray-400 dark:text-white ' \
                           'dark:focus:ring-primary-500 dark:focus:border-primary-500'
            self.fields[field_name].widget.attrs['required'] = True


class UserPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': 'bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-primary-500 '
                 'focus:border-primary-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 '
                 'dark:placeholder-gray-400 dark:text-white dark:focus:ring-primary-500 dark:focus:border-primary-500',
        'placeholder': 'name@company.com'
    }))


class UserSetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(max_length=50, widget=forms.PasswordInput(attrs={
        'class': 'bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-primary-500 '
                 'focus:border-primary-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 '
                 'dark:placeholder-gray-400 dark:text-white dark:focus:ring-primary-500 dark:focus:border-primary-500',
        'placeholder': 'New Password'
    }), label="New Password")
    new_password2 = forms.CharField(max_length=50, widget=forms.PasswordInput(attrs={
        'class': 'bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-primary-500 '
                 'focus:border-primary-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 '
                 'dark:placeholder-gray-400 dark:text-white dark:focus:ring-primary-500 dark:focus:border-primary-500',
        'placeholder': 'Confirm New Password'
    }), label="Confirm New Password")


class UserPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(max_length=50, widget=forms.PasswordInput(attrs={
        'class': 'bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-primary-500 '
                 'focus:border-primary-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 '
                 'dark:placeholder-gray-400 dark:text-white dark:focus:ring-primary-500 dark:focus:border-primary-500',
        'placeholder': 'Old Password'
    }), label='Old Password')
    new_password1 = forms.CharField(max_length=50, widget=forms.PasswordInput(attrs={
        'class': 'bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-primary-500 '
                 'focus:border-primary-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 '
                 'dark:placeholder-gray-400 dark:text-white dark:focus:ring-primary-500 dark:focus:border-primary-500',
        'placeholder': 'New Password'
    }), label="New Password")
    new_password2 = forms.CharField(max_length=50, widget=forms.PasswordInput(attrs={
        'class': 'bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-primary-500 '
                 'focus:border-primary-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 '
                 'dark:placeholder-gray-400 dark:text-white dark:focus:ring-primary-500 dark:focus:border-primary-500',
        'placeholder': 'Confirm New Password'
    }), label="Confirm New Password")


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Staff
        exclude = ('user', 'avatar', 'date_added')

    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            self.fields[field_name].widget.attrs['placeholder'] = field.label
            if field_name in ['date_added']:
                self.fields[field_name].widget.attrs['placeholder'] = 'YYYY-MM-DD'
            self.fields[field_name].widget.attrs['class'] = \
                'shadow-sm bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg ' \
                'focus:ring-primary-500 focus:border-primary-500 block w-full p-2.5 dark:bg-gray-700 ' \
                'dark:border-gray-600 dark:placeholder-gray-400 dark:text-white ' \
                'dark:focus:ring-primary-500 dark:focus:border-primary-500'
            self.fields[field_name].widget.attrs['required'] = False


class AuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = ('first_name', 'last_name', 'summary')

    def __init__(self, *args, **kwargs):
        super(AuthorForm, self).__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            self.fields[field_name].widget.attrs['placeholder'] = field.label
            self.fields[field_name].widget.attrs[
                'class'] = 'bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg ' \
                           'focus:ring-primary-500 focus:border-primary-500 block w-full p-2.5 dark:bg-gray-700 ' \
                           'dark:border-gray-600 dark:placeholder-gray-400 dark:text-white ' \
                           'dark:focus:ring-primary-500 dark:focus:border-primary-500'
            self.fields[field_name].widget.attrs['required'] = True


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ('name', 'description')

    def __init__(self, *args, **kwargs):
        super(CategoryForm, self).__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            self.fields[field_name].widget.attrs['placeholder'] = field.label
            self.fields[field_name].widget.attrs[
                'class'] = 'bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg ' \
                           'focus:ring-primary-500 focus:border-primary-500 block w-full p-2.5 dark:bg-gray-700 ' \
                           'dark:border-gray-600 dark:placeholder-gray-400 dark:text-white ' \
                           'dark:focus:ring-primary-500 dark:focus:border-primary-500'
            self.fields[field_name].widget.attrs['required'] = True


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = (
            'name', 'isbn', 'author', 'category', 'summary',
            'cover_page', 'date_published', 'barcode', 'quantity', 'fine'
        )

    def __init__(self, *args, **kwargs):
        super(BookForm, self).__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            self.fields[field_name].widget.attrs['placeholder'] = field.label
            if field_name in ['date_published']:
                self.fields[field_name].widget.attrs['placeholder'] = 'YYYY-MM-DD'
            self.fields[field_name].widget.attrs[
                'class'] = 'bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg ' \
                           'focus:ring-primary-500 focus:border-primary-500 block w-full p-2.5 dark:bg-gray-700 ' \
                           'dark:border-gray-600 dark:placeholder-gray-400 dark:text-white ' \
                           'dark:focus:ring-primary-500 dark:focus:border-primary-500'
            # self.fields[field_name].widget.attrs['required'] = True


class BookIssueForm(forms.ModelForm):
    return_date = forms.DateField(required=False)

    class Meta:
        model = BookIssue
        fields = ('book', 'member', 'issue_date', 'due_date', 'return_date')

    def __init__(self, *args, **kwargs):
        super(BookIssueForm, self).__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            self.fields[field_name].widget.attrs['placeholder'] = field.label
            if field_name in ['issue_date', 'due_date', 'returns_date']:
                self.fields[field_name].widget.attrs['placeholder'] = 'YYYY-MM-DD'
            self.fields[field_name].widget.attrs[
                'class'] = 'bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg ' \
                           'focus:ring-primary-500 focus:border-primary-500 block w-full p-2.5 dark:bg-gray-700 ' \
                           'dark:border-gray-600 dark:placeholder-gray-400 dark:text-white ' \
                           'dark:focus:ring-primary-500 dark:focus:border-primary-500'
            self.fields[field_name].widget.attrs['required'] = True
