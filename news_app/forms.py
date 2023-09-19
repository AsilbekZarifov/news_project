from django import forms
from .models import Contact,Comment

class Contactfrom(forms.ModelForm):

    class Meta:
        model = Contact
        fields = ['name', 'email', 'message']


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['body']