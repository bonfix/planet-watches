import uuid

from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser


class UserManager(BaseUserManager):
    def create_user(self, email, password=None):
        """
        Create and return a `User` with an email, username and password.
        """
        if not email:
            raise ValueError("Users Must Have an email address")

        user = self.model(
            email=self.normalize_email(email),
        )
        user.is_active = False
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        """
        Create and return a `User` with superuser (admin) permissions.
        """
        if password is None:
            raise TypeError("Superusers must have a password.")

        user = self.create_user(email, password)
        user.is_superuser = True
        user.is_staff = True
        user.save()

        return user


class User(AbstractBaseUser):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(
        verbose_name="email address", max_length=255, unique=True
    )
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    # Tells Django that the UserManager class defined above should manage
    # objects of this type.
    objects = UserManager()

    def __str__(self):
        return self.email

    class Meta:
        """
        to set table name in database
        """

        db_table = "User"


class UserProfile(models.Model):
    """
    to store all other attributes associated to user
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="profile"
    )
    name = models.CharField(max_length=50, unique=False)

    class Meta:
        """
        to set table name in database
        """

        db_table = "profile"


class MyModelBase(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # deleted_at = models.DateTimeField(blank=True, null=True)
    status = models.IntegerField(default=1)

    class Meta:
        abstract = True


# table to store outgoing emails
class Email(MyModelBase):
    type = models.CharField(max_length=255)
    subject = models.CharField(max_length=255)
    body = models.TextField()
    status = models.PositiveSmallIntegerField(default=0)

    class Meta:
            """
            to set table name in database
            """

            db_table = "email"


class AccountActivationCode(MyModelBase):
    # user = models.ForeignKey(User, on_delete=models.CASCADE)
    email = models.EmailField(max_length=255)
    verification_code = models.CharField(max_length=10)
    status = models.PositiveSmallIntegerField(default=1)