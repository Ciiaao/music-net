from django.urls import path
from . import views

urlpatterns = [
    path('inbox/', views.inbox, name='inbox'),
    path('', views.chat_inbox, name='chat_inbox'),
    path('<str:room_name>/', views.chat_room, name='chat_room'),
    path('share/<str:item_type>/<int:item_id>/', views.share_to_chat, name='share_to_chat'),
]