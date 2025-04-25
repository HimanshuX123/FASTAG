from django.contrib import admin
from .models import UserProfile, Payment


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'mobile', 'email', 'vehicle_number', 'created_at')
    search_fields = ('first_name', 'last_name', 'mobile', 'email', 'vehicle_number')
    list_filter = ('gender', 'vehicle_type', 'created_at')
    readonly_fields = ('qr_code',)  # QR Code will be shown in admin panel

    def qr_code_display(self, obj):
        if obj.qr_code:
            return f'<img src="{obj.qr_code.url}" width="100"/>'
        return "No QR Code"

    qr_code_display.allow_tags = True


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('user', 'amount', 'transaction_id','created_at')
    search_fields = ('user__first_name', 'user__last_name', 'transaction_id')
    list_filter = ['created_at']
