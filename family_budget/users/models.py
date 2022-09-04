import logging
import uuid

from django.contrib.auth.models import AbstractUser, User
from django.db import models
from django.utils import timezone
from django.utils.functional import cached_property
from django.utils.translation import gettext_lazy as _

logger = logging.getLogger(__name__)


NULL_AND_BLANK = {'null': True, 'blank': True}


class User(AbstractUser):
    """
    # Each `User` needs a human-readable unique identifier that we can use to
    # represent the `User` in the UI. We want to index this column in the
    # database to improve lookup performance.
    username = models.CharField(db_index=True, max_length=255, unique=True)

    # We also need a way to contact the user and a way for the user to identify
    # themselves when logging in. Since we need an email address for contacting
    # the user anyways, we will use it for logging in because it is
    # the most common form of login credential at the time of writing.
    email = models.EmailField(db_index=True, unique=True)

    # When a user no longer wishes to use our platform, they may try to delete
    # there account. That's a problem for us because the data we collect is
    # valuable to us and we don't want to delete it. To solve this problem, we
    # will simply offer users a way to deactivate their account.
    # That way they won't show up on the site anymore,
    # but we can still analyze the data.
    is_active = models.BooleanField(default=True)

    # The `is_staff` flag is expected by Django to determine who can and cannot
    # log into the Django admin site. For most users this flag will always be
    # falsed.
    is_staff = models.BooleanField(default=False)
    """

    # region Fields
    # The `USERNAME_FIELD` property tells us which field we will use to log in.
    # In this case, we want that to be the email field.
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]
    # objects = UserManager()

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        verbose_name="ID",
        help_text=_(
            """The unique identifier of the instance this object belongs to. 
            Mandatory, unless a new instance to create is given."""
        )
    )

    first_name = models.CharField(
        verbose_name=_("First names"),
        max_length=125,
        help_text=_("First name of the user."),
        **NULL_AND_BLANK
    )

    last_name = models.CharField(
        verbose_name=_("Last names"),
        max_length=125,
        help_text=_("Last name of the user."),
        **NULL_AND_BLANK
    )

    name = models.CharField(
        verbose_name=_("Full names"),
        max_length=125,
        **NULL_AND_BLANK,
        help_text=_(
            """Full name of the user. If user account type is `business`, 
            then this represents company's name."""
        ),
    )

    username = models.CharField(
        verbose_name=_("Username"),
        max_length=50,
        **NULL_AND_BLANK,
        unique=True,
        db_index=True,
        help_text=_(
            """Customers username. This cannot be used to login. 
            A username maybe used to generate a Paylink Profile."""
        ),
    )

    email = models.EmailField(
        verbose_name=_("Email"),
        unique=True,
        db_index=True,
        help_text=_("The primary email address of the user"),
    )

    email_verified = models.BooleanField(
        default=False,
        verbose_name=_("Email verified"),
        help_text=_("Flag to determine if user has verified their email address"),
        editable=False
    )

    date_joined = models.DateTimeField(
        default=timezone.now,
        blank=True,
        verbose_name=_("Joined Date"),
        editable=False,
        help_text=_("The date client joined the website."),
    )

    last_failed_login = models.DateTimeField(
        **NULL_AND_BLANK,
        editable=False,
        verbose_name=_("Last Failed Login"),
        help_text=_(
            """The date recorded when last the user failed to 
            login into account. Each attempt of failed login 
            is recorded for security and audit purposes."""
        ),
    )

    last_password_change = models.DateTimeField(
        **NULL_AND_BLANK,
        editable=False,
        verbose_name=_("Last Password Change"),
        help_text=_(
            """The date recorded when last the user 
            changed password. Each password change is 
            recorded for security and audit purposes."""
        ),
    )

    password_change_at = models.DateTimeField(
        **NULL_AND_BLANK,
        editable=False,
        verbose_name=_("Password Change")
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        editable=False,
        verbose_name=_("Updated"),
        **NULL_AND_BLANK,
        help_text=_(
            """Timestamp when the record was modified. 
            The date and time are displayed in the Timezone 
            from where request is made. 
            e.g. 2019-14-29T00:15:09Z for April 29, 2019 0:15:09 UTC"""
        ),
    )


    # region Metadata
    class Meta:
        """Meta for the naming in the django admin that
        describes a model if the object is singular or
        plural
        """
        verbose_name = _("User")
        verbose_name_plural = _("Users")
        ordering = ("-date_joined",)
        constraints = [
            models.UniqueConstraint(
                fields=["first_name", "last_name", "email"], name="unique_user"
            )
        ]
        indexes = [
            models.Index(fields=["last_name", "first_name"]),
            models.Index(fields=["first_name"], name="first_name_idx"),
        ]

    # endregion

    # region Methods
    def __str__(self):
        return self.email

    def save(self, *args, **kwargs):
        """On save, update timestamps"""
        if not self.id:
            self.date_joined = timezone.now()
        self.updated_at = timezone.now()
        return super(User, self).save(*args, **kwargs)

    @cached_property
    def initials(self):
        """Get the initials of a user"""
        try:
            return self.first_name[0].upper() + self.last_name[0].upper()
        except IndexError:
            return "GP"

    @cached_property
    def full_name(self):
        if self.first_name is not None:
            return f"{self.first_name} {self.last_name}"
        return "N/A"



