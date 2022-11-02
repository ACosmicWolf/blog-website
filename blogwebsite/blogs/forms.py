from django import forms
from .models import Blog

class BlogForm(forms.ModelForm):
    description=forms.CharField(widget=forms.Textarea)
    class Meta:
        model = Blog
        fields = [
            'title',
            'tags',
        ]