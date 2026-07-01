from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('profile/edit/', views.edit_profile_view, name='edit_profile'),
    path('explore/', views.explore_users, name='explore_users'), 
    path('u/<str:username>/', views.profile_view, name='profile_view'),
    path('u/<str:username>/follow/', views.toggle_follow, name='toggle_follow'),
    path('logout/', views.logout_view, name='logout'),
]