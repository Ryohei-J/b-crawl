from django import forms


class ScrapingForm(forms.Form):
    url = forms.URLField(
        label='', 
        required=True, 
        widget=forms.TextInput(attrs={'class': 'custom-component','placeholder': 'スレッドURL'})
    )