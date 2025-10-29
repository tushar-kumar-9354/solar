from django.shortcuts import render
from django.core.mail import send_mail
from django.http import JsonResponse

def home(request):
    return render(request, 'index.html')

def send_quote(request):
    if request.method == 'POST':
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
        Additional Info: {info}
        """

        send_mail(subject, message, email, ['solartechgen@gmail.com'])
        return JsonResponse({'success': True})

    return JsonResponse({'success': False})
