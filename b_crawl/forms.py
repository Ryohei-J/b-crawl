from django import forms


class ScrapingForm(forms.Form):
    url = forms.URLField(
        label='', 
        required=True, 
        widget=forms.TextInput(attrs={'class': 'custom-component','placeholder': 'スレッドURL'})
    )

class ContactForm(forms.Form):
    name = forms.CharField(
        label='',
        max_length=50, 
        required=False,
        widget=forms.TextInput(attrs={'class': 'custom-component','placeholder': '名前'})
    )

    email = forms.EmailField(
        label='',
        required=False,
        widget=forms.TextInput(attrs={'class': 'custom-component','placeholder': 'Email'})
    )

    text = forms.CharField(
        label='',
        required=True,
        widget=forms.Textarea(attrs={'class': 'custom-component','placeholder': '問い合わせ内容'})
    )