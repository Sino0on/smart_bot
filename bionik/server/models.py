from django.db import models
from django.contrib.auth.models import AbstractUser


class Account(AbstractUser):
    name = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    tg = models.CharField(max_length=100)
    age = models.DateField(blank=True, null=True)
    rank = models.IntegerField(default=1)

    def __str__(self):
        return self.username
