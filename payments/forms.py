from django import forms

class checkoutForm(forms.Form):
    email = forms.EmailField(label='', required=True, widget=forms.TextInput(attrs={'placeholder': 'Enter your Email Here'}))
