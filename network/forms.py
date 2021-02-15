from django import forms
from django.forms import ModelForm
from .models import Post, Like, Author
from django.forms import BaseModelFormSet
from django.forms import modelformset_factory


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['body']
        labels = {
            'body':""
        }
        widgets = {
            "body": forms.Textarea(
                attrs={
                    "class":"form-control",
                    "placeholder":"What's on your mind?",
                    "rows":"2",
                }
            )
        }
