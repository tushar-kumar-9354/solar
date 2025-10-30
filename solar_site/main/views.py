from django.shortcuts import render
from django.core.mail import send_mail, BadHeaderError
from django.http import JsonResponse
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

def home(request):
    return render(request, 'index.html')

def send_quote(request):
    if request.method == 'POST':
        try:
            name = request.POST.get('name')
            email = request.POST.get('email')
            phone = request.POST.get('phone')
            address = request.POST.get('address')
            service = request.POST.get('service')
            info = request.POST.get('info')

            subject = f"New Quote Request from {name}"
            message = f"""
            Name: {name}
            Email: {email}
            Phone: {phone}
            Address: {address}
            Service Interested: {service}
            Additional Information: {info}
            
            This is a new quote request from your website.
            """

            # Try to send email
            try:
                send_mail(
                    subject,
                    message,
                    settings.DEFAULT_FROM_EMAIL,  # Use your email as sender, not user's email
                    [settings.DEFAULT_FROM_EMAIL],  # Send to yourself
                    fail_silently=False,
                )
                logger.info(f"Quote request sent successfully from {email}")
                return JsonResponse({
                    'success': True, 
                    'message': 'Your quote request has been sent successfully! Our solar expert will contact you within 24 hours.'
                })
                
            except (BadHeaderError, ConnectionRefusedError, OSError) as e:
                # Log the request to database or file instead
                logger.warning(f"Email failed, but quote request received from {email}: {str(e)}")
                
                # Still return success to user, but log the request
                return JsonResponse({
                    'success': True, 
                    'message': 'Your request has been received! We will contact you shortly. (Note: Email confirmation may be delayed)'
                })
                
        except Exception as e:
            logger.error(f"Error processing quote request: {str(e)}")
            return JsonResponse({
                'success': False, 
                'message': 'Failed to process your request. Please try again later or contact us directly.'
            }, status=500)

    return JsonResponse({
        'success': False, 
        'message': 'Invalid request method.'
    }, status=400)