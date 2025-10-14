from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserChangeForm
from .forms import EditProfileForm, CustomPasswordChangeForm

from .models import LostItem, FoundItem, Item, Report, ReportItem
from .forms import ReportItemForm, ReportForm

# -------------------------
# Home Page (with Search)
# -------------------------
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

# -------------------------
# Signup Page
# -------------------------
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

# -------------------------
# Login Page
# -------------------------
def login_page(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, f"Welcome back, {user.username}!")
            return redirect("profile")
        else:
            messages.error(request, "Invalid username or password")

    return render(request, "login.html")

# -------------------------
# Logout Page
# -------------------------
def logout_page(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect("login")

# -------------------------
# About & Contact Pages
# -------------------------
def about_page(request):
    return render(request, "about.html")

def contact_page(request):
    return render(request, "contact.html")

# -------------------------
# Search Page
# -------------------------
def search(request):
    return render(request, 'search.html')

# -------------------------
# Report New Item (User reports lost/found item)
# -------------------------
@login_required
def report_item(request):
    if request.method == 'POST':
        form = ReportItemForm(request.POST, request.FILES)
        if form.is_valid():
            report_item = form.save(commit=False)
            report_item.user = request.user  # attach logged-in user
            report_item.save()
            messages.success(request, 'Your item report has been submitted successfully!')
            return redirect('user_reports')
    else:
        form = ReportItemForm()

    return render(request, 'report_item.html', {'form': form})

# -------------------------
# Item Detail Page
# -------------------------
def item_detail(request, item_type, id):
    if item_type == "lost":
        item = get_object_or_404(LostItem, id=id)
    elif item_type == "found":
        item = get_object_or_404(FoundItem, id=id)
    else:
        messages.error(request, "Invalid item type.")
        return redirect("home")

    return render(request, "item_detail.html", {"item": item, "item_type": item_type})

# -------------------------
# Report Existing Item to Admin (system-level report)
# -------------------------
@login_required
def report_existing_item(request, item_id):
    item = get_object_or_404(Item, id=item_id)

    if request.method == 'POST':
        form = ReportForm(request.POST)
        if form.is_valid():
            report = form.save(commit=False)
            report.item = item
            report.reporter = request.user
            report.save()

            # Optional: mark item as reported
            item.is_reported = True
            item.save()

            messages.success(request, "Your report has been submitted successfully.")
            return redirect('user_reports')
    else:
        form = ReportForm()

    return render(request, 'report_existing_item.html', {
        'form': form,
        'item': item,
    })

# -------------------------
# View All Reports by Logged-in User
# -------------------------
@login_required
def user_reports(request):
    """
    Show all reports created by the logged-in user.
    - my_reports: reports submitted via ReportItemForm (new items)
    - admin_reports: system-level reports on existing Item objects (only pending)
    """
    # User-submitted reports (all considered pending by default)
    my_reports = ReportItem.objects.filter(user=request.user).order_by('-created_at')

    # System-level reports: only pending
    admin_reports = Report.objects.filter(reporter=request.user, status='pending').order_by('-created_at')

    return render(request, 'user_reports.html', {
        'my_reports': my_reports,
        'admin_reports': admin_reports,
    })

@login_required
def profile_page(request):
    user = request.user  # logged-in user
    return render(request, 'profile.html', {'user': user})


@login_required
def profile_view(request):
    user = request.user
    lost_items = LostItem.objects.filter(user=user)  # এই user-এর রিপোর্ট করা সব item

    return render(request, 'profile.html', {
        'user': user,
        'lost_items': lost_items,
    })


@login_required
def edit_profile(request):
    if request.method == 'POST':
        profile_form = EditProfileForm(request.POST, instance=request.user)
        password_form = CustomPasswordChangeForm(request.user, request.POST)

        if 'first_name' in request.POST and profile_form.is_valid():
            profile_form.save()
            return redirect('profile')

        elif password_form.is_valid():
            user = password_form.save()
            update_session_auth_hash(request, user)  # logout না হয়
            return redirect('profile')

    else:
        profile_form = EditProfileForm(instance=request.user)
        password_form = CustomPasswordChangeForm(request.user)

    return render(request, 'edit_profile.html', {
        'profile_form': profile_form,
        'password_form': password_form,
    })