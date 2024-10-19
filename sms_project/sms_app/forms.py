from django import forms

class SMSSendForm(forms.Form):
    to = forms.CharField(label='Phone Number', max_length=15)
    message = forms.CharField(widget=forms.Textarea, label='Message')