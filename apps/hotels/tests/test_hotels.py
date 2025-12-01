from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from apps.hotels.models.hotels import Hotel
from apps.users.models.user_auth import User


class HotelTests(APITestCase):

    def setUp(self):
        # URLs
        self.list_url = reverse('hotels:hotel-list')
        self.create_url = reverse('hotels:hotel-create')

        # Admin user
        self.admin_user = User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='AdminPassword123!'
        )

        # Normal user
        self.normal_user = User.objects.create_user(
            username='user',
            email='user@example.com',
            password='UserPassword123!'
        )

        # Hotel data
        self.hotel_data = {
            'name': 'Test Hotel',
            'location': 'Test City',
            'rating': 4.5,
            'description': 'A nice hotel',
            'price_per_night': 150.00,
            'available_rooms': 10,
            'is_available': True,
            'has_wifi': True,
            'has_pool': False,
            'has_breakfast': True,
            'has_parking': True,
        }

        # Create a hotel for update/retrieve/delete tests
        self.hotel = Hotel.objects.create(**self.hotel_data)

    def test_list_hotels(self):
        """Anyone can list hotels"""
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_hotel(self):
        """Anyone can retrieve hotel details"""
        url = reverse('hotels:hotel-detail', args=[self.hotel.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_hotel_as_admin(self):
        """Admin can create a hotel"""
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.post(self.create_url, self.hotel_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_hotel_as_non_admin(self):
        """Non-admin cannot create a hotel"""
        self.client.force_authenticate(user=self.normal_user)
        response = self.client.post(self.create_url, self.hotel_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_hotel_as_admin(self):
        """Admin can update a hotel"""
        self.client.force_authenticate(user=self.admin_user)
        url = reverse('hotels:hotel-update', args=[self.hotel.id])
        response = self.client.put(url, {
            'name': 'Updated Hotel',
            'location': 'Updated City',
            'rating': 5.0,
            'description': 'Updated description',
            'price_per_night': 200.00,
            'available_rooms': 8,
            'is_available': True,
            'has_wifi': True,
            'has_pool': True,
            'has_breakfast': True,
            'has_parking': False,
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_hotel_as_non_admin(self):
        """Non-admin cannot update a hotel"""
        self.client.force_authenticate(user=self.normal_user)
        url = reverse('hotels:hotel-update', args=[self.hotel.id])
        response = self.client.put(url, self.hotel_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_hotel_as_admin(self):
        """Admin can delete a hotel"""
        self.client.force_authenticate(user=self.admin_user)
        url = reverse('hotels:hotel-delete', args=[self.hotel.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_hotel_as_non_admin(self):
        """Non-admin cannot delete a hotel"""
        self.client.force_authenticate(user=self.normal_user)
        url = reverse('hotels:hotel-delete', args=[self.hotel.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
