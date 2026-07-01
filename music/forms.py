from django import forms
from .models import Song, Playlist

class SongUploadForm(forms.ModelForm):
    class Meta:
        model = Song
        fields = ['audio_file', 'title', 'artist', 'album', 'genre', 'release_year']
        widgets = {
            'audio_file': forms.FileInput(attrs={'accept': 'audio/*'})
        }

class PlaylistForm(forms.ModelForm):
    class Meta:
        model = Playlist
        fields = ['title', 'is_public']