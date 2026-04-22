from django.contrib import admin
from .models import Trip


@admin.register(Trip)
class TripAdmin(admin.ModelAdmin):
    list_display = ('destination', 'user', 'days', 'mood', 'group_type', 'budget', 'created_at')
    search_fields = ('destination', 'user__username', 'user__email')
    list_filter = ('mood', 'group_type', 'created_at')
