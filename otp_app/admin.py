from django.contrib import admin
from .models import OTP

@admin.register(OTP)
class OTPAdmin(admin.ModelAdmin):
    list_display = ['user', 'otp_code', 'expires_at', 'verified']
    search_fields = ['user__email', 'otp_code']

