from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from .models import *
from django.contrib import messages
import bcrypt

def home(request):
    return render(request, 'home.html')

def signin(request):
    return HttpResponse("<h1>Sign In</h1>")

def register(request):
    return HttpResponse("<h1>Register</h1>")

def my_profile(request):
    return HttpResponse("<h2>Edit your profile</h2>")

def users(request):
    return HttpResponse("<h2>List of users with ordering and search functions</h2>")

def new_user(request):
    return HttpResponse("<h3>Render page to create a new user<h3>")

def create_user(request):
    if request.method=="POST":
        errors = User.objects.basic_validator(request.POST)

        if errors:
            for k,v in errors.items():
                messages.error(request, v)
            return redirect('/')

        hash = bcrypt.hashpw( request.POST['password'].encode(), bcrypt.gensalt() ).decode()

        new_user = User.objects.create(
            first_name = request.POST['first_name'],
            last_name = request.POST['last_name'],
            email = request.POST['email'],
            password = hash
        )
        return redirect(f'/users/{new_user.id}')

    return redirect('/')

def show_user(request, id):
    return HttpResponse(f"<h3>Show profile for user id: {id}")

def edit_user(request, id):
    return HttpResponse(f"<h3>Edit user id: {id}")

def deactivate_user(request, id):
    #Check if logged in user is an admin
    #Don't delete, instead deactivate
    #All messages and comments should appear as "user deleted" or "deleted comment"
    return redirect('/dashboard')