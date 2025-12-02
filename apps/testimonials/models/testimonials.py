from django.db import models
from apps.users.models.user_auth import BaseModel



class Testimonial(BaseModel):
    name = models.CharField(max_length=255)
    role = models.CharField(max_length=255)
    avatar = models.ImageField(upload_to='testimonials/avatars/', blank=True, null=True)
    text = models.TextField()
    is_published = models.BooleanField(default=True)
    
    
    def __str__(self):
        return f"{self.name} - {self.role or 'No role'}"
    
    
    class Meta:
        verbose_name = "Testimonial"
        verbose_name_plural = "Testimonials"
        ordering = ['-created_at']
        


    
    