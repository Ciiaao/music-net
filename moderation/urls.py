from django.urls import path
from . import views

urlpatterns = [
    path('', views.admin_dashboard, name='admin_dashboard'),
    path('user/<int:user_id>/toggle-block/', views.toggle_block_user, name='toggle_block_user'),
    path('post/<int:post_id>/delete/', views.delete_post, name='delete_post'),
    path('song/<int:song_id>/delete/', views.delete_song, name='delete_song'),
]