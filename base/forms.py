from django import forms
from .models import UserProfile, ReviewProduct

class UserProfileForm(forms.ModelForm):

    class Meta:

        model = UserProfile
        fields = ['display_name', 'delivery_address']

class ReviewProductForm(forms.ModelForm):

    class Meta:

        model = ReviewProduct
        fields = ['review']