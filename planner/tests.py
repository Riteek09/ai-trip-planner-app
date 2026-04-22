from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .models import Trip


class PlannerTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass123')

    def test_home_page_loads(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

    def test_dashboard_requires_login(self):
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 302)

    def test_trip_str(self):
        trip = Trip.objects.create(
            user=self.user,
            destination='Goa',
            days=3,
            mood='relax',
            group_type='solo',
            budget=10000,
            itinerary='Sample itinerary',
        )
        self.assertIn('Goa', str(trip))
