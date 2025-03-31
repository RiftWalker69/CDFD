from django import forms

class TransactionForm(forms.Form):
    distance_from_home = forms.FloatField(
        label='Distance from Home',
        min_value=0,
        required=True,
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    distance_from_last_transaction = forms.FloatField(
        label='Distance from Last Transaction',
        min_value=0,
        required=True,
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    ratio_to_median = forms.FloatField(
        label='Ratio to Median Purchase Price',
        min_value=0,
        required=True,
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    used_chip = forms.ChoiceField(
        label='Used Chip',
        choices=[(1, 'Yes'), (0, 'No')],
        required=True,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    online_order = forms.ChoiceField(
        label='Online Order',
        choices=[(1, 'Yes'), (0, 'No')],
        required=True,
        widget=forms.Select(attrs={'class': 'form-control'})
    )