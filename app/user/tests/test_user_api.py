from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status


CREATE_USER_URL = reverse('user:create')
TOKEN_URL = reverse('user:token')
print("Create User Url")
print(CREATE_USER_URL)

def create_user(**params):
    print("**Create User Params***")
    for p in params:
        print(p)
    print(params.items())
    return get_user_model().objects.create_user(**params)


class PublicUserApiTests(TestCase):
    """Test the user api (public)"""

    def setUp(self):
        self.client = APIClient()

    def test_create_valid_user_success(self):
        """Test creating user with valid payload is successful"""
        payload = {
            'email': 'glory@dev.com',
            'password': 'glory',
            'name': 'Ko Ko Pyae Sone'
        }    
        res = self.client.post(CREATE_USER_URL, payload)
        print("Post user success")
        print(res)
        print("data")
        print(res.data)
        

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(**res.data)
        print("***User***")
        print(user)
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', res.data)

    def test_user_exitsts(self):
        """Test creating user that already exists fails"""
        payload = {'email': 'glory@dev.com','password': 'testpass'}     
        create_user(**payload)

        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short(self):
        """Test that the password must be more than 5 characters"""
        payload = {'email': 'glory@dev.com','password': 'pw'}
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(
            email = payload['email']
        ).exists()
        self.assertFalse(user_exists)

    def test_create_token_for_user(self):
        """Test that a token is created for the user"""
        payload = {'email': 'glory@dev.com', 'password': 'glory'}
        create_user(**payload)
        res = self.client.post(TOKEN_URL, payload)

        self.assertIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK) 

    def test_create_token_invalid_credentials(self):
        """Test that token is not created if invalid credentials are given"""
        create_user(email='glory@dev.com', password = 'glory')
        payload = {'email': 'glory@dev.com', 'password': 'wrong'}
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_no_user(self):
        """Test that token is not created if user doesn't exist"""
        payload = {'email': 'glory@dev.com', 'password': 'glory'}
        res = self.client.post(TOKEN_URL, payload)
        print("***No User***")
        print(res.data)
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_missing_field(self):
        """Test the email and password are required"""
        res = self.client.post(TOKEN_URL, {'email': 'one', 'password':'a'})
        print('**Token Missing Fields**')
        print(res.data)
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)


        
