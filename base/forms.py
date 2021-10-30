from django import forms
from .models import Review, UserProfile

class ReviewForm(forms.ModelForm):

    class Meta:

        model = Review
        fields = ['name']

class UserProfileForm(forms.ModelForm):

    class Meta:

        model = UserProfile
        fields = ['display_name', 'delivery_address']