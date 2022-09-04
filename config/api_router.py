from django.conf import settings
from rest_framework.routers import DefaultRouter, SimpleRouter

from budget.api.views import BudgetItemViewSet, BudgetViewSet
from family_budget.users.api.views import UserViewSet

router = DefaultRouter() if settings.DEBUG else SimpleRouter()


router.register("users", UserViewSet)
router.register("budget-items", BudgetItemViewSet)
router.register("budgets", BudgetViewSet)

app_name = "api"
urlpatterns = router.urls
