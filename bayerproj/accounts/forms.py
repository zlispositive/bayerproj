from accounts.models import UserProfile
from django.contrib.auth.models import User
from django import forms

class UserForm(forms.ModelForm):
	password = forms.CharField(widget=forms.PasswordInput())

	class Meta:
		model = User
		fields = ('username', 'email', 'password')

class UserProfileForm(forms.ModelForm):
	rank = forms.CharField(widget=forms.HiddenInput(),initial='X')
	class Meta:
		model = UserProfile
		fields = ('title','bu')