import uuid

from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager
from django.conf import settings
# Note: AbstractUser already inherits PermissionsMixin,
# so importing PermissionsMixin is usually unnecessary.

# ------------------------------------------------------------------
# Custom Manager
# ------------------------------------------------------------------
# A manager controls how User objects are created.
# Instead of using the default UserManager directly,
# we customize it to support email-based authentication.
# ------------------------------------------------------------------

class CustomUserManager(UserManager):

    # Internal helper method used by both create_user()
    # and create_superuser() to avoid duplicate code.
    def _create_user(self, name, email, password, **extra_fields):

        # Every user must have an email.
        if not email:
            raise ValueError("You have not specified a valid e-mail address")

        # Normalize the email.
        # Example:
        # JENIL@GMAIL.COM -> JENIL@gmail.com
        email = self.normalize_email(email)

        # self.model refers to the User model that uses this manager.
        user = self.model(
            email=email,
            name=name,
            **extra_fields
        )

        # NEVER store plain-text passwords.
        # set_password() hashes the password securely.
        user.set_password(password)

        # Save the user to the database.
        # _db is provided by Django's manager.
        user.save(using=self._db)

        return user

    # Creates a normal user.
    def create_user(self, name=None, email=None, password=None, **extra_fields):

        # Normal users cannot access Django Admin.
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)

        return self._create_user(
            name,
            email,
            password,
            **extra_fields
        )

    # Creates an admin/superuser.
    def create_superuser(self, name=None, email=None, password=None, **extra_fields):

        # Superusers can access admin and have all permissions.
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        return self._create_user(
            name,
            email,
            password,
            **extra_fields
        )
    

# ------------------------------------------------------------------
# Custom User Model
# ------------------------------------------------------------------
# We inherit from AbstractUser to reuse Django's authentication system
# while adding our own custom fields.
# ------------------------------------------------------------------

class User(AbstractUser):

    # UUID primary key instead of integer IDs.
    # Example:
    # 550e8400-e29b-41d4-a716-446655440000
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    username = None
    # Email must be unique because users will log in using email.
    email = models.EmailField(unique=True)

    # Custom name field.
    name = models.CharField(
        max_length=150,
        blank=True,
        null=True
    )

    # Stores profile picture.
    # Uploaded files go to:
    # media/uploads/avatars/
    avatar = models.ImageField(
        upload_to="uploads/avatars",
        blank=True,
        null=True
    )

    # Whether the account is active.
    # Inactive users cannot log in.
    is_active = models.BooleanField(default=True)

    # Can access Django Admin.
    is_staff = models.BooleanField(default=False)

    # Has every permission.
    is_superuser = models.BooleanField(default=False)

    # Automatically set when the user is created.
    date_joined = models.DateTimeField(auto_now_add=True)

    # Django normally manages last_login automatically.
    # You usually don't redefine this field unless necessary.
    last_login = models.DateTimeField(null=True, blank=True)

    # Use our custom manager instead of Django's default one.
    objects = CustomUserManager()

    # Tell Django to use email for authentication.
    # Login:
    # Email + Password
    USERNAME_FIELD = "email"

    # Which field represents the user's email.
    EMAIL_FIELD = "email"

    # Extra fields required when creating a superuser.
    # Django will ask:
    #
    # Email:
    # Name:
    # Password:
    #
    REQUIRED_FIELDS = ["name"]
    
    def avatar_url(self):
        if self.avatar:
            return f'{settings.WEBSITE_URL}{self.avatar.url}'
        else:
            return ''

