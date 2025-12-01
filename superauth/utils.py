from django.core.mail import EmailMultiAlternatives
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

def send_qr_email(to_email: str, qr_image_bytes: bytes, role: str = "SuperAdmin") -> bool:
    """
    Sends a beautifully designed HTML email containing the 2FA QR code as an embedded image.
    Used during first-time SuperAdmin 2FA setup to securely deliver the QR code.
    Returns True on success, False on failure.
    """
    if not to_email or "@" not in to_email:
        logger.error(f"Invalid email: {to_email}")
        return False

    if not qr_image_bytes:
        logger.error("QR image bytes empty")
        return False

    subject = "SuperAdmin 2FA Setup – Scan QR Code"
    html_content = f"""
    <html>
    <body style="margin:0; padding:20px; font-family:Arial; background:#f4f9ff;">
        <div style="max-width:600px; margin:auto; background:white; border-radius:12px; padding:35px; box-shadow:0 6px 25px rgba(0,0,0,0.1); text-align:center;">
            <h2 style="color:#27ae60;">2FA Setup – Scan QR Code</h2>
            <p style="font-size:17px; color:#2c3e50;">Hello <strong>{role}</strong>,</p>
            <p style="font-size:16px; color:#34495e;">
                Your SuperAdmin account security is being upgraded!
            </p>
            <p style="font-size:16px; color:#34495e;">
                Please scan this QR code using <strong>Google Authenticator</strong> app mein:
            </p>
            
            <div style="margin:40px 0; padding:25px; background:#f8f9fa; border-radius:12px; border: 3px dashed #27ae60;">
                <img src="cid:qr_code.png" style="max-width:260px; border-radius:10px;">
            </div>
            
            <p style="background:#e8f5e8; padding:18px; border-radius:10px; color:#27ae60; font-weight:bold;">
                Scan karne ke baad aapko har 30 second mein naya 6-digit code milega
            </p>
            
            <hr style="border:1px dashed #ddd; margin:35px 0;">
            <p style="font-size:12px; color:#95a5a6;">© 2025 Superadmin • Bank-Level Security System</p>
        </div>
    </body>
    </html>
    """

    try:
        email = EmailMultiAlternatives(
            subject=subject,
            body="Open in HTML email to view your secure QR code.",
            from_email=f"Superadmin Security <{settings.EMAIL_HOST_USER}>",
            to=[to_email]
        )
        email.attach_alternative(html_content, "text/html")
        email.attach("qr_code.png", qr_image_bytes, "image/png")
        email.send(fail_silently=False)

        logger.info(f"QR Code successfully sent to {to_email}")
        return True

    except Exception as e:
        logger.error(f"Failed to send QR email to {to_email}: {e}")
        return False