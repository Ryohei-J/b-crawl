from django import forms


class ScrapingForm(forms.Form):
    url = forms.URLField(label='URL', required=True)