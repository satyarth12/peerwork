from django import forms
from .models import FriendRequest



class FriendRequestForm(forms.ModelForm):
	pitch=forms.CharField(widget=forms.Textarea(attrs={'class':'form-control','placeholder':'For eg: I will complete this project in X days or Y months and i have such such skills. '}),required=True,max_length=1000,label='')
	class Meta():
		model=FriendRequest
		fields=['pitch']

