from django import forms
from .models import Profile,Project,Comment
from django.contrib.auth.models import User
from django.forms import ModelForm

class NewProfileForm(forms.ModelForm):
    class Meta:
        model= Profile
        exclude =['user']

class NewProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        exclude = ['user', 'profile','comments','design','usability','content','vote']   


class NewCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        exclude = ['user','project']


class VoteForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ('design','usability','content')