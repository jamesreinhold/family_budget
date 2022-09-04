from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

from .choices import BUDGET_CATEGORY, BUDGET_CATEGORY_GENERAL
from .common import NULL_AND_BLANK, BaseModel, Timestampable


class BudgetItem(BaseModel, Timestampable):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    name = models.CharField(
        max_length=20, 
        help_text=_("The name of the budget item")
    )

    cost = models.DecimalField(
        verbose_name=_("Cost"),
        default=0.00,
        decimal_places=2,
        max_digits=9,
        help_text=_("The cost of the budget item.")
    )

    quantity = models.PositiveSmallIntegerField(
        default=1,
        **NULL_AND_BLANK,
        help_text=_("If quantity is more than 1, specify the quality "
        "of the budget item. Defaults to 1.")
    )

    linked_to_budget = models.BooleanField(
        default=False,
        help_text=_("A flag to determine if budget item is linked to a budget.")
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



class Budget(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    category = models.CharField(
        max_length=14,
        choices=BUDGET_CATEGORY,
        default=BUDGET_CATEGORY_GENERAL,
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

