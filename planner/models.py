from django.contrib.auth.models import User
from django.db import models


class Trip(models.Model):
    MOOD_CHOICES = [
        ('relax', 'Relax'),
        ('adventure', 'Adventure'),
        ('romantic', 'Romantic'),
        ('family', 'Family'),
        ('cultural', 'Cultural'),
    ]

    GROUP_CHOICES = [
        ('solo', 'Solo'),
        ('friends', 'Friends'),
        ('couple', 'Couple'),
        ('family', 'Family'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='trips')
    destination = models.CharField(max_length=120)
    days = models.PositiveIntegerField()
    mood = models.CharField(max_length=20, choices=MOOD_CHOICES)
    group_type = models.CharField(max_length=20, choices=GROUP_CHOICES)
    budget = models.PositiveIntegerField(help_text='Budget in INR')
    itinerary = models.TextField()
    weather_info = models.TextField(blank=True)
    estimated_cost = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.destination} ({self.user.username})'
