from django.test import TestCase
from .models import *
from .views import *


class TestLogin(TestCase):
    """
    test basic user login functionality
    """

    @classmethod
    def setUpTestData(cls):
        cls.test_user = User.objects.create(username='testuser')
        cls.test_user.set_password('t1t1t1t1')
        cls.test_user.save()

    def test_login_bad_user(self):
        logged_in = self.client.login(username='testuser', password='12345')  # login with bad password
        self.assertFalse(logged_in)  # make sure login failed
        logged_in = self.client.login(username='testuser222', password='t1t1t1t1')  # login with bad username
        self.assertFalse(logged_in)  # make sure login failed
        url = reverse('budget:user_settings')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)  # get authentication error for bad user

    def test_login_good_user(self):
        logged_in = self.client.login(username='testuser', password='t1t1t1t1')
        self.assertTrue(logged_in)  # make sure login succeeded
        url = reverse('budget:user_settings')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)  # successfully enter user settings page

    def test_logout(self):
        logged_in = self.client.login(username='testuser', password='t1t1t1t1')
        self.assertTrue(logged_in)  # make sure login succeeded
        self.client.logout()
        url = reverse('budget:user_settings')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)  # get authentication error


class TestTransaction(TestCase):
    """
    tests precondition and post save actions for transaction addition
    """

    def test_precondition_invalid_transaction(self):
        pass

    def test_precondition_valid_transaction(self):
        pass

    def test_envelope_update(self):
        pass
