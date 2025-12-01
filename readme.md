SuperAdmin Authentication System

Project Overview
A secure and production-ready SuperAdmin login system with:

• Username + Password login  
• First-time Google Authenticator 2FA setup (QR code sent via email)  
• Secure JWT tokens (Temporary → Final long-lived)  
• Beautiful HTML emails for OTP & QR code  
• Proper validation, error handling and logging  

Base URL:-
http://127.0.0.1:8000/

1. SuperAdmin Login (Step 1)

URL          : /superadmin/login/
Method       : POST

Request :-
{
    "username": "admin",
    "password": "your_password"
}

Required     : username, password

Success :-
{
    "message": "First time login! QR code has been sent to your email. Please scan it using Google Authenticator.",
    "temporary_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.xxxx",
    "setup_2fa": true
}

Success (2FA Already Set Up)
{
    "message": "Please enter the 6-digit code from Google Authenticator.",
    "temporary_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.xxxx",
    "setup_2fa": false
}

Failed
{ "error": "Invalid credentials." }

Description:
Checks username/password → if first time → generates TOTP secret → sends QR code email → returns temporary token (10 min)


2. Verify OTP & Get Final Token (Step 2)

URL          : /superadmin/otp-verify/
Method       : POST
Header       : Authorization: Bearer <temporary_token>

Request:-
{
    "otp": "483920"
}

Required     : otp (6 digits)

Success:-
{
    "status": "success",
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.xxxxxxxxxx",
    "message": "Welcome back, SuperAdmin!",
    "user": {
        "name": "Neha Nimje",
        "email": "nehanimje2004@gmail.com"
    }
}

Failed:-
{ "error": "Invalid or expired OTP. Please try again." }

Description
Verifies 6-digit code from Google Authenticator → issues final access token (24 hours)


Security Features used:

• Custom JWT with user_id + expiry  
• Temporary token (10 min) → Final token (24 hours)  
• Google Authenticator compatible TOTP  
• QR code sent via secure branded email  
• All inputs validated  
• Try-except + proper logging  
• Only is_superuser users allowed  
• OTP expiry & one-time use  

Models Used :-

CustomUser    -   stores totp_secret, email, etc.



