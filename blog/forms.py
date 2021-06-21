from django import forms
from .models import Post, SubmitForm, RawProject
from django.core.exceptions import ValidationError 

class PostForm(forms.ModelForm):
	class Meta():
		model=Post
		fields=['Type','title','requirements','role','days','months','budget','terms','benefits','currency','sub_type','skills_required']
	
	def clean(self):
		cleaned_data = super(PostForm, self).clean()
		tn = self.cleaned_data.get('sub_type', [])
		if len(tn) > 1:
			self.add_error(None, ValidationError('Invalid number of tags', code='invalid'))

		return cleaned_data





class Submit(forms.ModelForm):
	class Meta():
		model=SubmitForm
		fields=['reason']


class RawProjectForm(forms.ModelForm):
	class Meta():
		model=RawProject
		fields=['link']