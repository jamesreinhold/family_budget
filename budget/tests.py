from decimal import Decimal
from django.contrib.auth import get_user_model
from django.test import TestCase

from .models import BudgetItem

User = get_user_model()

class BudgetItemTestCase(TestCase):
    def setUp(self):
        user = User.objects.create(username="test_user", email="test_user@domain.com")
        BudgetItem.create(
            user=user,
            name="Bread", 
            amount=Decimal(23.45),
            quantity=5
        )
        BudgetItem.create(
            user=user,
            name="Salary", 
            amount=Decimal(2500.17),
            item_type="INCOME"
        )

    def test_budget_item_type(self):
        expense = BudgetItem.objects.get(name="Bread")
        income = BudgetItem.objects.get(name="Salary")
        self.assertEqual(income.item_type, 'INCOME')
        self.assertEqual(expense.item_type, 'EXPENSE')


    def test_user_income(self):
        user = User.objects.get(username="test_user")
        self.assertEqual(str(user.income), "{:.2f}".format(2500.17))
    
    def test_user_expense(self):
        user = User.objects.get(username="test_user")
        self.assertEqual(str(user.expenses), "{:.2f}".format(117.25))