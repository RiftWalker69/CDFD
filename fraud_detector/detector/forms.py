from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user

class TransactionForm(forms.Form):
    distance_from_home = forms.FloatField(
        label='Distance from Home',
        min_value=0,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter distance from home'
        })
    )
    
    distance_from_last_transaction = forms.FloatField(
        label='Distance from Last Transaction',
        min_value=0,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter distance from last transaction'
        })
    )
    
    ratio_to_median_purchase_price = forms.FloatField(
        label='Ratio to Median Purchase Price',
        min_value=0,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter ratio to median purchase'
        })
    )
    
    used_chip = forms.ChoiceField(
        label='Used Chip',
        choices=[(1, 'Yes'), (0, 'No')],
        widget=forms.Select(attrs={
            'class': 'form-control'
        })
    )
    
    online_order = forms.ChoiceField(
        label='Online Order',
        choices=[(1, 'Yes'), (0, 'No')],
        widget=forms.Select(attrs={
            'class': 'form-control'
        })
    ) 