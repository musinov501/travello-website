from django.db import models
from django.conf import settings
from apps.hotels.models import Hotel
from apps.tours.models import Tour
from apps.excursions.models import Excursion
from apps.shared.models import BaseModel

class Booking(BaseModel):
    STATUS_CHOICES = (
        ("pending", "Pending"),
        ("confirmed", "Confirmed"),
        ("canceled", "Canceled"),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

   
    hotel = models.ForeignKey(Hotel, null=True, blank=True, on_delete=models.CASCADE)
    tour = models.ForeignKey(Tour, null=True, blank=True, on_delete=models.CASCADE)
    excursion = models.ForeignKey(Excursion, null=True, blank=True, on_delete=models.CASCADE)

    check_in = models.DateField(null=True, blank=True)
    check_out = models.DateField(null=True, blank=True)

    guests = models.PositiveIntegerField(default=1)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")

    def __str__(self):
        return f"{self.user} booking"
