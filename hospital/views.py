from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core.mail import send_mail
from django.conf import settings

from .forms import BookingForm

from .models import Department, Doctors


# Create your views here.
def index(request):
    return render(request,'index.html')

def about(request):
    return render(request,'about.html')

def booking(request):
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save()

            # ---------- Admin / Hospital Email ----------
            subject = f'New Appointment Booking - {booking.p_name}'
            message = f'''
A new booking has been made:

Name: {booking.p_name}
Phone: {booking.p_phone}
Email: {booking.p_email}
Doctor: {booking.doc_name}
Date: {booking.booking_date}
            '''

            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,        # From (hospital email)
                ['arshadarshaz135@gmail.com'],      # To (your email)
                fail_silently=False,
            )

            # ---------- Patient Confirmation Email ----------
            send_mail(
                "Appointment Confirmation",
                f"Dear {booking.p_name},\n\n"
                "Thank you for booking an appointment with CityCare Hospital.\n"
                f"Doctor: {booking.doc_name}\n"
                f"Date: {booking.booking_date}\n\n"
                "We look forward to seeing you.\n\n"
                "CityCare Hospital",
                settings.DEFAULT_FROM_EMAIL,        # From hospital
                [booking.p_email],                  # ✅ Patient email
                fail_silently=False,
            )

            return render(request, 'confirmation.html')
    else:
        form = BookingForm()

    return render(request, 'booking.html', {'form': form})


def contact(request):
    return render(request,'contact.html')

def department(request):
    dict_dept = {
        'dept': Department.objects.all()
    }
    return render(request,'department.html', dict_dept)

def doctors(request):
    dict_docs = {
        'doctors': Doctors.objects.all()
    }
    return render(request,'doctors.html', dict_docs)