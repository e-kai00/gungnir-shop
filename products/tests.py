from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.contrib.messages import get_messages
from django.urls import reverse
from .forms import ProductForm
from .models import Product 
from .views import (
    product_detail, 
    add_product, 
    edit_product, 
    delete_product, 
    submit_review
    )


class ProductViewTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='password'
        )
        self.client = Client()
        self.product = Product.objects.create(
            name='Test Product', 
            description='Test description', 
            price=10.99
            )


    def test_product_detail(self):
        response = self.client.get(reverse('product_detail', args=[self.product.id]))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'products/product_detail.html')
        self.assertEqual(response.context['product'], self.product)


class SubmitReviewTest(TestCase):
    pass