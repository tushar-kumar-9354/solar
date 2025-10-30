import resend
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

def send_email_resend(to_email, subject, message):
    """Send email using Resend API"""
    try:
        if not settings.RESEND_API_KEY:
            logger.warning("Resend API key not configured")
            return False
            
        resend.api_key = settings.RESEND_API_KEY
        
        params = {
            "from": "Solar Tech Gen <onboarding@resend.dev>",
            "to": [to_email],
            "subject": subject,
            "html": f"<pre>{message}</pre>",  # Simple HTML formatting
        }
        
        response = resend.Emails.send(params)
        logger.info(f"Email sent via Resend: {response}")
        return True
        
    except Exception as e:
        logger.error(f"Resend email failed: {str(e)}")
        return False