from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from users.models import User
from social.models import Post
from music.models import Song

# Custom Security Decorator
def moderator_required(view_func):
    """Ensures only users with admin privileges can access these views."""
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated and (request.user.is_admin_moderator or request.user.is_superuser):
            return view_func(request, *args, **kwargs)
        return redirect('main_feed')
    return _wrapped_view

@moderator_required
def admin_dashboard(request):
    """The main control panel for the platform."""
    users = User.objects.all().order_by('-date_joined')
    posts = Post.objects.all().order_by('-created_at')
    songs = Song.objects.all().order_by('-uploaded_at')
    
    return render(request, 'moderation/dashboard.html', {
        'users': users,
        'posts': posts,
        'songs': songs
    })

@moderator_required
def toggle_block_user(request, user_id):
    """مدیریت کاربران: مسدود کردن/رفع مسدودی"""
    target_user = get_object_or_404(User, id=user_id)
    
    # Prevent admins from blocking other superusers
    if not target_user.is_superuser:
        target_user.is_blocked = not target_user.is_blocked
        target_user.save()
        
    return redirect('admin_dashboard')

@moderator_required
def delete_post(request, post_id):
    """مدیریت محتوا: حذف پست‌های نامناسب"""
    post = get_object_or_404(Post, id=post_id)
    post.delete()
    return redirect('admin_dashboard')

@moderator_required
def delete_song(request, song_id):
    """مدیریت محتوا: حذف آهنگ‌های نامناسب"""
    song = get_object_or_404(Song, id=song_id)
    # This also deletes the physical audio file from the server
    song.audio_file.delete()
    song.delete()
    return redirect('admin_dashboard')