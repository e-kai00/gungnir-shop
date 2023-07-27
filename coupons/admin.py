from django.contrib import admin
from .models import Coupon


class CouponAdmin(admin.ModelAdmin):

    list_display = ['code', 'value', 'valid_from', 'expire_on', 'active']
    list_filter = ['active', 'valid_from', 'expire_on']
    search_fields = ['code']

admin.site.register(Coupon, CouponAdmin)
