from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Song, Playlist
from .forms import SongUploadForm, PlaylistForm

@login_required
def upload_song(request):
    if request.method == 'POST':
        form = SongUploadForm(request.POST, request.FILES)
        if form.is_valid():
            song = form.save(commit=False)
            song.uploader = request.user
            song.save()
            return redirect('song_detail', song_id=song.id)
    else:
        form = SongUploadForm()
    return render(request, 'music/upload.html', {'form': form})

def song_detail(request, song_id):
    song = get_object_or_404(Song, id=song_id)
    return render(request, 'music/song_detail.html', {'song': song})

@login_required
def create_playlist(request):
    if request.method == 'POST':
        form = PlaylistForm(request.POST)
        if form.is_valid():
            playlist = form.save(commit=False)
            playlist.owner = request.user
            playlist.save()
            return redirect('playlist_detail', playlist_id=playlist.id)
    else:
        form = PlaylistForm()
    return render(request, 'music/playlist_form.html', {'form': form})

def playlist_detail(request, playlist_id):
    playlist = get_object_or_404(Playlist, id=playlist_id)
    return render(request, 'music/playlist_detail.html', {'playlist': playlist})

# Update your existing song_detail view to look like this:
def song_detail(request, song_id):
    song = get_object_or_404(Song, id=song_id)
    user_playlists = None
    if request.user.is_authenticated:
        # Fetch playlists so the user can add this song to them
        user_playlists = request.user.playlists.all()
    return render(request, 'music/song_detail.html', {
        'song': song, 
        'user_playlists': user_playlists
    })

@login_required
def add_to_playlist(request, song_id):
    """Processes the form on the song page to add a track to a playlist."""
    if request.method == 'POST':
        song = get_object_or_404(Song, id=song_id)
        playlist_id = request.POST.get('playlist_id')
        
        # Security check: Ensure the user actually owns the playlist they selected
        playlist = get_object_or_404(Playlist, id=playlist_id, owner=request.user)
        
        playlist.songs.add(song)
    return redirect('song_detail', song_id=song_id)


@login_required
def remove_from_playlist(request, playlist_id, song_id):
    """Removes a track from a playlist."""
    if request.method == 'POST':
        # Security check: Only the owner can remove songs
        playlist = get_object_or_404(Playlist, id=playlist_id, owner=request.user)
        song = get_object_or_404(Song, id=song_id)
        
        playlist.songs.remove(song)
    return redirect('playlist_detail', playlist_id=playlist_id)

from django.db.models import Q

@login_required
def playlist_add_tracks(request, playlist_id):
    """A dedicated page to search and add tracks to a specific playlist."""
    playlist = get_object_or_404(Playlist, id=playlist_id, owner=request.user)
    
    query = request.GET.get('q', '')
    if query:
        # Search by title OR artist
        songs = Song.objects.filter(Q(title__icontains=query) | Q(artist__icontains=query))
    else:
        # If no search, just show the 20 newest songs on the platform
        songs = Song.objects.all().order_by('-uploaded_at')[:20]
        
    return render(request, 'music/playlist_add_tracks.html', {
        'playlist': playlist,
        'songs': songs,
        'query': query
    })

@login_required
def quick_add_to_playlist(request, playlist_id, song_id):
    """Instantly adds a song to the playlist from the search page."""
    if request.method == 'POST':
        playlist = get_object_or_404(Playlist, id=playlist_id, owner=request.user)
        song = get_object_or_404(Song, id=song_id)
        
        # Add the song to the playlist
        playlist.songs.add(song)
        
    # Redirect back to the search page so they can keep adding songs
    return redirect('playlist_add_tracks', playlist_id=playlist_id)

from django.db.models import Q




@login_required
def global_search(request):
    """A global search page to find any song or artist on the platform."""
    query = request.GET.get('q', '')
    songs = []
    
    if query:
        # Search by title OR artist across the entire platform
        songs = Song.objects.filter(Q(title__icontains=query) | Q(artist__icontains=query)).order_by('-uploaded_at')
        
    return render(request, 'music/search.html', {
        'songs': songs,
        'query': query
    })


@login_required
def delete_playlist(request, playlist_id):
    """Deletes a playlist permanently."""
    # Security: Ensure the logged-in user is the owner
    playlist = get_object_or_404(Playlist, id=playlist_id, owner=request.user)
    
    if request.method == 'POST':
        playlist.delete()
        # Redirect them back to their profile page after deletion
        return redirect('profile_view', username=request.user.username)
        
    return redirect('playlist_detail', playlist_id=playlist_id)