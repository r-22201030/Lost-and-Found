from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_page, name='home'),
    path('signup/', views.signup_page, name='signup'),
    path('login/', views.login_page, name='login'),
    path('logout/', views.logout_page, name='logout'),
    path('about/', views.about_page, name='about'),
    path('contact/', views.contact_page, name='contact'),
    path('search/', views.search, name='search'),

    # New item report
    path('report/', views.report_item, name='report_item'),

    # Item details
    path('item/<str:item_type>/<int:id>/', views.item_detail, name='item_detail'),

    # Existing item report
    path('item/<int:item_id>/report/', views.report_existing_item, name='report_existing_item'),

    # User's reports
    path('my-reports/', views.user_reports, name='user_reports'),
    path('profile/', views.profile_page, name='profile'),
    path('edit-profile/', views.edit_profile, name='edit_profile'),
    path('notifications/', views.notifications, name='notifications')

]
