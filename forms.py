import re
from django import forms
from markdownx.widgets import MarkdownxWidget

from .plugshop.forms import OrderForm as PlugshopOrderForm
from apps.shop.models import Product, ShippingType, Category


class CategoryAdminForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = '__all__'
        widgets = {
            'short_description': MarkdownxWidget(),
            'description': MarkdownxWidget(),
        }


class ProductAdminForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'
        widgets = {
            'short_description': MarkdownxWidget(),
            'description': MarkdownxWidget(),
        }


class OrderForm(PlugshopOrderForm):
    shipping_type = forms.ModelChoiceField(empty_label=None,
                        queryset=ShippingType.objects.filter(is_active=True))
    name = forms.CharField(required=True, error_messages={
                                'required': 'Enter Name'
                            })
    email = forms.EmailField(required=True, error_messages={
                                    'required': 'Show email'
                                })
    phone = forms.CharField(required=True, error_messages={
                                    'required': 'Enter the phone'
                                })
    
    def __require(self, name, error):
        value = self.cleaned_data.get(name, None)
        if len(value) == 0: 
            self.errors[name] = [error]
            
    def clean_name(self):
        name = self.cleaned_data.get('name').strip().split()
        shipping_type = self.cleaned_data.get('shipping_type')
        if shipping_type.require_zip_code and len(name) < 3:
            raise forms.ValidationError('Enter last name, first name and patronymic.')

        if len(name):
            self.cleaned_data['last_name']  = name[0]
            self.cleaned_data['first_name'] = " ".join(name[1:])
        else:
            raise forms.ValidationError('Enter your name')

        return " ".join(name)
        
    def clean(self):
        cleaned_data = self.cleaned_data
        shipping_type = cleaned_data.get('shipping_type')

        if shipping_type:
            if shipping_type.require_address:
                self.__require('address', 'Delivery address not specified')
            if shipping_type.require_zip_code:
                self.__require('zip_code', 'No index specified')
                self.__require('city', 'City not specified')

                zip_code = self.cleaned_data.get('zip_code', None)
                if re.search(r'^\d{6}$', zip_code) is None:
                    self.errors['zip_code'] = ['The index consists of 6 digits']
        return cleaned_data