from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from apps.excursions.models import Excursion

User = get_user_model()


class ExcursionTests(APITestCase):

    def setUp(self):
        self.admin = User.objects.create_user(
            username="admin",
            password="admin123",
            is_staff=True
        )

        # This is the fix:
        self.client.force_authenticate(user=self.admin)

        # Create one excursion
        self.excursion = Excursion.objects.create(
            title="Old City Walk",
            location="Bukhara",
            duration_hours=2,
            price=25.50,
            description="A walk through the ancient city.",
            is_available=True
        )

        self.list_url = reverse("excursions:excursion-list")
        self.create_url = reverse("excursions:excursion-create")
        self.detail_url = reverse("excursions:excursion-detail", args=[self.excursion.id])
        self.update_url = reverse("excursions:excursion-update", args=[self.excursion.id])
        self.delete_url = reverse("excursions:excursion-delete", args=[self.excursion.id])


    # ----------------------------
    # LIST TEST
    # ----------------------------
    def test_list_excursions(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    # ----------------------------
    # CREATE TEST
    # ----------------------------
    def test_create_excursion_as_admin(self):
        data = {
            "title": "Mountain Adventure",
            "location": "Tian Shan",
            "duration_hours": 6,
            "price": 80.00,
            "description": "High-altitude trekking with a guide.",
            "is_available": True
        }

        response = self.client.post(self.create_url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Excursion.objects.count(), 2)

    # ----------------------------
    # DETAIL TEST
    # ----------------------------
    def test_excursion_detail(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "Old City Walk")

    # ----------------------------
    # UPDATE TEST (PUT)
    # ----------------------------
    def test_update_excursion_as_admin(self):
        data = {
            "title": "Updated City Walk",
            "location": "Samarkand",
            "duration_hours": 3,
            "price": 30.00,
            "description": "Updated description.",
            "is_available": True
        }

        response = self.client.put(self.update_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.excursion.refresh_from_db()
        self.assertEqual(self.excursion.title, "Updated City Walk")

    # ----------------------------
    # PARTIAL UPDATE TEST (PATCH)
    # ----------------------------
    def test_patch_excursion(self):
        data = {
            "price": 45.00
        }

        response = self.client.patch(self.update_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.excursion.refresh_from_db()
        self.assertEqual(float(self.excursion.price), 45.00)

    # ----------------------------
    # DELETE TEST
    # ----------------------------
    def test_delete_excursion_as_admin(self):
        response = self.client.delete(self.delete_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Excursion.objects.count(), 0)
