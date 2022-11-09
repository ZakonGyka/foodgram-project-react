from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.exceptions import ValidationError


# class User(AbstractUser):
#     username_validator = UnicodeUsernameValidator()
#     username = models.CharField(
#         max_length=200,
#         unique=True,
#         help_text='Макс. длина 200 символов',
#         validators=[username_validator],
#         error_messages={
#             'unique': 'Этот никнейм уже используется'
#         },
#     )
