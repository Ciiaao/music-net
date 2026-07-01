from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from users.models import User
from chat.models import Message
from music.models import Playlist,Song
from social.models import Post
from notifications.models import Notification
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


@login_required
def chat_room(request, room_name):
    other_user = None
    
    try:
        # If the room_name is actually a username, it's a private 1-on-1 chat
        other_user = User.objects.get(username=room_name)
        # Create a consistent, unique room string by sorting usernames alphabetically
        users = sorted([request.user.username, other_user.username])
        actual_room_name = f"private_{users[0]}_{users[1]}"
    except User.DoesNotExist:
        # If the user doesn't exist, treat it as a public Group Chat (e.g. global_music_lounge)
        actual_room_name = room_name

    # Fetch history using the actual room name
    messages = Message.objects.filter(room_name=actual_room_name).order_by('timestamp')[:50]
    
    return render(request, 'chat/room.html', {
        'room_name': actual_room_name,
        'display_name': room_name, # Display the username or group name at the top
        'other_user': other_user,
        'messages': messages
    })
@login_required
def chat_inbox(request):
    # A simple page listing who the user follows so they can click and chat with them
    following = request.user.profile.following.all()
    return render(request, 'chat/inbox.html', {'following': following})




# Replace your share_to_chat function with this:
@login_required
def share_to_chat(request, item_type, item_id):
    """Sends a message with an embedded playable song or playlist, and triggers a notification."""
    song = None
    playlist = None
    item_title = ""

    # Grab the actual object from the database
    if item_type == 'song':
        song = get_object_or_404(Song, id=item_id)
        item_title = f"Song: {song.title}"
    elif item_type == 'playlist':
        playlist = get_object_or_404(Playlist, id=item_id)
        item_title = f"Playlist: {playlist.title}"
    elif item_type == 'post':
        post = get_object_or_404(Post, id=item_id)
        item_title = f"a Post by {post.author.username}"
        song = post.attached_song
        playlist = post.attached_playlist

    following = request.user.profile.following.all()

    if request.method == 'POST':
        recipient_username = request.POST.get('recipient')
        recipient = get_object_or_404(User, username=recipient_username)
        message_content = request.POST.get('content', '') # Optional custom text

        users = sorted([request.user.username, recipient.username])
        room_name = f"private_{users[0]}_{users[1]}"

        # 1. Save to the Message database
        Message.objects.create(
            sender=request.user,
            room_name=room_name,
            content=message_content,
            attached_song=song,
            attached_playlist=playlist
        )

        # 2. CREATE THE NOTIFICATION (This is the missing piece!)
        # Create a smart preview text depending on if they typed a message or not
        preview_text = message_content[:50] if message_content else f"Shared a {item_title}"
        
        if request.user != recipient: # Don't notify if they share it with themselves
            Notification.objects.create(
                recipient=recipient,
                sender=request.user,
                notification_type='message',
                text_preview=preview_text
            )

        # 3. Build the live WebSocket payload
        attachment_data = None
        if song:
            attachment_data = {
                'type': 'song', 
                'title': song.title, 
                'artist': song.artist, 
                'url': song.audio_file.url
            }
        elif playlist:
            attachment_data = {
                'type': 'playlist', 
                'title': playlist.title, 
                'id': playlist.id, 
                'count': playlist.songs.count()
            }

        # 4. Broadcast to the room
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            room_name,
            {
                'type': 'chat_message',
                'message': message_content,
                'username': request.user.username,
                'attachment': attachment_data 
            }
        )

        return redirect('chat_room', room_name=recipient.username)

    return render(request, 'chat/share_to_chat.html', {
        'item_title': item_title,
        'following': following
    })
@login_required
def inbox(request):
    """The main messaging dashboard."""
    # Get everyone the user follows so they can quickly start a chat
    following = request.user.profile.following.all()
    
    return render(request, 'chat/inbox.html', {
        'following': following
    })