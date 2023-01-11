from django.db import models

# Create your models here.
class user(models.Model):
    username=models.CharField(name="user_name", max_length=20)
    password=models.CharField(name="password", max_length=20)