from django.contrib import admin
from .models import Shipping


class ShippingAdmin(admin.ModelAdmin):

    list_display = (
        'method',
        'price',
        'delivery_time',
        'processing_time',
    )


admin.site.register(Shipping, ShippingAdmin)
