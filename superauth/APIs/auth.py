from ..views import *

class SuperAdminLogin(APIView):
    """
    Handles SuperAdmin login.
    - Validates username & password
    - If first time → generates TOTP secret, sends QR code via email
    - Returns a temporary JWT (10 min) for OTP verification
    """
    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request):
        username = request.data.get("username", "").strip()
        password = request.data.get("password", "")

        if not username or not password:
            return Response({"error": "Username and password are required."},status=status.HTTP_400_BAD_REQUEST)

        try:
            user = CustomUser.objects.get(username=username)
        except CustomUser.DoesNotExist:
            return Response({"error": "Invalid credentials."},status=status.HTTP_401_UNAUTHORIZED)

        if not user.check_password(password):
            return Response(
                {"error": "Invalid credentials."},status=status.HTTP_401_UNAUTHORIZED)

        token = create_jwt(user, expire_minutes=10)

        if not user.totp_secret:
            try:
                secret = pyotp.random_base32()
                user.totp_secret = secret
                user.save(update_fields=["totp_secret"])

                uri = pyotp.TOTP(secret).provisioning_uri(name=username, issuer_name="SuperAdmin")
                qr = qrcode.make(uri)

                buffer = io.BytesIO()
                qr.save(buffer, format='PNG')
                qr_bytes = buffer.getvalue()
                buffer.close()

                send_qr_email(user.email, qr_bytes)

                return Response({
                    "message": "QR code has been sent to your email. Please scan it with Google Authenticator.",
                    "token": token,
                    "setup_2fa": True
                }, status=status.HTTP_200_OK)

            except Exception as e:
                return Response({"error": "Failed to setup 2FA. Please try again later."},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({
            "message": "Please enter the OTP.",
            "token": token,
            "setup_2fa": False
        }, status=status.HTTP_200_OK)


class VerifySuperAdminOTP(APIView):
    """
    Verifies the 6-digit OTP sent by Google Authenticator.
    - Uses temporary JWT from SuperAdminLogin
    - On success → issues long-lived access token (24 hours)
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsSuperAdmin]

    def post(self, request):
        user = request.user
        otp = request.data.get("otp", "").strip()

        if not otp or len(otp) != 6 or not otp.isdigit():
            return Response({"error": "Please provide a valid 6-digit OTP."},status=status.HTTP_400_BAD_REQUEST)

        if not user.totp_secret:
            return Response({"error": "2FA is not set up for this account."},status=status.HTTP_400_BAD_REQUEST)

        try:
            totp = pyotp.TOTP(user.totp_secret)
            if totp.verify(otp, valid_window=1):
                final_token = create_jwt(user, expire_minutes=1440)  

                return Response({
                    "status": "success",
                    "access_token": final_token,
                    "message": "Welcome back, SuperAdmin!",
                    "user": {
                        "name": user.get_full_name() or user.username,
                        "email": user.email,
                        "username": user.username
                    }
                }, status=status.HTTP_200_OK)

            else:
                return Response({"error": "Invalid or expired OTP."},status=status.HTTP_401_UNAUTHORIZED)

        except Exception as e:
            return Response({"error": "An error occurred during OTP verification."},status=status.HTTP_500_INTERNAL_SERVER_ERROR)