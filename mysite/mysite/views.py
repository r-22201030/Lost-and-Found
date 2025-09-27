
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib import messages
from .forms import SignUpForm

def signup(request):
    # handle next redirect if someone was trying to access a protected page
    next_url = request.GET.get('next') or request.POST.get('next') or None

    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # auto-login after signup
            messages.success(request, "Account created successfully. Welcome!")
            if next_url:
                return redirect(next_url)
            return redirect('home')
    else:
        form = SignUpForm()

    return render(request, 'registration/signup.html', {'form': form, 'next': next_url})

from django.http import HttpResponse

def home(request):
    return HttpResponse("Welcome to the Home Page")
