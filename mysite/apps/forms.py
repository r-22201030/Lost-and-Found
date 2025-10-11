# core/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Item, LostItem, FoundItem,Report

class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True, help_text='Required. Enter a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("This email is already registered.")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data.get('first_name', '')
        user.last_name = self.cleaned_data.get('last_name', '')
        if commit:
            user.save()
        return user


class ReportItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = [
            'name',
            'category',
            'location',
            'date_lost',
            'description',
            'contact_info',
            'image'
        ]
        widgets = {
            'date_lost': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 3}),
        }


class ReportForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = ['reason', 'description']  # ✅ 'details' নয়, 'description' ব্যবহার করো
        widgets = {
            'reason': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter reason'}),
            'description': forms.Textarea(attrs={'rows': 3, 'class': 'form-control', 'placeholder': 'Write details about this report...'}),
        }
