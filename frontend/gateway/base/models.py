from django.db import models

# Create your models here.


class UserModel(models.Model):
    user_id = models.IntegerField()
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)