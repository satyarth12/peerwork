from django.db import models
from taggit.managers import TaggableManager
from django.utils import timezone
from django.urls import reverse
from django.conf import settings
from django.db.models.signals import post_save, pre_save
from multiselectfield import MultiSelectField
from .validators import (validate_geeks2,validate_budget,validate_days,term)


import hashlib
import random
from django.utils.text import slugify


vis=(
	('Public','Public(All Students) - Recommended'),
	('Private','Private(Only to Students invited by you)')
	)


pro=(
	('Animation & Media', 'Animation & Media'),
	('Photography & Video','Photography & Video'),
	('Programming & Development', 'Programming & Development'),
	('Graphics & Design', 'Graphics & Design'),
	('Marketing', 'Marketing / Digital Marketing'),
	('Hospitality', 'Hospitality (Event/Hotel Management)'),
	('Soft Skills', 'Soft Skills'),
	('Customer Service', 'Customer Service'),
	('Legal','Law & Legals'),
	('Lifestyle','Gaming/Traveling/Cooking/Cultural and etc..')
	)

pay=(
	('NDA','Working Students must sign a Non-disclosure Agreement to work on your project. They agree to keep details discussed through private messages and files/documents/code confidential.'),
	('Urgent','Receive faster responses from skilled students and get your Project started within a day!'),
	('Recruiter','Our hands-on PRIME Recruitment service ensures you get the best students for your project. Our recruiters personally review all the proposals saving you time screening students\' proposals.')
	)

work=(
	('Chandigarh University','Chandigarh University'),
	('LPU','Lovely Professional University'),
	('All','Whole India')	
	)



mobility=(
	('Home','Home'),
	('Institute','Institute')
)

curr=(
	('INR','INR'),
	)


class Post(models.Model):
	Type=models.CharField(max_length=30,choices=pro, verbose_name="Category of the work")
	sub_type=TaggableManager(verbose_name="Expertise Criteria: ",help_text="Selecting this field out of the main Category will deduce the chance for this project of getting Requested")
	
	title=models.CharField(max_length=50,verbose_name='What is your project about?',validators =[validate_geeks2],help_text="Max Length : 50 chars", unique=True)
	
	role=models.TextField(verbose_name="Explain freelancer's role and requirements", validators =[validate_geeks2]) 

	days=models.IntegerField(verbose_name="Days required for project",validators=[validate_days])
	months=models.IntegerField(verbose_name="Months required for project")

	skills_required=models.CharField(blank=True,default='',max_length=500)

	benefits=models.TextField(max_length=1000,verbose_name="What are the other benefits for the employee student will gain from this project?")


	currency=models.CharField(max_length=20,choices=curr,default='INR',blank=True)
	budget=models.IntegerField(verbose_name="Fixed Budget ", help_text="- MIN INR 300", validators=[validate_budget])
	
	requirements=models.TextField(verbose_name="Explain project in detail", help_text=''' <br/>- Detailed explaination for your project. // Do not share any of your contact details. 
																				// Do not promote any third party services. // MIN word 60.
																				''', validators =[validate_geeks2])

	
	date_posted=models.DateTimeField(default=timezone.now)
	terms=models.BooleanField(default='True',verbose_name='I agree to the Terms & Conditions of Peerwork.in',validators=[term])

	slug=models.SlugField(unique=True,default="",max_length=200)

	in_progress=models.BooleanField(default=False,blank=True)
	accepted=models.BooleanField(default=False,blank=True)
	user=models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

	

	def __str__(self):
		return self.title	

	def get_absolute_url(self,**kwargs):
		return reverse('post-detail',kwargs={'slug':self.slug})

	def get_request_url(self,**kwargs):
		return reverse('friend-request',kwargs={'slug':self.slug})

	def get_api_request_url(self,**kwargs):
		return reverse('friend-api-request',kwargs={'slug':self.slug})

	@property
	def get_content_type(self):
		instance=self
		content_type=ContentType.objects.get_for_model(instance.__class__)
		return content_type
	


def pre_save_post_receiver(sender, instance, *args, **kwargs):
	short_slug=instance.Type+instance.title
	slug="%s" %(slugify(short_slug))
	instance.slug=slug

pre_save.connect(pre_save_post_receiver, sender=Post)



class SubmitForm(models.Model):
	project_user=models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,related_name="project_user")
	project_doer_user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name="project_doer_user")
	on_project=models.OneToOneField(Post,on_delete=models.CASCADE,related_name="on_project")

	request_submit=models.BooleanField(default=False,blank=True)
	granted=models.BooleanField(default=False,blank=True)
	reason=models.TextField(max_length=500,blank=True)

	def __str__(self):
		if self.request_submit:
			return "For {}, requested by {}".format(self.on_project, self.project_user)
		elif self.granted:
			return "For {}, time is granted by {}".format(self.on_project, self.project_doer_user)
		elif not self.request_submit:
			return "For {}, submission request cancelled and asked time by {}".format(self.on_project, self.project_doer_user) 




class RawProject(models.Model):
	project_name=models.ForeignKey(Post,on_delete=models.CASCADE,related_name="project_name")
	link=models.URLField(max_length=500,verbose_name="Project's GitHub Link")
	done=models.BooleanField(default=False,blank=True)

	def __str__(self):
	    return '{}, link : {}'.format(self.project_name.title,self.link)

	def save(self, *args, **kwargs):
	    super(RawProject,self).save(*args, **kwargs)