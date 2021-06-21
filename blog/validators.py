from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
import re



def validate_geeks2(value):  
	regex = re.compile('[@_!#$%^&*<>?}{~:]')
	# and all(x.isnumeric()==False for x in value)
	if regex.search(value) == None:
		pass
	else:	
		raise ValidationError(
		    _('This field can only contain letters A-Z. Not any special characters or numbers.')
		)


def validate_budget(value):
	if value<300:
		raise ValidationError('The minimum budget should be at least INR 300')


def validate_days(value):
	if value>31:
		raise ValidationError('''Days limit is 31.
								Try converting it into Months and Days''')

def term(value):
	if value==False:
		raise ValidationError('Required Field')



def clean_email2(self):
		User=get_user_model()
		data = self.cleaned_data('email')
		if User.objects.filter(email=data).count() > 0:
			raise forms.ValidationError("We have a user with this user email-id")
		return data		


def tag_validation(value):
	new_value=value.split(',')
	for val in new_value:
		if all(x.lower()==False for x in val):
			raise ValidationError('Skill tags should be in small letters')