from django.contrib import admin
from .models import Review


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['id', 'ride', 'rated_by', 'rated_user', 'rating', 'created_at']
    list_filter  = ['rating']