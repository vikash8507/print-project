from django.shortcuts import  render, redirect
from django.contrib.auth import login
from django.contrib import messages

from .forms import NewUserForm

def register_view(request):
	if request.user.is_authenticated:
		return redirect('dashboard')

	if request.method == "POST":
		form = NewUserForm(request.POST)
		if form.is_valid():
			user = form.save()
			login(request, user)
			messages.success(request, "Registration successful." )
			return redirect("login")
		else:
			form = NewUserForm(request.POST)
			return render (request, "registration/register.html", {"form":form})
	form = NewUserForm()
	return render (request, "registration/register.html", {"form":form})