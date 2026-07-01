
from django.db import models
from django.conf import settings
# Import your music models at the top
from music.models import Song, Playlist 

class Message(models.Model):
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sent_messages')
    room_name = models.CharField(max_length=255)
    
    
    content = models.TextField(blank=True, null=True) 
    
   
    attached_song = models.ForeignKey(Song, on_delete=models.SET_NULL, null=True, blank=True)
    attached_playlist = models.ForeignKey(Playlist, on_delete=models.SET_NULL, null=True, blank=True)
    
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['timestamp']