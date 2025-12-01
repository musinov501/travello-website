from django.db import models
from apps.users.models.user_auth import BaseModel



class Excursion(BaseModel):
    STATUS_CHOICES = (
        (True, 'Active'),
        (False, 'Inactive'),
    )
    
    
    title = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    duration_hours = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    image = models.ImageField(upload_to='excursions/images/', null=True, blank=True)
    is_available = models.BooleanField(choices=STATUS_CHOICES, default=True)
    
    
    def __str__(self):
        return f"{self.title} - {self.location}"
    
    
    class Meta:
        verbose_name = "Excursion"
        verbose_name_plural = "Excursions"
        ordering = ['title']
   