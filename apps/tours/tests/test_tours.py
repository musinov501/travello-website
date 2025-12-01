from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from apps.tours.models.tours import Tour
from apps.users.models.user_auth import User


class TourTests(APITestCase):

    def setUp(self):
        # Admin user
        self.admin_user = User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='AdminPass123!'
        )

        # Regular user
        self.user = User.objects.create_user(
            username='user',
            email='user@example.com',
            password='UserPass123!'
        )

        # Sample tour
        self.tour = Tour.objects.create(
            title='Amazing Tour',
            destination='Paris',
            duration_days=5,
            price=1000,
            capacity=10,
            status=True
        )

        # URLs
        self.list_url = reverse('tours:list')
        self.detail_url = reverse('tours:detail', kwargs={'pk': self.tour.id})
        self.create_url = reverse('tours:create')
        self.update_url = reverse('tours:update', kwargs={'pk': self.tour.id})
        self.delete_url = reverse('tours:delete', kwargs={'pk': self.tour.id})

        # Sample data for creating/updating
        self.tour_data = {
            'title': 'Updated Tour',
            'destination': 'London',
            'duration_days': 7,
            'price': 1200,
            'capacity': 15,
            'status': True,
            "description": "A wonderful experience in Paris."
        }

    def test_list_tours(self):
        """Anyone can list tours"""
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data) > 0)

    def test_retrieve_tour(self):
        """Anyone can retrieve a tour"""
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], self.tour.id)

    def test_create_tour_as_admin(self):
        """Admin can create a tour"""
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.post(self.create_url, self.tour_data, format='json')
        print(response.data)  
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['title'], self.tour_data['title'])

    def test_create_tour_as_non_admin(self):
        """Non-admin cannot create a tour"""
        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.create_url, self.tour_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_tour_as_admin(self):
        """Admin can update a tour"""
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.put(self.update_url, self.tour_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.tour_data['title'])

    def test_update_tour_as_non_admin(self):
        """Non-admin cannot update a tour"""
        self.client.force_authenticate(user=self.user)
        response = self.client.put(self.update_url, self.tour_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_tour_as_admin(self):
        """Admin can delete a tour"""
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.delete(self.delete_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_tour_as_non_admin(self):
        """Non-admin cannot delete a tour"""
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(self.delete_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
