from rest_framework import serializers

from library.models import User, Staff, Member, Category, Author, Book, BookIssue, Income, Expense


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class StaffSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False)

    class Meta:
        model = Staff
        fields = '__all__'


class MemberSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False)

    class Meta:
        model = Member
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = '__all__'


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'


class BookIssueSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookIssue
        fields = '__all__'


class IncomeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Income
        fields = '__all__'


class ExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expense
        fields = '__all__'


class IncomeDashboardSerializer(serializers.Serializer):
    month = serializers.DateTimeField(format='%Y/%m/%d')
    total = serializers.DecimalField(default=0, max_digits=63, decimal_places=2)
