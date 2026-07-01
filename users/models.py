from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

class User(AbstractUser):
    """Custom User model to allow for future global expansion."""
    is_admin_moderator = models.BooleanField(default=False)
    is_blocked = models.BooleanField(default=False)

class Profile(models.Model):
    """Profile model containing social attributes and follow relationships."""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    avatar = models.ImageField(upload_to='avatars/', default='avatars/default.png', blank=True)
    bio = models.TextField(max_length=500, blank=True)
    music_interests = models.CharField(max_length=255, blank=True, help_text="e.g. Rock, Techno, Hip-Hop")
    
    # Many-to-Many field for following system (non-symmetrical)
    following = models.ManyToManyField(
        'self', 
        related_name='followers', 
        symmetrical=False, 
        blank=True
    )
    is_private = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username}'s Profile"

# Signals to automatically create/save Profile whenever a User is created
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

class AppUser(User):
    """
    A Proxy model that tricks Django into displaying the 
    built-in User model inside our custom Users app.
    """
    class Meta:
        proxy = True
        verbose_name = 'User Account'
        verbose_name_plural = 'User Accounts'