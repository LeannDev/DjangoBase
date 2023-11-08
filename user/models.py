from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):

    premium = models.BooleanField(default=False)

    def __str__(self):
        return  f'User: {self.username}'