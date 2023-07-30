from django.db import models
from django.contrib.postgres.fields import IntegerRangeField
from datetime import datetime, timedelta


class Shipping(models.Model):

    method = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    delivery_time = IntegerRangeField(default=[10,21])                                 
    processing_time = models.IntegerField(default=1)


    def __str__(self):
        return self.method


    def estimated_delivery(self):  
        
        today = datetime.now().date()
        min_time_delivery, max_time_delivery = self.delivery_time.lower, self.delivery_time.upper
        
        min_estimated_delivery = today + timedelta(days=min_time_delivery + self.processing_time)
        max_estimated_delivery = today + timedelta(days=max_time_delivery + self.processing_time)
        estimated_delivery_range = f'{min_estimated_delivery} - {max_estimated_delivery}'

        return estimated_delivery_range


