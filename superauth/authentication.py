from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
import jwt
from django.conf import settings
from .models import CustomUser


class JWTAuthentication(BaseAuthentication):
    """
    Custom JWT Authentication class for DRF.
    Checks the 'Authorization: Bearer <token>' header,
    verifies the token and returns the authenticated user.
    Used to protect SuperAdmin routes.
    """
    
    def authenticate(self, request):
        auth_header = request.headers.get('Authorization')

        if not auth_header or not auth_header.startswith('Bearer '):
            return None  

        token = auth_header.split(' ')[1]

        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])

            user_id = payload.get('user_id')
            if not user_id:
                raise AuthenticationFailed('Invalid token: missing user ID')

            user = CustomUser.objects.get(id=user_id)
            return (user, token)

        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Token has expired. Please log in again.')
        
        except jwt.InvalidTokenError:
            raise AuthenticationFailed('Invalid token. Authentication failed.')
        
        except CustomUser.DoesNotExist:
            raise AuthenticationFailed('User not found or account deleted.')
        
        except Exception as e:
            raise AuthenticationFailed('Token verification failed. Please try again.')
        

