from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _
import logging

from .choices import ModelChoices
from .common import NULL_AND_BLANK, BaseModel, Timestampable

from django.contrib.auth import get_user_model

User = get_user_model()
logger = logging.getLogger(__name__)    

class BudgetItem(BaseModel, Timestampable):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        editable=False
    )

    type = models.CharField(
        max_length=7,
        choices=ModelChoices.BUDGET_ITEM_TYPE,
        default=ModelChoices.BUDGET_ITEM_TYPE_EXPENSES,
        help_text=_("The type of budget item.")
    )

    name = models.CharField(
        max_length=20, 
        help_text=_("The name of the budget item"),
        unique=True,
    )

    amount = models.DecimalField(
        verbose_name=_("Amount"),
        default=1.00,
        decimal_places=2,
        max_digits=9,
        help_text=_("The amount value of the budget item.")
    )

    quantity = models.PositiveSmallIntegerField(
        default=0,
        **NULL_AND_BLANK,
        help_text=_("If quantity is more than 1, specify the quality "
        "of the budget item. Defaults to 1. Quantity is required if `type` is `EXPENSE`.")
    )

    linked_to_budget = models.BooleanField(
        default=False,
        help_text=_("A flag to determine if budget item is linked to a budget."),
        editable=False
    )

    #Metadata
    class Meta :
        verbose_name = _("Budget Item")
        verbose_name_plural = _("Budget Item")
        ordering = ['-created_at']


    def __str__(self) -> str:
        return self.name
    
    @property
    def linked_budget(self):
        """Returns list of budgets item is/are linked"""
        pass
    
    @property
    def total(self) -> str:
        return self.quantity * self.cost
    
    @classmethod
    def create(
        cls, 
        user:User, 
        name:str, 
        amount:float, 
        quantity:int=None, 
        type:str=ModelChoices.BUDGET_ITEM_TYPE_EXPENSES):
        """
        Creates a Budget Item

        Args:
            user (User): The user ID
            name (str): The name of the budget item
            amount (float): The amount of the budget item
            quantity (int, optional): The quantity of the budget item if type is an expense
            type (str, optional): The type of the budget item. Defaults to ModelChoices.BUDGET_ITEM_TYPE_EXPENSES.
        """
        logger.info(f"Create a budget item: {type}")
        if type == ModelChoices.BUDGET_ITEM_TYPE_EXPENSES:
            return cls.objects.create(user=user, name=name, quantity=quantity, amount=amount)

        else:
            return cls.objects.create(user=user, name=name, amount=amount, type="INCOME")



class Budget(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    category = models.CharField(
        max_length=14,
        choices=ModelChoices.BUDGET_CATEGORY,
        default=ModelChoices.BUDGET_CATEGORY_GENERAL,
        help_text=_("The category of the budget")
    )

    name = models.CharField(
        max_length=75,
        help_text=_("The name of the budget. This is the friendly name of the budget.")
    )

    budget_items = models.ManyToManyField(
        BudgetItem,
        help_text=_("The items of the budget")
    )

    def __str__(self) -> str:
        return self.name

