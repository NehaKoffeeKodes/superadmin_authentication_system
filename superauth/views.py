from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from .models import CustomUser
from superauth.authentication.superadmin_authentication import JWTAuthentication
from .permissions.superadmin_permission import IsSuperAdmin
from .authentication.jwt import create_jwt
from .utils.send_qr_to_email_utils import send_qr_email 
import pyotp
import qrcode
import io



