import logging

from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from rest_framework_friendly_errors.mixins import FriendlyErrorMessagesMixin

from budget.models import BudgetItem

logger = logging.getLogger(__name__)
User = get_user_model()



class BudgetItemSerializer(FriendlyErrorMessagesMixin, serializers.ModelSerializer):
    name = serializers.CharField(
        min_length=2,
        max_length=20, 
        help_text=_("The name of the budget item")
    )

    class Meta:
        model = BudgetItem
        fields = "__all__"
    
    def create(self, validated_data):
        return super().create(validated_data)
