from django.contrib.auth.models import AbstractBaseUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

from skymarket.users.managers import UserManager


class UserRoles:
    USER = "user"
    ADMIN = "admin"
    choices = (
        (USER, USER),
        (ADMIN, ADMIN),
    )


class User(AbstractBaseUser):
    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'phone', "role"]

    first_name = models.CharField(
        max_length=64,
        null=True,
        verbose_name="Имя",
        help_text="Введите имя, макс 64 символа",
    )

    last_name = models.CharField(
        max_length=64,
        null=True,
        verbose_name="Фамилия",
        help_text="Введите фамилию, макс 64 символа",
    )

    email = models.EmailField(
        unique=True,
        max_length=50,
        verbose_name="email address",
        help_text="Укажите электронную почту",
    )

    phone = PhoneNumberField(
        max_length=20,
        null=True,
        verbose_name="Телефон для связи",
        help_text="Укажите телефон для связи",

    )

    role = models.CharField(
        max_length=20,
        choices=UserRoles.choices,
        default=UserRoles.USER,
        verbose_name="Роль пользователя",
        help_text="Выберите роль пользователя",
    )

    image = models.ImageField(
        upload_to="photos/",
        verbose_name="фото",
        help_text="Разместите Ваше фото",
        null=True,
        blank=True,
    )

    is_active = models.BooleanField(
        null=True,
        default=True,
        verbose_name="Аккаунт активен",
        help_text="Укажите, активен ли аккаунт"
    )

    @property
    def is_superuser(self):
        return self.is_admin

    @property
    def is_staff(self):
        return self.is_admin

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return self.is_admin

    @property
    def is_admin(self):
        return self.role == UserRoles.ADMIN

    @property
    def is_user(self):
        return self.role == UserRoles.USER

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        ordering = ["email"]

