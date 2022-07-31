from django import forms
from .models import *


class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['name', 'phone']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'call-to-action__inner-name', 'placeholder': 'Имя'}),
            'phone': forms.TextInput(attrs={'class': 'call-to-action__inner-phone', 'placeholder': 'Номер телефона'}),
        }

