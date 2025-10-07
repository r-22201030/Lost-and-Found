from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib import messages
from django.http import HttpResponse
from .forms import SignUpForm
from .models import LostItem, FoundItem

# -------------------------------
# Signup View
# -------------------------------
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

# -------------------------------
# Home View
# -------------------------------
def home(request):
    query = request.GET.get('q', '')

    lost_items = LostItem.objects.all()
    found_items = FoundItem.objects.all()

    # Apply search filter if query exists
    if query:
        lost_items = LostItem.objects.filter(title__icontains=query) | LostItem.objects.filter(location__icontains=query)
        found_items = FoundItem.objects.filter(title__icontains=query) | FoundItem.objects.filter(location__icontains=query)

    return render(request, 'Home.html', {
        'lost_items': lost_items,
        'found_items': found_items,
        'query': query,
    })

# -------------------------------
# Optional separate search view (if you want /search/ URL)
# -------------------------------
def search(request):
    query = request.GET.get('q', '')

    lost_items = LostItem.objects.filter(title__icontains=query) | LostItem.objects.filter(location__icontains=query)
    found_items = FoundItem.objects.filter(title__icontains=query) | FoundItem.objects.filter(location__icontains=query)

    return render(request, 'Home.html', {
        'lost_items': lost_items,
        'found_items': found_items,
        'query': query,
    })
