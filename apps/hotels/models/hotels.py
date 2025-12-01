from django.db import models
from apps.shared.models import BaseModel  # assuming you have a BaseModel with created_at, updated_at

class Hotel(BaseModel):
    STATUS_CHOICES = (
        (True, 'Active'),
        (False, 'Inactive'),
    )

    name = models.CharField(max_length=255, verbose_name="Hotel Name")
    location = models.CharField(max_length=255, verbose_name="Location")
    rating = models.DecimalField(max_digits=2, decimal_places=1, default = 0.0)
    description = models.TextField(blank=True, null=True, verbose_name="Description")
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2)
    available_rooms = models.PositiveIntegerField(default=0)
    is_available = models.BooleanField(default=True, choices=STATUS_CHOICES, verbose_name="Is Available")
    main_image = models.ImageField(upload_to='hotels/images/', blank=True, null=True, verbose_name="Main Image")
    
    
    has_wifi = models.BooleanField(default=False)
    has_pool = models.BooleanField(default=False)
    has_breakfast = models.BooleanField(default=False)
    has_parking = models.BooleanField(default=False)
    
    
    def __str__(self):
        return f"{self.name} - {self.location}"

    class Meta:
        db_table = 'hotels'
        verbose_name = 'Hotel'
        verbose_name_plural = 'Hotels'
        ordering = ['-created_at']


