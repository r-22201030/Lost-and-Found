# apps/urls.py
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
    path('report/', views.report_item, name='report_item'),
    path('item/<str:item_type>/<int:id>/', views.item_detail, name='item_detail'),


]
