from bootstrap_datepicker_plus.widgets import DatePickerInput, TimePickerInput
from django import forms
from .models import Carton


class AddCartonAndProductForm(forms.ModelForm):
    class Meta:
        model = Carton
        fields = ['carton_id','product_name','product_quantity','product_price','production_date','expiry_date']
        widgets = {
            'production_date':DatePickerInput(format='%d-%m-%Y'),
            'expiry_date':DatePickerInput(format='%d-%m-%Y'),
        }


class PharmacistDetailsForm(forms.Form):
    details = forms.CharField(max_length=100,widget=forms.Textarea(attrs={'rows':10, 'cols':100}))
