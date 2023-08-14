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
        """
        Calculate estimated delivery range based on the 'delivery_time_min',
        'delivery_time_max', and 'processing_time' of the model instance.
        The delivery range is represented as string in the format
        "day month - day month", where the first day is the earliest estimated
        delivery and the second day is the latest estimated delivery date.
        """

        today = datetime.now().date()

        min_estimated_delivery = (
            today + timedelta(days=self.delivery_time_min +
                              self.processing_time)
        )
        max_estimated_delivery = (
            today + timedelta(days=self.delivery_time_max +
                              self.processing_time)
        )
        estimated_delivery_range = (
            f'{min_estimated_delivery.strftime("%d %b")} - '
            f'{max_estimated_delivery.strftime("%d %b")}'
        )

        return estimated_delivery_range

    def order_dispatch(self):
        """
        Calculate dispatch date based on 'processing_time' of the model
        instance. The dispatch date is represented as string in the
        format "day month".
        """

        today = datetime.now().date()
        dispatch_date = today + timedelta(days=self.processing_time)
        return dispatch_date.strftime("%d %b")
