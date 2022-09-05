import contextlib
import logging

from django.http.response import Http404
from django.utils.translation import gettext_lazy as _
from rest_framework import status, filters
from rest_framework.mixins import (
    CreateModelMixin,
    DestroyModelMixin,
    ListModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from budget.models import Budget, BudgetItem
from helpers.filters import BudgetItemFilter

from .serializers import BudgetItemSerializer, BudgetSerializer
from django_filters.rest_framework import DjangoFilterBackend

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

    This endpoint allows you to create a new Budget Item by an authenticated user.
    """
    queryset = BudgetItem.objects.all()
    lookup_field = "budget_item_id"
    lookup_value_regex = "[0-9a-fA-F]{8}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{12}"
    serializer_class = BudgetItemSerializer
    permission_classes = [IsAuthenticated]
    search_fields = (
        "name", "type"
    )
    ordering_fields = ['created_at', 'updated_at']
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    filterset_class = BudgetItemFilter

    # def get_permissions(self):
    #     """
    #     Instantiates and returns the list of permissions that this view requires.
    #     """
    #     if self.action in ["destroy"]:
    #         permission_classes = [IsAdminUser]
    #     else:
    #         permission_classes = [IsAuthenticated]
    #     return [permission() for permission in permission_classes]

    def get_object(self, queryset=None):
        return BudgetItem.objects.filter(pk=self.kwargs["budget_item_id"]).first()

    def list(self, request, *args, **kwargs):
        """
        List Budget Items

        Endpoints retrieves the list of Budget Items.
        
        **Search fields**:
        You can search and filter by `name` and `type`
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


class BudgetViewSet(
    RetrieveModelMixin,
    ListModelMixin,
    UpdateModelMixin,
    GenericViewSet,
    DestroyModelMixin,
    CreateModelMixin):
    """
    Create a Budget

    This endpoint allows you to create a new Budget by an authenticated user.
    """

    queryset = Budget.objects.all()
    lookup_field = "budget_id"
    lookup_value_regex = "[0-9a-fA-F]{8}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{12}"
    serializer_class = BudgetSerializer
    permission_classes = [IsAuthenticated]

    # def get_permissions(self):
    #     """
    #     Instantiates and returns the list of permissions that this view requires.
    #     """
    #     if self.action in ["list"]:
    #         permission_classes = [IsAdminUser]
    #     else:
    #         permission_classes = [IsAuthenticated]
    #     return [permission() for permission in permission_classes]

    def get_object(self, queryset=None):
        return Budget.objects.filter(pk=self.kwargs["budget_id"]).first()

    def list(self, request, *args, **kwargs):
        """
        List Budgets

        Endpoints retrieves the list of Budgets.
        """
        return super(BudgetViewSet, self).list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        """
        Get Budget

        Retrieve the information of Budget by passed Id.
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
        Update a Budget

        Update the record of a Budget.
        """
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

    def partial_update(self, request, *args, **kwargs):
        """
        Patch a Budget

        Patch a Budget by passed Id.
        """
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

    def destroy(self, request, *args, **kwargs):
        """
        Delete a Budget

        Delete the record of a Budget by passed Id.
        """
        with contextlib.suppress(Http404):
            instance = self.get_object()
            self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
