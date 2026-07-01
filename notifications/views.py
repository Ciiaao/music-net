from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Notification
@login_required
def notification_list(request):
    """Displays all notifications and marks them as read."""
    # Fetch notifications ordered by newest first
    notifications = Notification.objects.filter(recipient=request.user).order_by('-created_at')
    
    # Mark unread notifications as read since the user is looking at them now
    notifications.filter(is_read=False).update(is_read=True)
    
    return render(request, 'notifications/list.html', {
        'notifications': notifications
    })