from django.db import models

# Create your models here.

from django.db import models
from django.contrib.auth.models import AbstractUser

class Employee(AbstractUser):
    phone_number = models.CharField(max_length=255, blank=False, null=False)
    
    def __str__(self):
        return self.username
    
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name
    
class Client(models.Model):
    first_name = models.CharField(max_length=255, blank=False, null=False)
    last_name = models.CharField(max_length=255, blank=False, null=False)
    phone_number = models.CharField(max_length=255, blank=True)
    email = models.EmailField(blank=False, null=False)
    details = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    categories = models.ManyToManyField(
        Category,
        through='ClientCategory',
        related_name='clients'
    )

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class ClientCategory(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.client} in {self.category}"