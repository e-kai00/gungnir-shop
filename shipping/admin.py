from django.contrib import admin
from .models import Shipping


class ShippingAdmin(admin.ModelAdmin):

    list_display = (
        'method',
        'price',
        'delivery_time_min',
        'delivery_time_max',
        'processing_time',
    )


admin.site.register(Shipping, ShippingAdmin)
