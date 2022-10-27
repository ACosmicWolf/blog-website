from email.policy import default
from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    pass

class Blog(models.Model):
    id = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=80)
    date_added = models.DateField()
    views = models.IntegerField(default=0)
    author = models.ForeignKey(
        User,
        models.SET_NULL,
        blank=True,
        null=True
    )
