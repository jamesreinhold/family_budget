import contextlib
import logging

from django.http.response import Http404
from django.utils.translation import gettext_lazy as _
from rest_framework import status
from rest_framework.mixins import (
    CreateModelMixin,
    DestroyModelMixin,
    ListModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
)
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from budget.models import BudgetItem

from .serializers import BudgetItemSerializer

logger = logging.getLogger(__name__)


class BudgetItemViewSet(
    RetrieveModelMixin,
    ListModelMixin,
    UpdateModelMixin,
    GenericViewSet,
    DestroyModelMixin,
    CreateModelMixin):
    """
    Create a Budget Item

    This endpoint allows you to create a new Budget Item.
    """

    queryset = BudgetItem.objects.all()
    lookup_field = "budget_item_id"
    lookup_value_regex = "[0-9a-fA-F]{8}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{12}"
    serializer_class = BudgetItemSerializer

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action in ["list"]:
            permission_classes = [IsAdminUser]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def get_object(self, queryset=None):
        return BudgetItem.objects.filter(pk=self.kwargs["budget_item_id"]).first()

    def list(self, request, *args, **kwargs):
        """
        List Budget Items

        Endpoints retrieves the list of Budget Items.
        """
        return super(BudgetItemViewSet, self).list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        """
        Get Budget Item

        Retrieve the information of Budget Item by passed Id.
        """
        try:
            instance = self.get_object()
        except Exception as e:
            return Response({"message": str(e)})
        else:
            # any additional logic
            serializer = self.get_serializer(instance)

            return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        """
        Update a Budget Item

        Update the record of a Budget Item.
        """
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

    def partial_update(self, request, *args, **kwargs):
        """
        Patch a Budget Item

        Patch a Budget Item by passed Id.
        """
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

    def destroy(self, request, *args, **kwargs):
        """
        Delete a Budget Item

        Delete the record of a Budget Item by passed Id.
        """
        with contextlib.suppress(Http404):
            instance = self.get_object()
            self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
