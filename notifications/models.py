from django.db import models
from django.conf import settings
from social.models import Post

class Notification(models.Model):
    NOTIFICATION_TYPES = (
        ('follow', 'Follow'),
        ('like', 'Like'),
        ('comment', 'Comment'),
        ('message', 'Message'),
    )
    
    recipient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notifications')
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sent_notifications')
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES)
    
    # Optional tie to a post (for likes and comments)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True, blank=True)
    text_preview = models.CharField(max_length=255, blank=True) # A snippet of the comment
    
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at'] # Newest notifications first

    def __str__(self):
        return f"{self.sender.username} -> {self.recipient.username} ({self.notification_type})"