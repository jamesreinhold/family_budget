from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework_friendly_errors.mixins import FriendlyErrorMessagesMixin


User = get_user_model()


class UserSerializer(FriendlyErrorMessagesMixin, serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = (
            "password",
        )
