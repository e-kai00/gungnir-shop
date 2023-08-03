from django import forms


class ApplyCouponForm(forms.Form):

    code = forms.CharField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].label = False
            self.fields[field].widget.attrs['class'] = 'coupon_form'
