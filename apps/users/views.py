# users app

from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from .models import User

def index(request):
    return render(request, 'users/index.html')

def login(request):
    if request.method == 'POST':

        attempt = User.objects.login(request.POST['email'], request.POST['password'])

        if not 'errors' in attempt:
            user = User.objects.get(email = request.POST['email'])
            user_in_session(request, user)

            return redirect(reverse('appointments:home'))
        else:
            for error in attempt['errors']:
                messages.error(request, error)
            
    return redirect(reverse('users:home'))

def register(request):
    if request.method == 'POST':
        user_input = {
            'name': request.POST['name'],
            'dob': request.POST['dob'],
            'email': request.POST['email'],
            'password': request.POST['password'],
            'password_confirm': request.POST['password_confirm'],
        }

        attempt = User.objects.register(user_input)

        if 'errors' in attempt:
            for error in attempt['errors']:
                messages.error(request, error)

        if 'new_user' in attempt:
            user_in_session(request, attempt['new_user'])
            return redirect(reverse('appointments:home'))

    return redirect(reverse('users:home'))

def user_in_session(request, user):
    request.session['user_id'] = user.id

def logout(request):
    request.session['user_id'] = null

    return redirect(reverse('users:home'))
    