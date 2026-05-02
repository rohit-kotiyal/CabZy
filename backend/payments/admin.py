from django.contrib import admin
from .models import Payment, PromoCode



@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['id', 'ride', 'amount', 'method', 'status', 'created_at']
    list_filter = ['status', 'method']


@admin.register(PromoCode)
class PromoCodeAdmin(admin.ModelAdmin):
    list_display = ['code', 'discount_pct', 'max_uses', 'used_count', 'is_active', 'expires_at']


