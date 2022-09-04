from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class UsersConfig(AppConfig):
    name = "family_budget.users"
    verbose_name = _("Users")

    def ready(self):
        try:
            import family_budget.users.receivers  # noqa F401
        except ImportError:
            pass
