from django import forms
from .models import Shipping


class ShippingForm(forms.Form):

    shipping = forms.ModelChoiceField(
        queryset=Shipping.objects.all(),
        empty_label=None
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].label = False
            self.fields[field].widget.attrs['class'] = 'shipping-form'
