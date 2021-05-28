from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from .models import *
from django.contrib import messages
import bcrypt

def home(request):
    return render(request, 'home.html')

def signin_page(request):
    return render(request, 'signin.html')

def signin_user(request):
    if request.method=="POST":
        errors = False
        try:
            user = User.objects.get(email = request.POST['email'])
        except:
            messages.error(request, "Email does not exist")
            errors = True

        if not bcrypt.checkpw( request.POST['password'].encode(), user.password.encode()):
            messages.error(request, "Incorrect password")
            errors = True

        if not errors:
            request.session['current_user_id'] = user.id
            request.session['user_level'] = user.user_level
            return redirect('/dashboard')
    
    return redirect('/signin')


def register(request):
    return render(request, 'register.html')

def my_profile(request):
    context = {}
    try:
        context['current_user'] = User.objects.get(id = request.session['current_user_id'])
    except:
        return redirect('/')

    return render(request, 'my_profile.html')

def new_user(request):
    if request.session['user_level'] >= 7:
        return render(request, '/users/new')
    else:
        return redirect('/dashboard')

def edit_user(request, id):
    user = User.objects.get(id = request.session['current_user_id'])
    context = {
        'user': user,
    }

    if user.id == id:
        context['own_profile'] = True
    elif user.user_level >= 7:
        context['own_profile'] = False
    else:
        return redirect('/')

    return render(request, 'edit_user.html', context)
    

def create_user(request):
    if request.method=="POST":
        errors = User.objects.basic_validator(request.POST)

        if errors:
            for k,v in errors.items():
                messages.error(request, v)
            return redirect('/')

        hash = create_hash(request.POST['password'])

        if User.objects.all().count() == 0:
            user_level = 9
        elif 'user_level' not in request.POST:
            user_level = 1
        else:
            user_level = request.POST['user_level']

        new_user = User.objects.create(
            first_name = request.POST['first_name'],
            last_name = request.POST['last_name'],
            email = request.POST['email'].lower(),
            password = hash,
            user_level = user_level
        )

        if 'current_user_id' not in request.session:
            request.session['current_user_id'] = new_user.id
        return redirect(f'/users/{new_user.id}')

    return redirect('/')

def create_hash(plain_password):
    return bcrypt.hashpw( plain_password.encode(), bcrypt.gensalt() ).decode()

def OLDcreate_user(request):
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
    context = {}
    try:
        context['user'] = User.objects.get(id = id)
    except:
        error_404(request, "User not found")
        return False

    return render(request, 'user_page.html', context)

def update_user(request, id):
    if request.method=="POST":
        errors = User.objects.basic_validator(request.POST)
        if errors:
            for k,v in errors.items():
                messages.error(request, v)
        else:
            user = User.objects.get(id = id)
            if 'password' in request.POST:
                user.password = create_hash(request.POST['password'])

            elif 'email' in request.POST:
                user.email = request.POST['email']
                user.first_name = request.POST['first_name']
                user.last_name = request.POST['last_name']

            elif 'description' in request.POST:
                user.description = request.POST['description']

            user.save()
            messages.success(request, "Account updated!")
    return redirect(f"users/{id}")

def my_profile(request):
    if 'current_user_id' in request.session:
        return redirect(f"/users/{request.session['current_user_id']}")
    else:
        return redirect('/')

def deactivate_user(request, id):
    #Check if logged in user is an admin
    #Don't delete, instead deactivate
    #All messages and comments should appear as "user deleted" or "deleted comment"
    return redirect('/dashboard')

def error_404(request, message):
    context = {
        'message': message
    }
    return render(request, 'error_404.html', context)

def logout(request):
    request.session.flush()
    return redirect('/')