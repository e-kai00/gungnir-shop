from django.test import TestCase, RequestFactory
from django.contrib.sessions.middleware import SessionMiddleware
from django.contrib.messages.middleware import MessageMiddleware
from django.contrib.messages import get_messages
from .models import Coupon
from .views import apply_coupon
from django.urls import reverse
from django.utils import timezone


class CouponTest(TestCase):
    """
    Test case for the coupon functionality.

    This test case verifies the behavior of the coupon-related views and logic.
    Methods:        
        1. test_apply_coupon: Test the application of a valid coupon code. It simulates 
        the application of a valid coupon code and verifies the expected behavior.
        2. test_apply_invalid_coupon: Test the handling of an invalid coupon code. 
        It simulates the application of an invalid coupon code and verifies the expected 
        error message.
    """

    def setUp(self):
        self.factory = RequestFactory()
        self.coupon = Coupon.objects.create(
            code='TESTCODE',
            value=10,
            valid_from=timezone.now(),
            expire_on=timezone.now() + timezone.timedelta(days=30),
            active=True
        )

        self.session_middleware = SessionMiddleware()
        self.message_middleware = MessageMiddleware()


    def test_apply_coupon(self):
        
        data = {'code': self.coupon.code}
        request = self.factory.post(
            reverse('apply_coupon'),
            data
        )

        self.session_middleware.process_request(request)
        self.message_middleware.process_request(request)
        request.session.save()

        response = apply_coupon(request)

        # print(request.session['coupon_id'])

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('view_basket'))
        self.assertEqual(request.session['coupon_id'], self.coupon.id)
        
    
    def test_apply_invalid_coupon(self):
                
        data = {'code': 'INVALIDCODE'}
        request = self.factory.post(
            reverse('apply_coupon'),
            data
        )

        self.session_middleware.process_request(request)
        self.message_middleware.process_request(request)
        request.session.save()

        response = apply_coupon(request)

        messages = list(get_messages(request))
        session_data = dict(request.session)

        # print(f'Message level: {messages[0].level}')
        # print(f'Session: {session_data}')

        self.assertIsNone(request.session['coupon_id'])
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('view_basket'))
        self.assertEqual(messages[0].level, 40) # ERROR
        self.assertIn(f'This coupon code does not exist.', messages[0].message)
               
        