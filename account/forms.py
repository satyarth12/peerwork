from .models import Review
from django import forms
from account.models import Account, Review, UserProfile
from django.contrib.auth.forms import UserCreationForm	
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError


class ReviewForm(forms.ModelForm):
	class Meta:
		model=Review
		fields=['reaction','review','rating']



class UserRegisterForm(UserCreationForm):

	password1=forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Minimun 8 characaters'}),required=True,max_length=100,label='')
	password2=forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Confirm Password'}),required=True,max_length=100,label='Confirm Password')
	
	def clean_email(self):
		print(type(self.cleaned_data))
		User=get_user_model()
		email=self.cleaned_data.get('email')
		user_count=User.objects.filter(email=email).count()
		if user_count>0:
			raise forms.ValidationError("The email is already registered. Please reset your password")
		else:
			with open("djangoproject/disposable-email-provider-domains.txt",'r') as f:
				blacklist=f.read().splitlines()
			for disposable_email in blacklist:
				if disposable_email in email:
					raise forms.ValidationError("Please enter another Email(We consider it as spam)")
			return email
				


	class Meta():
		model=Account
		fields=['email','username','first_name','last_name','password1','password2']




class UserUpdateForm(forms.ModelForm):
	def clean_email(self):
		User=get_user_model()
		
		email=self.cleaned_data.get('email')

		user_count=User.objects.filter(email=email).count()
		if user_count>1:
			raise forms.ValidationError("The email is already registered.")
		else:
			with open("djangoproject/disposable-email-provider-domains.txt",'r') as f:
				blacklist=f.read().splitlines()
			for disposable_email in blacklist:
				if disposable_email in email:
					raise forms.ValidationError("Please enter another Email(We consider it as spam)")
			return email


	def clean_username(self):
		User=get_user_model()
		username=self.cleaned_data.get('username')
		username_count=User.objects.filter(username=username).count()

		if username_count>1:
			raise forms.ValidationError("The entered username already exists.")
		else:
			return username

	def clean_phone(self):
		phone=self.cleaned_data.get('phone')

		if len(phone)>10:
			raise forms.ValidationError("Please enter a valid phone number")
		else:
			return phone


	class Meta():
		model=Account
		fields=['image','email','username','first_name','last_name','phone','gender']




class UserProfileForm(forms.ModelForm):
	class Meta:
		model=UserProfile
		fields=['about_me','mobility','rate','professional_title','experience','course','city','languages','github_username']

	def clean(self):
		cleaned_data = super(UserProfileForm, self).clean()
		tn = self.cleaned_data.get('professional_title', [])
		if len(tn) > 3:
			self.add_error(None, ValidationError('Invalid number of tags', code='invalid'))

		return cleaned_data