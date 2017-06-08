# appointments app

from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from datetime import datetime
import time

from ..users.models import User
from .models import Appointment

def index(request):
    user = User.objects.get(id = request.session['user_id'])
    today = time.strftime("%B %d, %Y")


    # fix filtering
    today_appointments = Appointment.objects.filter(user = user).filter(appoint_date = time.strftime("%Y-%m-%d"))

    other_appointments = Appointment.objects.exclude(appoint_date = time.strftime("%Y-%m-%d"))

    context = {
        'user': user,
        'today_appointments': today_appointments,
        'other_appointments': other_appointments,
        'today' : today
    }
    return render(request, 'appointments/index.html', context)


def read(request, appointment_id):
    appointment = Appointment.objects.get(id=appointment_id)
    # print datetime.strptime(appointment.appoint_time, '%I:%M %p').strftime("%I:%M %p")

    context = {
        'appointment': appointment,
        'date': appointment.appoint_date.strftime("%Y-%m-%d"),
        'time': appointment.appoint_time.strftime("%I:%M")
    }
    return render(request, 'appointments/appointment.html', context)


def create(request):
    if request.method == 'POST':
        new_appointment = {
            'appoint_date': request.POST['appoint_date'],
            'appoint_time': request.POST['appoint_time'],
            'task': request.POST['task'],
            'id': request.session['user_id']
        }

        validation = Appointment.objects.create_appointment(new_appointment)

        if 'errors' in validation:
            for error in validation['errors']:
                messages.error(request, error)

    return redirect(reverse('appointments:home'))

def edit(request, appointment_id):
    if request.method == 'POST':
        edit_appointment = {
            'id': appointment_id,
            'appoint_date': request.POST['date'],
            'appoint_time': request.POST['time'],
            'task': request.POST['task'],
            'status': request.POST['status']
        }

        validation = Appointment.objects.update_appointment(edit_appointment)

        if 'errors' in validation:
            for error in validation['errors']:
                messages.error(request, error)
            return redirect(reverse('appointments:edit', kwargs={'appointment_id': appointment_id }))
        else:
            return redirect(reverse('appointments:home'))
    
    return redirect(reverse('appointments:home'))


def delete(request):
    # Delete Appointment from db
    return redirect(reverse('appointments:home'))
