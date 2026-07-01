from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from .models import Post, Like, Comment
from .forms import PostForm, CommentForm
from notifications.models import Notification
from music.models import Song, Playlist
@login_required
def main_feed(request):
    """Shows posts ONLY from users the current user is following."""
    following_users = request.user.profile.following.all()
    # Include the user's own posts plus the people they follow
    users_to_show = list(following_users) + [request.user.profile]
    
    posts = Post.objects.filter(author__profile__in=users_to_show)
    
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('main_feed')
    else:
        form = PostForm()
        
    return render(request, 'social/feed.html', {'posts': posts, 'form': form, 'feed_type': 'Main Feed'})

@login_required
def discover_feed(request):
    """Shows popular posts from across the entire network."""
    # Get top 50 posts ordered by the number of likes
    posts = Post.objects.annotate(like_count=Count('likes')).order_by('-like_count', '-created_at')[:50]
    return render(request, 'social/feed.html', {'posts': posts, 'feed_type': 'Discovery Feed'})

@login_required
def toggle_like(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    like, created = Like.objects.get_or_create(post=post, user=request.user)
    
    if not created:
        like.delete() 
    elif request.user != post.author: # Only notify if someone ELSE likes it
        Notification.objects.create(
            recipient=post.author, sender=request.user, notification_type='like', post=post
        )
    return redirect(request.META.get('HTTP_REFERER', 'main_feed'))

@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            
            if request.user != post.author: # Only notify if someone ELSE comments
                Notification.objects.create(
                    recipient=post.author, 
                    sender=request.user, 
                    notification_type='comment', 
                    post=post, 
                    text_preview=comment.text[:50] # Save a snippet of the comment
                )
    return redirect(request.META.get('HTTP_REFERER', 'main_feed'))




@login_required
def share_to_feed(request, item_type, item_id):
    """Creates a new post with a pre-attached song or playlist."""
    song = None
    playlist = None
    
    # Determine what we are sharing based on the URL parameters
    if item_type == 'song':
        song = get_object_or_404(Song, id=item_id)
    elif item_type == 'playlist':
        playlist = get_object_or_404(Playlist, id=item_id)
        # Prevent sharing private playlists
        if not playlist.is_public and playlist.owner != request.user:
            return redirect('main_feed')
            
    if request.method == 'POST':
        content = request.POST.get('content', '')
        # Create the post with the attached media
        Post.objects.create(
            author=request.user,
            content=content,
            attached_song=song,
            attached_playlist=playlist
        )
        return redirect('main_feed')
        
    return render(request, 'social/share.html', {
        'song': song, 
        'playlist': playlist
    })