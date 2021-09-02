from rest_framework import response
from .models import Token
from django.urls import reverse
from rest_framework.test import APIClient, APITestCase
# Create your tests here.

class AuthTestCase(APITestCase):
    def setUp(self) -> None:
        self.client = APIClient()

        self.login_url = reverse('login')
        self.register_url = reverse('register')
        self.confirmation_url = reverse('confirmation')
        self.data = {
            "email": "johndoe@gmail.com",
            "first_name": "John",
            "last_name": "DOE",
            "password": "Jom5366@gh"
        }

    def register(self):
        response = self.client.post(self.register_url, data= self.data)
        return self.assertEqual(response.status_code, 201)
    
    def activate_account(self):
        token = Token.objects.get(user__username= self.data['email'])

        response = self.client.post(self.confirmation_url, data={'digest': token.digest})

        return self.assertEqual(response.status_code, 200)

    def activate_account_with_bad_digest(self):
        response = self.client.post(self.confirmation_url, data={'digest': 478596333})

        return self.assertEqual(response.status_code, 400)

    def test_bad_register(self):
        data = {**self.data}
        data.pop('email')
        response = self.client.post(self.register_url, data= data)
        return self.assertEqual(response.status_code, 400)

    def login(self):
        response = response = self.client.post(self.login_url, data= {
            "username": "johndoe@gmail.com",
            "password": "Jom5366@gh"
        })
        return self.assertEqual(response.status_code, 200)

    def login_with_bad_credentials(self):
        response = response = self.client.post(self.login_url, data= {
            "username": "johndoe@gmail.com",
            "password": "Jom536"
        })
        return self.assertEqual(response.status_code, 400)