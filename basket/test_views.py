from django.test import TestCase, RequestFactory
from django.contrib.auth.models import User
from django.contrib.sessions.middleware import SessionMiddleware
from django.contrib.messages.middleware import MessageMiddleware
from django.contrib.messages import get_messages
from .views import add_to_basket, update_basket, remove_from_basket
from products.models import Product
from django.urls import reverse


class BasketTest(TestCase):
    """
    Test cases for the basket functionality.

    This class provides test methods to verify the behavior 
    of the basket-related functions: adding, updating, and 
    removing items from the basket.
    """
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

        session_data = dict(request.session)
        messages = list(get_messages(request))

        # print(f'Session structure: {session_data}')
        # print(request.session['basket'])
        # print(request.session['basket'][self.product.pk])

        self.assertEqual(response.status_code, 302)
        self.assertEqual(len(request.session['basket']), 1)
        self.assertEqual(request.session['basket'][self.product.pk], 2)
        self.assertEqual(messages[0].level, 25) # SUCCESS
        self.assertIn(f'{self.product.name} added to basket', messages[0].message)


    def test_update_basket(self):

        request = self.factory.post(
            reverse('update_basket', args=[self.product.pk]),
            {'quantity': 3}
        )

        session_middleware = SessionMiddleware()
        session_middleware.process_request(request)
        request.session.save()

        request.user = self.user

        message_middleware = MessageMiddleware()
        message_middleware.process_request(request)

        response = update_basket(request, self.product.pk)

        messages = list(get_messages(request))
        expected_redirect_url = reverse('view_basket')  
        session_data = dict(request.session)

        # print(f'Session structure: {session_data}')
        # print(f'Message level: {messages[0].level}')
        # print(f'Message msg: {messages[0].message}')
        # print(f'Response object: {(str(response))}')
        
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, expected_redirect_url)
        self.assertEqual(request.session['basket'][self.product.pk], 3)
        self.assertEqual(messages[0].level, 25) # SUCCESS
        self.assertIn(f'{self.product.name} updated to 3', messages[0].message)


    def test_remove_from_basket(self):
        
        request = self.factory.get(
            reverse('remove_from_basket', args=[self.product.pk]),
        )
       
        session_middlewar = SessionMiddleware()
        session_middlewar.process_request(request)
        request.session.save()

        # attach product
        request.session['basket'] = {self.product.pk: 1}

        request.user = self.user

        message_middleware = MessageMiddleware()
        message_middleware.process_request(request)

        response = remove_from_basket(request, self.product.pk)

        messages = list(get_messages(request))
       
        self.assertNotIn(self.product.pk, request.session.get('basket', {}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(messages[0].level, 25) # SUCCESS
        self.assertIn(f'{self.product.name} removed from basket', messages[0].message)
