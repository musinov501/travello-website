from django.db import models
from apps.users.models.user_auth import BaseModel
from apps.hotels.models.hotels import Hotel



class Tour(BaseModel):
    TOUR_TYPE_CHOICES = [
        ('ADVENTURE', 'Adventure'),
        ('CULTURAL', 'Cultural'),
        ('LEISURE', 'Leisure'),
        ('OTHER', 'Other')
    ]
    
    title = models.CharField(max_length=255)
    description = models.TextField()
    destination = models.CharField(max_length=255)
    duration_days = models.PositiveIntegerField()
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    tour_type = models.CharField(max_length=20, choices=TOUR_TYPE_CHOICES, default='OTHER')
    capacity = models.PositiveIntegerField()
    hotel = models.ForeignKey(Hotel, on_delete=models.SET_NULL, null=True, blank=True, related_name='tours')
    image = models.ImageField(upload_to='tours/', null=True, blank=True)
    status = models.BooleanField(default=True)  

    def __str__(self):
        return self.title
    

    class Meta:
        verbose_name = 'Tour'
        verbose_name_plural = 'Tours'
        ordering = ['-created_at']
        
