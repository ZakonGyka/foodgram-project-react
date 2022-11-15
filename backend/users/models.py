from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.exceptions import ValidationError
from django.db import models


class User(AbstractUser):
    username_validator = UnicodeUsernameValidator()
    email = models.EmailField(
        verbose_name='Адрес электронной почты',
        blank=False,
        unique=True,
        max_length=150,
        error_messages={
            'unique': 'Такой адрес электронной почты уже зарегистрирован.'
        },
    )
    username = models.CharField(
        verbose_name='Логин',
        max_length=150,
        unique=True,
        validators=[username_validator],
        error_messages={
            'unique': 'Пользователь с таким логином уже зарегистрирован.'
        },
    )
    first_name = models.CharField(verbose_name='Имя', max_length=150)
    last_name = models.CharField(verbose_name='Фамилия', max_length=150)
    is_superuser = models.BooleanField(default=False) # можено попробовать убрать
    is_active = models.BooleanField(default=True) # можено попробовать убрать
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']
    USERNAME_FIELD = 'email'

    @property
    def is_admin(self):
        return self.is_superuser

    def get_full_name(self):
        return f'{self.first_name} + {self.last_name}'

    def get_short_name(self):
        return f'{self.username[:15]}'

    def __str__(self):
        return self.username

    class Meta:
        ordering = ('username',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class Follow(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower',
        verbose_name='Подписчик',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following',
        verbose_name='Автор'
    )

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        constraints = [
            models.UniqueConstraint(
                fields=('user', 'author'),
                name='unique_user_follow'
            )
        ]
