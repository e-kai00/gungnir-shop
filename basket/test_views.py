from django.test import TestCase, RequestFactory, override_settings
from django.contrib.auth.models import AnonymousUser, User
from django.contrib.sessions.middleware import SessionMiddleware
from django.contrib.messages.middleware import MessageMiddleware
from .views import add_to_basket
from products.models import Product
from django.urls import reverse


class BasketTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username='test_user', password='test_pass'
        )
        self.product = Product.objects.create(name='Test product 1', price=10.00)


    def test_add_to_basket(self):
      
        request = self.factory.post(
            reverse('add_to_basket', args=[self.product.pk]),
            {'quantity': 2, 'redirect_url': '/'}
        )
        # set up session
        middleware = SessionMiddleware()
        middleware.process_request(request)
        request.session.save()
        # set up user
        request.user = self.user

        middleware_message = MessageMiddleware()
        middleware_message.process_request(request)

        response = add_to_basket(request, self.product.pk)        

        # print statements
        session_data = dict(request.session)
        print(f'Session structure: {session_data}')
        print(request.session['basket'])
        print(request.session['basket'][self.product.pk])

        self.assertEqual(response.status_code, 302)
        self.assertEqual(len(request.session['basket']), 1)
        self.assertEqual(request.session['basket'][self.product.pk], 2)