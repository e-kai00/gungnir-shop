from django.contrib import admin
from .models import Product, Category, Reviews

class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'sku',
        'name',
        'category',
        'price',         
        'image',
    )

    ordering = ('sku',)

class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'friendly_name',
        'name',
    )

class ReviewsAdmin(admin.ModelAdmin):
    list_display = (
        'product',
        'rating',
        'created_by',
        'created_on',
    )

    list_filter = (        
        'rating',
    )


admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Reviews, ReviewsAdmin)