from django.http import JsonResponse
from django.shortcuts import render
from .email_utils import send_email_resend
import logging

logger = logging.getLogger(__name__)

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
🌟 NEW QUOTE REQUEST 🌟

Name: {name}
Email: {email}
Phone: {phone}
Address: {address}
Service Interested: {service}
Additional Information: {info}

This request was submitted through your website.
            """

            # Send email using Resends
            success = send_email_resend(
                'solartechgen@gmail.com',  # Send to yourself
                subject,
                message
            )
            
            if success:
                logger.info(f"Quote request sent via Resend from {email}")
                return JsonResponse({
                    'success': True, 
                    'message': 'Your quote request has been sent successfully! We will contact you within 24 hours.'
                })
            else:
                # Fallback: log to console
                logger.info(f"Quote request (needs manual follow-up): {name} - {email} - {phone}")
                return JsonResponse({
                    'success': True, 
                    'message': 'Your request has been received! We will contact you shortly.'
                })
                
        except Exception as e:
            logger.error(f"Error processing quote: {str(e)}")
            return JsonResponse({
                'success': False, 
                'message': 'Failed to process request. Please try again.'
            }, status=500)

    return JsonResponse({'success': False}, status=400)

def home(request):
    return render(request, 'index.html')