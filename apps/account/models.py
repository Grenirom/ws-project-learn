import uuid
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.core.validators import MinValueValidator, MaxValueValidator, RegexValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.account.managers import MyUserManager


class CustomUser(AbstractUser, PermissionsMixin):
    username = models.CharField(50, blank=True, null=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True, max_length=155)
    image = models.ImageField(upload_to='avatars', default='avatars/default_avatar.jpg', blank=True)
    password = models.CharField(validators=[
        MinValueValidator(limit_value=8),
        MaxValueValidator(limit_value=20),
        RegexValidator(
            regex=r'^(?=.*[a-zA-Z])(?=.*\d)(?=.*[!@#$%^])[a-zA-Z\d!@#$%^]+$',
            message='Пароль должен состоять из букв, чисел, и специальных символов!'
        )
    ])
    is_active = models.BooleanField(
        _("active"),
        default=False,
        help_text=_(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )
    activation_code = models.CharField(max_length=300, blank=True)

    objects = MyUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def create_activation_code(self):
        code = str(uuid.uuid4())
        print(code, 'code from models')
        self.activation_code = code
        self.save()

    def __str__(self):
        return f'{self.email}'

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

