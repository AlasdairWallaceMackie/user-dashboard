from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('signin', views.signin, name="signin"),
    path('register', views.register, name="register"),
    path('my_profile', views.my_profile, name="my_profile"),
    path('users', views.users, name="users_list"),
    path('users/new', views.new_user, name="new_user"),
    path('users/<int:id>', views.show_user, name="show_user"),
    path('users/edit/<int:id>', views.edit_user, name="edit_user"),
    path('users/destroy/<int:id>', views.deactivate_user, name="deactivate_user")
]