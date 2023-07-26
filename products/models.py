from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=254)
    friendly_name = models.CharField(max_length=254, null=True, blank=True)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name

    def get_friendly_name(self):
        return self.friendly_name


class Product(models.Model):
    category = models.ForeignKey('Category', null=True, blank=True, on_delete=models.SET_NULL)
    sku = models.CharField(max_length=254, null=True, blank=True)
    name = models.CharField(max_length=254)
    description = models.TextField()    
    price = models.DecimalField(max_digits=6, decimal_places=2)    
    image_url = models.URLField(max_length=1024, null=True, blank=True)
    image = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.name
    
    def get_rating(self):
        """ Calculate average product rating """
        total_rating = 0

        for review in self.reviews.all():
            total_rating += review.rating

        if total_rating > 0:
            return total_rating / self.reviews.count()
        else:
            return 0



class Reviews(models.Model):
    product = models.ForeignKey(Product, related_name='reviews', on_delete=models.CASCADE)
    comment = models.TextField(max_length=500, null=True, blank=True)
    rating = models.IntegerField()
    created_by = models.ForeignKey(User, related_name='reviews', on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.product.name
    
    class Meta:
        verbose_name_plural = 'Reviews'
        ordering = ['-created_on']
