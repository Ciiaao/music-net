from django import forms
from .models import Post, Comment

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['content', 'attached_song', 'attached_playlist']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 3, 'placeholder': 'What are you listening to?'}),
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        widgets = {
            'text': forms.TextInput(attrs={'placeholder': 'Write a comment...'}),
        }