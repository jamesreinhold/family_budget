import logging

from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from rest_framework_friendly_errors.mixins import FriendlyErrorMessagesMixin

from budget.choices import ModelChoices
from budget.models import Budget, BudgetItem

logger = logging.getLogger(__name__)
User = get_user_model()



class BudgetItemSerializer(FriendlyErrorMessagesMixin, serializers.ModelSerializer):
    name = serializers.CharField(
        min_length=2,
        max_length=20, 
        help_text=_("The name of the budget item")
    )

    quantity = serializers.IntegerField(
        default=1,
        required=False,
        help_text=_("If quantity is more than 1, specify the quality "
        "of the budget item. Defaults to 1.")
    )

    item_type = serializers.ChoiceField(
        choices=ModelChoices.BUDGET_ITEM_TYPE,
        default=ModelChoices.BUDGET_ITEM_TYPE_EXPENSES,
        help_text=_("The type of budget item.")
    )

    total = serializers.SerializerMethodField()

    class Meta:
        model = BudgetItem
        fields = "__all__"
        # fields = (
        #     "id",
        #     "user",
        #     "budget_type,"
        #     "name",
        #     "quantity",
        #     "amount",
        #     "total",
        #     "created_at",
        #     "updated_at",
        #     "linked_to_budget"
        # )
        read_only_fields = (
            "id",
            "user",
            "created_at",
            "updated_at"
        )
    
    def get_total(self, obj):
        return obj.total
    
    def validate_name(self, value):
        if item_exist := self.Meta.model.objects.filter(name__iexact=value).exists():
            self.register_error(
                error_message="An item already exists with this name.",
                error_code="name_already_exist",
                field_name="name"
            )
        
        return value
    
    def create(self, validated_data):
        logger.info(f"{__name__}: Creating a budget item:")
        if validated_data['item_type'] == ModelChoices.BUDGET_ITEM_TYPE_EXPENSES:
            return self.Meta.model.create(
                user=self.context['request'].user,
                name=validated_data['name'],
                quantity=validated_data['quantity'],
                amount=validated_data['amount']
            )
        return self.Meta.model.create(
                user=self.context['request'].user,
                name=validated_data['name'],
                amount=validated_data['amount'],
                item_type=ModelChoices.BUDGET_ITEM_TYPE_INCOME
            )



class BudgetItemResponseSerializer(FriendlyErrorMessagesMixin, serializers.ModelSerializer):
    name = serializers.CharField(
        min_length=2,
        max_length=20, 
        help_text=_("The name of the budget item")
    )

    quantity = serializers.IntegerField(
        default=1,
        required=False,
        help_text=_("If quantity is more than 1, specify the quality "
        "of the budget item. Defaults to 1.")
    )

    class Meta:
        model = BudgetItem
        fields = ("name", "item_type", "amount", "quantity")
    

class BudgetSerializer(FriendlyErrorMessagesMixin, serializers.ModelSerializer):
    name = serializers.CharField(
        min_length=2,
        max_length=20, 
        help_text=_("The name of the budget item")
    )

    category = serializers.ChoiceField(
        choices=ModelChoices.BUDGET_CATEGORY,
        default=ModelChoices.BUDGET_CATEGORY_GENERAL,
        help_text=_("The category of the budget")
    )

    budget_items = BudgetItemResponseSerializer(many=True)

    class Meta:
        model = Budget
        fields = "__all__"
    
    def validate_name(self, value):
        if budget_exist := self.Meta.model.objects.filter(name__iexact=value).exists():
            self.register_error(
                error_message="A budget already exists with this name.",
                error_code="name_already_exist",
                field_name="name"
            )
        
        return value

    def create(self, validated_data):
        return super().create(validated_data)
