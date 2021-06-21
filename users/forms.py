from django import forms
from account.models import Account
from django.contrib.auth.forms import UserCreationForm	
from .models import Profile, Preference, Verify,Education,Work,Projects,SampleLink
from django.contrib.auth import get_user_model



class VerifyForm(forms.ModelForm):
	class Meta():
		model=Verify
		fields=['image1','image2','name']



class WorkForm(forms.ModelForm):
	class Meta():
		model=Work
		fields=['organisation','designation','description','From','To']
		widgets = {
	            'From': forms.DateInput(attrs={'placeholder': 'year-month-date'}),
	            'To': forms.DateInput(attrs={'placeholder': 'year-month-date'})
	        }


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['achievments', 'details']




class ProjectForm(forms.ModelForm):
	class Meta():
		model=Projects
		fields=['project_title','project_description','project_link']




class EducationForm(forms.ModelForm):
    class Meta:
        model = Education
        fields = ('institution_type','institution_name','course','score','start_year','end_year', )
        widgets = {
	            'start_year': forms.DateInput(attrs={'placeholder': 'year-month-date'}),
	            'end_year': forms.DateInput(attrs={'placeholder': 'year-month-date'})
	        }



class PreferenceForm(forms.ModelForm):
	class Meta():
		model=Preference
		fields=['skillsets']



class SampleLinkForm(forms.ModelForm):
	class Meta():
		model=SampleLink
		fields=['blog_link','github_link','playstore_link','other_link']