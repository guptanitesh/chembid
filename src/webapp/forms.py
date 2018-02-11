from django import forms
from .models import Product
from .models import Mainproduct
from .models import ProductAvailability
from .models import ImpurityAvailability
from .models import Api,impurity
from django.contrib.admin import widgets
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

def clean_unique(form, field, exclude_initial=True, 
                 format="The %(field)s %(value)s has already been taken."):
    value = form.cleaned_data.get(field)
    if value:
        qs = form._meta.model._default_manager.filter(**{field:value})
        if exclude_initial and form.initial:
            initial_value = form.initial.get(field)
            qs = qs.exclude(**{field:initial_value})
        if qs.count() > 0:
            raise forms.ValidationError(format % {'field':field, 'value':value})
    return value


class ProductForm(forms.ModelForm):

	class Meta:
		model = Product
		fields = ('name', 'Cas', 'grade', 'quantity')

class MainproductForm(forms.ModelForm):

	class Meta:
		model = Mainproduct
		# components = forms.CharField(widget = forms.TextInput(attrs={'data-role': 'tagsinput'}))
		fields = ('seller', 'name', 'components', 'company_name', 'country', 'company_type')
		
class ApiForm(forms.ModelForm):

	class Meta:
		model = Api
		fields = ('name', 'mainproduct')

class SignUpForm(UserCreationForm):
    av_choices=(
        ('','Company Type'),
        ('Manufacturer','Manufacturer'),
        ('Trader','Trader'),
    )

    username = forms.CharField(max_length=30, required=True, widget=forms.TextInput(attrs={'placeholder' : 'Username'}))
    phone_no = forms.IntegerField( required=True,  widget=forms.TextInput(attrs={'placeholder' : 'Mobile'}))
    email = forms.EmailField(max_length=254,  widget=forms.TextInput(attrs={'placeholder' : 'Email'}))
    company_name = forms.CharField(max_length=100, required=True,  widget=forms.TextInput(attrs={'placeholder' : 'CompanyName'}))   
    company_type = forms.ChoiceField(choices = av_choices, required=True)
        
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'company_name', 'company_type', 'phone_no',)
        # fields = ('username', 'email','company_name', 'password1', 'password2', )

    def clean_username(self):
        return clean_unique(self, 'username') 

class ImpurityForm(forms.ModelForm):

    class Meta:
        model=impurity
        fields=('name','Cas','grade','quantity')


class ProductAvailabilityForm(forms.ModelForm):

    class Meta:
        model=ProductAvailability
        fields=('name', 'email', 'company_name', 'phone_no', 'product_name', 'Cas','grade','quantity')



class ImpurityAvailabilityForm(forms.ModelForm):

    class Meta:
        model=ImpurityAvailability
        fields=('name', 'email', 'company_name', 'phone_no', 'impurity_name','Cas','grade','quantity')
