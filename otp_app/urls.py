from django.urls import path
from .views import GenerateOTP, VerifyOTP, otp_status

urlpatterns = [
    path('generate-otp/', GenerateOTP.as_view(), name='generate-otp'),
    path('verify-otp/', VerifyOTP.as_view(), name='verify-otp'),
    path('otp-status/', otp_status, name='otp-status'),
]
