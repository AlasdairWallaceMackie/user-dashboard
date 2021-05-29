from django.shortcuts import redirect, render
from ..login_and_reg.models import User

def dashboard(request):

    if 'current_user_id' in request.session:
        context = {
            'all_users': User.objects.all(),
            'admin': False,
        }

        if request.session['user_level'] >= 7:
            context['admin'] = True
            
        return render(request, 'dashboard.html', context)

    else:
        return redirect('/signin')