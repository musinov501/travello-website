from django.contrib.auth.models import AbstractUser
from django.db import models


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        abstract = True


class User(AbstractUser):
    phone = models.CharField(max_length=15, blank=True, null=True)
    
    REQUIRED_FIELDS = ['phone']
    
    def __str__(self):
        return self.username
    
    
    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        

 
