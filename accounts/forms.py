from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from accounts.models import (Users,Category,Product,Invoice)
# Create your model forms here
class userForm(forms.ModelForm):
	 
	class Meta:
		model = Users
		fields = ('address','city','contactno','gstn')
class CategoryForm(forms.ModelForm):
	class Meta:
		model = Category
		fields = '__all__'	
#('A_FullName','A_EmailId',' A_passwd',' A_city','A_contactno','A_Profile')
class ProductForm(forms.ModelForm):
	 
	class Meta:
		model = Product
		fields = '__all__'		
class CreateInvoiceForm(forms.ModelForm):
	
	class Meta:
		model = Invoice
		fields = ('address','payment_mode')     		
