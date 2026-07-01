from django.urls import path
from . import views

urlpatterns = [
    path('upload/', views.upload_song, name='upload_song'),
    path('track/<int:song_id>/', views.song_detail, name='song_detail'),
    path('playlist/new/', views.create_playlist, name='create_playlist'),
    path('playlist/<int:playlist_id>/', views.playlist_detail, name='playlist_detail'),
    path('song/<int:song_id>/add-to-playlist/', views.add_to_playlist, name='add_to_playlist'),
    path('playlist/<int:playlist_id>/remove-song/<int:song_id>/', views.remove_from_playlist, name='remove_from_playlist'),
    path('playlist/<int:playlist_id>/add-tracks/', views.playlist_add_tracks, name='playlist_add_tracks'),
    path('playlist/<int:playlist_id>/quick-add/<int:song_id>/', views.quick_add_to_playlist, name='quick_add_to_playlist'),
    path('search/', views.global_search, name='global_search'),
    path('playlist/<int:playlist_id>/delete/', views.delete_playlist, name='delete_playlist'),

]