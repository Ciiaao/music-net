from django.shortcuts import get_object_or_404, render
from notifications.models import Notification
from django.shortcuts import render, redirect
from django.contrib.auth import login,logout
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm, ProfileUpdateForm
from .models import User, Profile

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('main_feed')
    else:
        form = RegisterForm()
    return render(request, 'users/register.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def profile_view(request, username):
    target_user = get_object_or_404(User, username=username)
    profile = target_user.profile
    is_following = request.user.profile.following.filter(id=profile.id).exists()
    
    # 1. Fetch all songs uploaded by this user
    songs = target_user.uploaded_songs.all().order_by('-uploaded_at')
    
    # 2. Fetch playlists (Hide private ones if looking at someone else's profile)
    if request.user == target_user:
        playlists = target_user.playlists.all().order_by('-created_at')
    else:
        playlists = target_user.playlists.filter(is_public=True).order_by('-created_at')
    
    return render(request, 'users/profile.html', {
        'target_user': target_user,
        'profile': profile,
        'is_following': is_following,
        'songs': songs,
        'playlists': playlists  # Pass the new data to the template
    })
@login_required
def edit_profile_view(request):
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            return redirect('profile_view', username=request.user.username)
    else:
        form = ProfileUpdateForm(instance=request.user.profile)
    return render(request, 'users/edit_profile.html', {'form': form})

@login_required
def toggle_follow(request, username):
    user_to_toggle = get_object_or_404(User, username=username)
    profile_to_toggle = user_to_toggle.profile
    user_profile = request.user.profile

    if user_profile != profile_to_toggle:
        if user_profile.following.filter(id=profile_to_toggle.id).exists():
            user_profile.following.remove(profile_to_toggle)
        else:
            user_profile.following.add(profile_to_toggle)
            # Create the notification!
            Notification.objects.create(
                recipient=user_to_toggle, 
                sender=request.user, 
                notification_type='follow'
            )
            
    return redirect('profile_view', username=username)
@login_required
def explore_users(request):
    """A directory to find and follow other users."""
    # Get all users except the currently logged-in user and hidden superusers
    users = User.objects.exclude(id=request.user.id).exclude(is_superuser=True)
    return render(request, 'users/explore.html', {'users': users})