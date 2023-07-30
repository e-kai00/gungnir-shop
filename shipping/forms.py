from django import forms
from .models import Shipping


class ShippingForm(forms.Form):

    shipping = forms.ModelChoiceField(
        queryset=Shipping.objects.all(), 
        empty_label=None
    )

    