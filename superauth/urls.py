from django.urls import path
from .APIs.auth import SuperAdminLogin, VerifySuperAdminOTP

urlpatterns = [
    path("login/", SuperAdminLogin.as_view()),
    path("otp-verify/", VerifySuperAdminOTP.as_view()),
]

    