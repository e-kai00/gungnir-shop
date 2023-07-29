from django.db import models

from django.contrib.postgres.fields import DateRangeField
from datetime import datetime, timedelta


class Shipping(models.Model):

    method = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=6, decimal_places=2) 
    delivery_time = DateRangeField()
    processing_time = models.PositiveBigIntegerField(default=1)


    def __str__(self):
        return self.method


    def estimated_delivery(self):
        
        today = datetime.now().date()
        estimated_delivery_time = today + timedelta(days=self.delivery_time + self.processing_time)
        return estimated_delivery_time


