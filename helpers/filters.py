from django.utils.translation import gettext_lazy as _
from django_filters import rest_framework as filters

from budget.choices import ModelChoices
from budget.models import BudgetItem


class BudgetItemFilter(filters.FilterSet):
    item_type = filters.ChoiceFilter(
        field_name="item_type",
        label="Type",
        lookup_expr="exact",
        choices=ModelChoices.BUDGET_ITEM_TYPE,
        help_text=_(
            "Applies filter by item_type. Returns records where `item_type` is equal to passed value."
        ),
    )

    min_amount = filters.NumberFilter(field_name="amount", lookup_expr='gte')
    max_amount = filters.NumberFilter(field_name="amount", lookup_expr='lte')

    class Meta:
        model = BudgetItem
        fields = ['item_type', 'min_amount', 'max_amount']
