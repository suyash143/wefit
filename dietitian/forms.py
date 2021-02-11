from django import forms
from .models import Information


class ClientPicture(forms.ModelForm):
    class Meta:
        model = Information
        fields = '__all__'


class UpdatePicture(forms.ModelForm):
    class Meta:
        model = Information
        fields = ['payment_screenshot']