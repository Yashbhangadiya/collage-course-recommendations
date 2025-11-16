from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login 
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.models import User
from django.contrib import messages
from .models import College, Course, UserProfile
import csv
import os
from django.conf import settings

def load_colleges_from_csv():
    csv_path = os.path.join(settings.BASE_DIR, 'recommendation', 'colleges.csv')
    with open(csv_path, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            college, created = College.objects.get_or_create(
                name=row['name'],
                city=row['city'],
                website=row['website']
            )
            Course.objects.get_or_create(
                college=college,
                stream=row['stream'],
                name=row['course'],
                cutoff_percentage=float(row['cutoff_percentage']),
                description=row['description']
            )


def home(request):
    courses = None  # Default

    if request.user.is_authenticated:
        if request.method == 'POST':
            stream = request.POST.get('stream')
            percentage = request.POST.get('percentage')
            

            try:
                percentage = float(percentage)
                profile, created = UserProfile.objects.get_or_create(user=request.user)
                profile.stream = stream
                profile.percentage = percentage
                profile.save()

                load_colleges_from_csv()  # Load CSV data
                courses = Course.objects.filter(
                    stream=profile.stream,
                    cutoff_percentage__lte=profile.percentage
                ).select_related('college')

            except ValueError:
                messages.error(request, 'Please enter a valid percentage.')

        return render(request, 'home.html', {'courses': courses})

    else:
        if request.method == 'POST':
            return redirect('login')
        return render(request, 'home.html')


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'login.html')

def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
        else:
            user = User.objects.create_user(username=username, password=password, email=email)
            UserProfile.objects.create(user=user)
            login(request, user)
            return redirect('home')
    return render(request, 'signup.html')
def logout_view(request):  # Renamed to avoid conflict
    auth_logout(request)    # Call Django's logout function
    return redirect('home')
