from django.db import models

# Create your models here.


class Post(models.Model):
    message = models.TextField()
    