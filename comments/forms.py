from django import forms
from .models import Comment


#forms.ModelForm | forms.Form

class CommentForm(forms.ModelForm):
    class Meta:
        model=Comment
        fields = ['name', 'email', 'text']