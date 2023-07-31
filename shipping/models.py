from django.db import models
from datetime import datetime, timedelta


class Shipping(models.Model):

    method = models.CharField(max_length=50, default='Standard')
    price = models.DecimalField(max_digits=6, decimal_places=2)    
    delivery_time_min = models.PositiveIntegerField(default=10)
    delivery_time_max = models.PositiveIntegerField(default=21)                              
    processing_time = models.PositiveIntegerField(default=1)


    def __str__(self):
        return f"${self.price} {self.method}"


    def estimated_delivery(self):  
        
        today = datetime.now().date()       
        
        min_estimated_delivery = today + timedelta(days=self.delivery_time_min + self.processing_time)
        max_estimated_delivery = today + timedelta(days=self.delivery_time_max + self.processing_time)
        estimated_delivery_range = f'{min_estimated_delivery.strftime("%d %b")} - {max_estimated_delivery.strftime("%d %b")}'

        return estimated_delivery_range
    

    def order_dispatch(self):

        today = datetime.now().date()
        dispatch_date = today + timedelta(days=self.processing_time)
        return dispatch_date.strftime("%d %b")


