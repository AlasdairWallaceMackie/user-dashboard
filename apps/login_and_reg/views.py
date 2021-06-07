from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from .models import *
from ..dashboard.models import *
from django.contrib import messages
import bcrypt

def home(request):
    context = {
        'logged_in': False
    }

    if 'current_user_id' in request.session:
        context['logged_in'] = True

    return render(request, 'home.html', context)

def signin_page(request):
    return render(request, 'signin.html')

def signin_user(request):
    if request.method=="POST":
        errors = False
        try:
            user = User.objects.get(email = request.POST['email'])
        except:
            if request.POST['email'] == "":
                messages.error(request, "Please enter an email address")
            else:
                messages.error(request, "Email does not exist")
            errors = True
            return redirect('/signin')

        if not bcrypt.checkpw( request.POST['password'].encode(), user.password.encode()):
            messages.error(request, "Incorrect password")
            errors = True

        if not errors:
            request.session['current_user_id'] = user.id
            set_user_level(request)
            # request.session['user_level'] = user.user_level
            return redirect('/dashboard')
    
    return redirect('/signin')


def register(request):
    return render(request, 'register.html')

def duplicate_email(request):
    if request.method=="GET":
        print(f"Checking for duplicate email: {request.GET['email']}")
        print(f"Data: {request.GET}")
        email = request.GET['email']

        if email:
            return JsonResponse( {'duplicate': User.objects.filter(email = email).exists()} )
    
    return redirect('/')


def my_profile(request):
    context = {}
    try:
        context['current_user'] = User.objects.get(id = request.session['current_user_id'])
    except:
        return redirect('/')

    return render(request, 'my_profile.html')

def my_page(request):
    try:
        return redirect(f"/users/{request.session['current_user_id']}")
    except:
        return redirect('/signin')

def new_user(request):
    if request.session['user_level'] >= 7:
        return render(request, 'new_user.html')
    else:
        return redirect('/dashboard')

def edit_user(request, id):

    if 'current_user_id' in request.session:
        try:
            user = User.objects.get(id = id)
        except:
            messages.error(request, "User not found")
            return redirect('/error_404')

        context = {
            'user': user,
            'own_profile': False,
            'admin': False,
        }

        if id == request.session['current_user_id']:
            context['own_profile'] = True
        
        if request.session['user_level'] >= 7:
            context['admin'] = True

        if context['admin'] == True or context['own_profile'] == True:
            return render(request, 'edit_user.html', context)

    return redirect('/')

def create_user(request):
    if request.method=="POST":
        print("Creating user")
        errors = User.objects.basic_validator(request.POST)

        if errors:
            print("Errors found when creating user")
            for k,v in errors.items():
                messages.error(request, v)
            return redirect(f"/{request.POST['current_url']}")

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

        print(f"New user created! ID: {new_user.id}, Email: {new_user.email}")
        messages.success(request, "Account created!")
        if 'current_user_id' not in request.session:
            print(f"Logging in as {new_user.email}")
            request.session['current_user_id'] = new_user.id
            set_user_level(request)
        return redirect(f'/users/{new_user.id}')

    return redirect(f"/{request.POST['current_url']}")

def create_hash(plain_password):
    return bcrypt.hashpw( plain_password.encode(), bcrypt.gensalt() ).decode()

def show_user(request, id):
    if 'current_user_id' in request.session:
        context = {
            'can_edit': False
        }
        try:
            context['user'] = User.objects.get(id = id)
        except:
            messages.error(request, "User not found")
            return redirect('/error')

        if request.session['user_level'] >= 7 or request.session['current_user_id'] == id:
            context['can_edit'] = True

        return render(request, 'user_page.html', context)
    else:
        return redirect('/signin')

def update_user(request, id):
    #verify admin or id matches session

    if request.method=="POST":
        if request.session['user_level'] >= 7 or request.session['current_user_id'] == id:
            print("Attempting to update user. Validating...")
            try:
                user = User.objects.get(id = id)
            except:
                return HttpResponse("<h2>Error: User not found</h2>")
            
            errors = User.objects.basic_validator(request.POST)

            if 'email' in request.POST:
                if request.POST['email'].lower() == user.email:
                    errors.pop('duplicate_email')

            if errors:
                print("Errors found when updating user")
                for k,v in errors.items():
                    messages.error(request, v)
            else:

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
    return redirect(f"/users/{id}/edit")

def my_profile(request):
    if 'current_user_id' in request.session:
        return redirect(f"/users/{request.session['current_user_id']}/edit")
    else:
        return redirect('/')

def deactivate_user(request, id):
    #Check if logged in user is an admin
    #Don't delete, instead deactivate
    #All messages and comments should appear as "user deleted" or "deleted comment"
    return HttpResponse(f"<h2>Placeholder to delete user id: {id}</h2>")

def error_404(request):
    return render(request, 'error_404.html')

def logout(request):
    request.session.flush()
    return redirect('/')

def post_message(request, id):
    if request.method == "POST":
        errors = Message.objects.basic_validator(request.POST)

        if errors:
            for k,v in errors.items():
                messages.error(request, v)
        else:
            if 'message_id' in request.POST:
                Comment.objects.create(
                    text = request.POST['text'],
                    message = Message.objects.get(id = request.POST['message_id']),
                    author = User.objects.get(id = request.session['current_user_id']),
                )
            else:
                try:
                    recipient = User.objects.get(id = id)
                except:
                    messages.error("User not found")
                    return redirect('error')

                Message.objects.create(
                    text = request.POST['text'],
                    recipient = recipient,
                    author = User.objects.get(id = request.session['current_user_id'])
                )
    return redirect(f'/users/{id}')

def set_user_level(request):
    try:
        user = User.objects.get(id = request.session['current_user_id'])
        request.session['user_level'] = user.user_level
    except:
        return None

def get_newest_post(request):
    if request.method=="GET":
        try:
            current_user = User.objects.get(id = request.session['current_user_id'])
            class_name = current_user.most_recent_post().__class__.__name__.lower()
            context = {
                'current_user': current_user,
                f'{class_name}': current_user.most_recent_post(),
            }

            return JsonResponse({
                'render': render(request, f"{class_name}.html", context)
            })

        except:
            pass
    
    return redirect("/")