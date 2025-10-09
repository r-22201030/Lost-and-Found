from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Q

from .models import LostItem, FoundItem, Item
from .forms import ReportItemForm


# ✅ Home Page (with Search)
def home_page(request):
    query = request.GET.get('q', '').strip()

    if query:
        lost_items = LostItem.objects.filter(
            Q(title__icontains=query) | Q(location__icontains=query)
        )
        found_items = FoundItem.objects.filter(
            Q(title__icontains=query) | Q(location__icontains=query)
        )
    else:
        lost_items = LostItem.objects.all()
        found_items = FoundItem.objects.all()

    return render(request, "Home.html", {
        "lost_items": lost_items,
        "found_items": found_items,
        "query": query,
    })


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

        user = User.objects.create_user(username=username, password=password)
        login(request, user)
        messages.success(request, f"Welcome {user.username}, your account has been created!")
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
            messages.success(request, f"Welcome back, {user.username}!")
            return redirect("home")
        else:
            messages.error(request, "Invalid username or password")

    return render(request, "login.html")


# ✅ Logout Page
def logout_page(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect("login")


# ✅ About Page
def about_page(request):
    return render(request, "about.html")


# ✅ Contact Page
def contact_page(request):
    return render(request, "contact.html")


# ✅ Search Page (optional)
def search(request):
    return render(request, 'search.html')


# ✅ Report Item Page (FORM Version)
def report_item(request):
    if request.method == 'POST':
        form = ReportItemForm(request.POST, request.FILES)
        if form.is_valid():
            item = form.save(commit=False)
            if request.user.is_authenticated:
                item.created_by = request.user
            item.save()
            messages.success(request, 'Item reported successfully!')
            return redirect('report_item')  # submission success → same page
    else:
        form = ReportItemForm()

    # ✅ Template path ঠিক করা হলো
    return render(request, 'report_item.html', {'form': form})


# ✅ Item Detail Page
def item_detail(request, item_type, id):
    """
    item_type: 'lost' or 'found'
    id: item id
    """
    if item_type == "lost":
        item = get_object_or_404(LostItem, id=id)
    elif item_type == "found":
        item = get_object_or_404(FoundItem, id=id)
    else:
        messages.error(request, "Invalid item type.")
        return redirect("home")

    return render(request, "item_detail.html", {"item": item, "item_type": item_type})
