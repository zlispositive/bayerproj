from django.shortcuts import render, render_to_response
from django import forms
from django.http import HttpResponse, HttpResponseRedirect
# from accounts.models import User

# Create your views here.

class UserForm(forms.Form):
	username = forms.CharField()
	password = forms.CharField(widget = forms.PasswordInput )

# def regist(req):
# 	if req.method == 'POST':
# 		uf = UserForm(req.POST)
# 		if uf.is_valid():
# 			username = uf.cleaned_data['username']
# 			password = uf.cleaned_data['password']
# 			User.objects.create(username = username, password = password)
# 			return HttpResponseRedirect('/login/')
# 	else:
# 		uf = UserForm()
# 	return render_to_response('regist.html', {'uf': uf})

# def login(req):
# 	if req.method == 'POST':
# 		uf = UserForm(req.POST)
# 		if uf.is_valid():
# 			username = uf.cleaned_data['username']
# 			password = uf.cleaned_data['password']
# 			user = User.objects.filter(username__exact = username, password_exact = password)
# 			if user:
# 				req.session['username'] = username
# 				return HttpResponseRedirect('/index/')
# 			else:
# 				return HttpResponseRedirect('/login/')
# 	else:
# 		uf = UserForm()
# 	return render_to_response('logout.html', {'uf': uf})

# def index(req):
# 	username = req.session.get('username', 'anybody')
# 	return render_to_response('index.html', {'username': session})

# def logout(req):
# 	session = req.session.get('username', False)
# 	if session:
# 		del req.session['username']
# 		return render_to_response('logout.html', {'username': session})
# 	else:
# 		return HttpResponse('Please login!')