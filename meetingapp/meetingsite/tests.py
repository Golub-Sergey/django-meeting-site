from django.test import TestCase, Client
from unittest.mock import Mock
from django.urls import reverse
from .views import BaseView, LoginView, ProfileView

# diagnostic tests
class TestViews(TestCase):

    # выполняет один раз при старте тестов
    fixtures = [
        'fixtures/users.json'
    ]

    # выполняет перед каждым тестом
    def setUp(self):
        self.client = Client()

    def test_base_page(self):
        response = self.client.get(reverse('base'))
        self.assertEqual(response.status_code, 200)

    def test_profile_page(self):
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 302)

    def test_create_profile_page(self):
        response = self.client.get(reverse('create_profile'))
        self.assertEqual(response.status_code, 302)
    
    def test_update_profile_page(self):
        response = self.client.get(reverse('update_profile'))
        self.assertEqual(response.status_code, 302)
    
    def test_update_user_page(self):
        response = self.client.get(reverse('update_user'))
        self.assertEqual(response.status_code, 302)

    def test_registrate_user_page(self):
        response = self.client.get(reverse('registration'))
        self.assertEqual(response.status_code, 200)
    
    def test_profile_page_loggedin(self):
        self.client.login(username='02', password='02')
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 200)

    def test_profile_page_loggedin_kwargs(self):
        self.client.login(username='02', password='02')
        response = self.client.get(reverse('profile'), data={'user_profile':'03'})
        self.assertEqual(response.status_code, 200)
    
    def test_create_profile_page_loggedin(self):
        self.client.login(username='02', password='02')
        response = self.client.get(reverse('create_profile'))
        self.assertEqual(response.status_code, 200)
    
    def test_update_profile_page_loggedin(self):
        self.client.login(username='02', password='02')
        response = self.client.get(reverse('update_profile'))
        self.assertEqual(response.status_code, 200)
    

    def test_update_user_page_loggedin(self):
        self.client.login(username='02', password='02')
        response = self.client.get(reverse('update_user'))
        self.assertEqual(response.status_code, 200)
