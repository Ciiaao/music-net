from django.urls import path
from . import views

urlpatterns = [
    path('', views.main_feed, name='main_feed'),
    path('discover/', views.discover_feed, name='discover_feed'),
    path('post/<int:post_id>/like/', views.toggle_like, name='toggle_like'),
    path('post/<int:post_id>/comment/', views.add_comment, name='add_comment'),
    path('share/<str:item_type>/<int:item_id>/', views.share_to_feed, name='share_to_feed'),
]