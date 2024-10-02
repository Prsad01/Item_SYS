from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from .models import Item
from django.contrib.auth.models import User
from decimal import Decimal
from rest_framework_simplejwt.tokens import RefreshToken

class ItemTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.accesstoken = RefreshToken.for_user(self.user).access_token

        self.create_data = {
            "name": "Item1",
            "description": "Description for Item1",
            "quantity": 10,
            "price": 99.99,
            }
        self.item = Item.objects.create(**self.create_data)
        self.url= reverse('item-detail' ,args=[self.item.id])
        self.create_url = reverse('item-list')
    def test_single_item(self):

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + str(self.accesstoken))
        response = self.client.get(self.url)
        
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.item.name)

    def test_list_item(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + str(self.accesstoken))
        response = self.client.get(reverse('item-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_item(self):
        new_create_data = {
            "name": "Item11",
            "description": "Description for Item1",
            "quantity": 10,
            "price": 99.99,
            }
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + str(self.accesstoken))
        response = self.client.post(self.create_url,new_create_data,format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_put_item(self):
        updated_data = {
             "name": "Updated Item1",
            "description": "updatedDescription for Item1",
            "quantity": 15,
            "price": Decimal('100.99'),
        }
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + str(self.accesstoken))
        response = self.client.put(self.url,updated_data,format='json')
        self.assertEqual(response.status_code,  status.HTTP_200_OK)
        self.item.refresh_from_db()
        self.assertEqual(self.item.name,  updated_data['name'])
        self.assertEqual(self.item.price,   Decimal('100.99'))
        self.assertEqual(self.item.quantity,15)

    def test_path_item(self):
        updated_data = {
            "quantity": 10
        }
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + str(self.accesstoken))
        response = self.client.patch(self.url,updated_data,format='json')
        self.assertEqual(response.status_code,  status.HTTP_200_OK)
        self.item.refresh_from_db()
        self.assertEqual(self.item.quantity,10)

    def test_destroy_item(self):
        self.assertEqual(Item.objects.count(), 1)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + str(self.accesstoken))
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Item.objects.count(), 0)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)