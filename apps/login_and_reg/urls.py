from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('signin', views.signin_page, name="signin"),
    path('logout', views.logout, name="logout"),
    path('register', views.register, name="register"),
    path('my_profile', views.my_profile, name="my_profile"),
    path('my_page', views.my_page, name="my_page"),
    path('users/signin', views.signin_user, name="signin_user"),
    path('users/new', views.new_user, name="new_user"),
    path('users/create', views.create_user, name="create_user"),
    path('users/<int:id>', views.show_user, name="show_user"),
    path('users/<int:id>/edit', views.edit_user, name="edit_user"),
    path('users/<int:id>/update', views.update_user, name="update_user"),
    path('users/<int:id>/destroy', views.deactivate_user, name="deactivate_user"),
    path('users/<int:id>/post_message', views.post_message, name="post_message"),
    path('error', views.error_404, name="error_404"),
    path('newest_post', views.get_newest_post, name="get_newest_post"),

]