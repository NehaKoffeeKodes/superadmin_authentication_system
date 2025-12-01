from rest_framework import serializers
from django.contrib.auth import authenticate


class SuperAdminLoginSerializer(serializers.Serializer):
    """
    Validates SuperAdmin login credentials.
    - Checks if username & password are correct
    - Ensures the user has is_active = True
    - Ensures the user has is_superuser = True
    - Attaches authenticated user to validated data
    Used in SuperAdmin login API before proceeding to 2FA/OTP step.
    """
    username = serializers.CharField(
        required=True,
        max_length=150,
        error_messages={
            "required": "Username is required.",
            "blank": "Username cannot be empty.",
            "max_length": "Username is too long."
        }
    )
    password = serializers.CharField(
        required=True,
        write_only=True,
        style={'input_type': 'password'},
        error_messages={
            "required": "Password is required.",
            "blank": "Password cannot be empty."
        }
    )

    def validate(self, data):
        username = data.get("username", "").strip()
        password = data.get("password", "")

        if not username or not password:
            raise serializers.ValidationError("Both username and password are required.")

        user = authenticate(username=username, password=password)
        if not user:
            raise serializers.ValidationError("Invalid username or password.")

        if not user.is_active:
            raise serializers.ValidationError("This account is deactivated.")

        if not user.is_superuser:
            raise serializers.ValidationError("Access denied. SuperAdmin privileges required.")

        data["user"] = user
        return data


class OTPVerifySerializer(serializers.Serializer):
    """
    Validates the 6-digit OTP entered by SuperAdmin during 2FA or email verification.
    Ensures OTP is exactly 6 digits and contains only numbers.
    Used in OTP verification endpoints.
    """
    otp = serializers.CharField(
        required=True,
        max_length=6,
        min_length=6,
        error_messages={
            "required": "OTP is required.",
            "invalid": "OTP must be a valid string.",
            "max_length": "OTP must be exactly 6 digits.",
            "min_length": "OTP must be exactly 6 digits."
        }
    )

    def validate_otp(self, value):
        otp = value.strip()
        if not otp.isdigit():
            raise serializers.ValidationError("OTP must contain only digits.")
        return otp

    def validate(self, data):
        otp = data.get("otp", "").strip()
        if len(otp) != 6 or not otp.isdigit():
            raise serializers.ValidationError("Please provide a valid 6-digit OTP.")
        return data