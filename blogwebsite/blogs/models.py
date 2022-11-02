from email.policy import default
from django.db import models
from django.contrib.auth.models import AbstractUser
from taggit.managers import TaggableManager

# Create your models here.
class User(AbstractUser):
    pass

class Blog(models.Model):
    id = models.BigAutoField(auto_created=True,primary_key=True)
    title = models.CharField(max_length=250)
    slug = models.SlugField(unique=True, max_length=100)
    date_added = models.DateField(auto_now_add=True)
    views = models.IntegerField(default=0)
    author = models.ForeignKey(
        User,
        models.SET_NULL,
        blank=True,
        null=True
    )
    tags = TaggableManager()

    def __str__(self):
        return str(self.id)+" "+self.title
