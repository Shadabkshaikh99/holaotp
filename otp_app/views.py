from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth.models import User
from .models import OTP
from .serializers import OTPSerializer
from django.utils import timezone
import random

class GenerateOTP(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        otp_code = str(random.randint(100000, 999999))
        expires_at = timezone.now() + timezone.timedelta(minutes=5)
        OTP.objects.create(user=user, otp_code=otp_code, expires_at=expires_at)
        # Here, you should send the OTP to the user's email or mobile number.
        return Response({"message": "OTP sent", "otp": otp_code}, status=status.HTTP_201_CREATED)

class VerifyOTP(APIView):
    def post(self, request):
        otp_code = request.data.get('otp_code')
        user = request.user
        try:
            otp = OTP.objects.get(user=user, otp_code=otp_code)
            if otp.is_expired():
                return Response({"message": "OTP expired"}, status=status.HTTP_400_BAD_REQUEST)
            otp.verified = True
            otp.save()
            return Response({"message": "OTP verified"}, status=status.HTTP_200_OK)
        except OTP.DoesNotExist:
            return Response({"message": "Invalid OTP"}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def otp_status(request):
    user = request.user
    try:
        otp = OTP.objects.filter(user=user).latest('expires_at')
        serializer = OTPSerializer(otp)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except OTP.DoesNotExist:
        return Response({"message": "No OTP found"}, status=status.HTTP_404_NOT_FOUND)
