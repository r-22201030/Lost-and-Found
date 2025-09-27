from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages

# Home Page
def home(request):
    return render(request, 'Home.html')

# Signup View
def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # signup এর পর সাথে সাথে login
            messages.success(request, f"Welcome {user.username}, your account has been created!")
            return redirect('home')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})

# Login View
def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')  # already logged in হলে home এ redirect

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f"Welcome back, {user.username}!")
            return redirect('home')
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()

    return render(request, 'login.html', {'form': form})

# Logout View
def logout_view(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect('home')
from django.shortcuts import render
from .models import LostItem, FoundItem

def home_page(request):
    lost_items = LostItem.objects.all()
    found_items = FoundItem.objects.all()
    return render(request, "Home.html", {
        "lost_items": lost_items,
        "found_items": found_items
    })

def about_page(request):
    return render(request, "about.html")

def contact_page(request):
    return render(request, "contact.html")

def login_page(request):
    return render(request, "login.html")

from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

def signup_page(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)   # auto login after signup
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, "signup.html", {"form": form})

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages


# ✅ Home Page
def home_page(request):
    return render(request, "Home.html")


# ✅ Signup Page
def signup_page(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        terms = request.POST.get("terms")

        if not terms:
            return render(request, "signup.html", {"error": "You must agree to terms & conditions."})

        if User.objects.filter(username=username).exists():
            return render(request, "signup.html", {"error": "Username already exists!"})

        # নতুন user create
        user = User.objects.create_user(username=username, password=password)
        login(request, user)
        return redirect("home")

    return render(request, "signup.html")


# ✅ Login Page
def login_page(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("home")
        else:
            messages.error(request, "Invalid username or password")

    return render(request, "login.html")


# ✅ Logout Page
def logout_page(request):
    logout(request)
    return redirect("login")

from django.shortcuts import render

def about_page(request):
    return render(request, "about.html")

def contact_page(request):
    return render(request, "contact.html")

from django.contrib.auth import logout
from django.shortcuts import redirect

def logout_view(request):
    logout(request)
    return redirect('home')
from django.shortcuts import render

def about_page(request):
    return render(request, 'about.html')

def contact_page(request):
    return render(request, 'contact.html')
