from django import forms


class ScrapingForm(forms.Form):
    url = forms.URLField(
        label='', 
        required=True, 
        widget=forms.TextInput(attrs={'class': 'custom-component','placeholder': 'スレッドURL'})
    )

class ContactForm(forms.Form):
    name = forms.CharField(
        max_length=50, 
        required=False
    )

    email = forms.EmailField(
        required=False
    )

    text = forms.CharField(widget=forms.Textarea)