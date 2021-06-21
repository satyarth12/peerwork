from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.auth import get_user_model
from django.urls import reverse

from taggit.managers import TaggableManager
from blog.models import Post

from phone_field import PhoneField
from django.core.mail import send_mail

import random
import hashlib

from PIL import Image
from multiselectfield import MultiSelectField
from django.utils.safestring import mark_safe
from django.conf import settings
from django.db.models import Q
from django.utils import timezone

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.template.loader import render_to_string



class AccountQuerySet(models.QuerySet):
    def search(self,query=None):
        qs=self
        if query !="" and query is not None:
            or_lookup=(Q(first_name__icontains=query)|
                        Q(last_name__icontains=query)| 
                        Q(username__icontains=query)|
                        Q(professional_title__icontains=query)
                        )

            qs=qs.filter(or_lookup).distinct()
        return qs



class MyAccountManager(BaseUserManager):
	def create_user(self, email, username, first_name, password=None):
		if not email:
			raise ValueError('Users must have an email address')
		if not username:
			raise ValueError('Users must have a username')
		if not first_name:
			raise ValueError('Users must have a Name')



		user = self.model(
			email=self.normalize_email(email),
			username=username,
			first_name=first_name
		)

		user.set_password(password)
		user.save(using=self._db)
		return user

	def create_superuser(self, email, username, first_name, password):
		user = self.create_user(
			email=self.normalize_email(email),
			password=password,
			username=username,
			first_name=first_name
		)
		user.is_admin = True
		user.is_staff = True
		user.is_superuser = True
		user.save(using=self._db)
		return user

	def get_queryset(self):
		return AccountQuerySet(self.model, using=self._db)
    
	def search(self,query=None):   
		return self.get_queryset().search(query=query)



Mobility=(
	('Yes','Yes'),
	('No','No (Work Form Home)'),
	('Yes but not outstation','Yes but not outstation')
)

cities=(
	('Chandigarh','Chandigarh'),
	('Lucknow','Lucknow'),
	('Ambala','Ambala'),
	('Delhi','Delhi'),
	('Noida','Noida'),
	('Gurgaon','Gurgaon'),
	('Rohtak','Rohtak'),
	('Rest of India','Rest of India')
)
sex=(
	('Male','Male'),
	('Female','Female'),
	('Other','Other')
	)

exp=(
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

programs=(
		("Engineering","Engineering"),
		("Studies of Management","Studies of Management"),
		("Journalism And Mass Communication","Journalism And Mass Communication"),
		("Arts And Humanities","Arts And Humanities"),
		("Hotel & Hospitality Management","Hotel & Hospitality Management"),
		("School Of Legal Studies","School Of Legal Studies"),
		("(PhD) Doctor Of Philosophy","(PhD) Doctor Of Philosophy"),


	)	

class Account(AbstractBaseUser):
	email 					= models.EmailField(max_length=60, unique=True)
	username 				= models.CharField(max_length=30, unique=True)

	date_joined				= models.DateTimeField(verbose_name='date joined', auto_now_add=True)
	last_login				= models.DateTimeField(verbose_name='last login', auto_now=True)
	is_admin				= models.BooleanField(default=False)
	is_active				= models.BooleanField(default=True)
	is_staff				= models.BooleanField(default=False)
	is_superuser			= models.BooleanField(default=False)

	first_name				= models.CharField(max_length=100,verbose_name="First Name")
	last_name				= models.CharField(blank=True,max_length=100,verbose_name="Last Name")
	phone 					= models.CharField(max_length=13,blank=True, help_text='Contact phone number')

	gender					=models.CharField(blank=True,max_length=10,choices=sex,default="What is your gender?")

	image					=models.ImageField(blank=True,default='default.png',upload_to='profile_pics')

	
	member_from=models.DateTimeField(blank=True,default=timezone.now)


	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = ['username','first_name']

	objects = MyAccountManager()

	def __str__(self):
		return self.email

	def get_absolute_url(self,**kwargs):
		return reverse('user-posts',kwargs={'pk':self.pk})

	#def save(self, *args, **kwargs):#save method is being override of the profile model for resizing large profile pics
		#super(Account,self).save(*args, **kwargs) #super is used to acess the save method of the parent class

		img=Image.open(self.image.path)

		if img.height>300 or img.width>300:
			output_size=(300,300)
			img.thumbnail(output_size)
			img.save(self.image.path) #to override the initial image file


	# For checking permissions. to keep it simple all admin have ALL permissons
	def has_perm(self, perm, obj=None):
		return self.is_admin

	# Does this user have permission to view this app? (ALWAYS YES FOR SIMPLICITY)
	def has_module_perms(self, app_label):
		return True


class UserProfile(models.Model):
	user 					=models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	about_me				=models.TextField(blank=True,max_length=2000,default="")

	mobility 				=models.CharField(max_length=26,blank=True,choices=Mobility)

	rate 					=models.IntegerField(blank=True,default='0')

	professional_title 		=TaggableManager(help_text="Create your custom title tag, if not in the list.")

	experience				=models.CharField(blank=True,choices=exp,max_length=100)
	course					=models.CharField(blank=True,max_length=35,choices=programs)
	city					=models.CharField(blank=True,max_length=30,choices=cities)

	languages				=models.CharField(blank=True,max_length=500)

	github_username			=models.CharField(blank=True,max_length=100)

	def __str__(self):
		return f'{self.user.username} Informations'

	def save(self, *args, **kwargs):
		super(UserProfile,self).save(*args, **kwargs) 
		

	def get_absolute_url(self,**kwargs):
		return reverse('user-posts',kwargs={'pk':self.pk})





class EmailConfirmed(models.Model):
	user=models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	activation_key=models.CharField(max_length=200)
	confirmed=models.BooleanField(default=False)

	def __unicode__(self):
		return str(self.user.username)

	def __str__(self):
		return f'{self.user}'


	def activate_user_email(self):
		#send email and render a string
		activation_url="%s%s" %(settings.SITE_URL, reverse("activation_view",args=[self.activation_key]))
		context={
		"activation_key":self.activation_key,
		"activation_url":activation_url,
		}
		message=render_to_string("account/activation_message.txt",context)
		subject="Activate Your Email"
		print(message)
		self.email_user(subject,message,settings.DEFAULT_FROM_EMAIL)

	def email_user(self, subject, message, from_email=None, **kwargs):
		send_mail(subject, message, from_email, [self.user.email], **kwargs)


User=get_user_model()
@receiver(post_save,sender=User)
def user_created(sender, instance, created, *args, **kwargs):
	user=instance
	
	if created:
		email_confirmed, email_is_created=EmailConfirmed.objects.get_or_create(user=user)
		if email_is_created:
			short_hash=hashlib.sha1(str(random.random()).encode('utf-8')).hexdigest()[:5]
			base,domain=str(user.email).split("@")
			activation_key=hashlib.sha1((short_hash+base).encode('utf-8')).hexdigest()
			email_confirmed.activation_key=activation_key
			email_confirmed.save()
			email_confirmed.activate_user_email()

	else:
		instance.emailconfirmed.save()
			

		


class Review(models.Model):
	react=(
		('Satisfied','Satisfied'),
		('Moderate','Moderate'),
		('Not Satisfied','Not Satisfied'),
	)
	for_user=models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,related_name='for_user')
	by_user=models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,related_name='user')
	project=models.OneToOneField(Post,on_delete=models.CASCADE,related_name='review_project')

	reaction=models.CharField(max_length=15,choices=react,default='Satisfied')
	review=models.TextField(max_length=1000,blank=True)
	rating=models.IntegerField(default=1)

	create_at=models.DateTimeField(auto_now_add=True)

	def __unicode__(self):
		return self.user.username

	def __str__(self):
		return 'For {} - By {}. On project {}'.format(self.for_user, self.by_user, self.project)

	def get_absolute_url(self,**kwargs):
		return reverse('user-posts',kwargs={'pk':self.pk})






class BankDetail(models.Model):
	user=models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	acc_no=models.CharField(max_length=100,blank=True, verbose_name="Account Number")
	ifsc=models.CharField(max_length=50,blank=True,verbose_name="Bank IFSC Code")
	name=models.CharField(max_length=500,blank=True, verbose_name="Account Holder's Name")

	verified=models.BooleanField(default=False,blank=True)
	
	def __str__(self):
		return f'{self.user} BANK DETAILS'

	def save(self, *args, **kwargs):
		super(BankDetail,self).save(*args, **kwargs) 

	def create_bankdetail(sender,**kwargs):
		if kwargs['created']:
			user_bankdetail=BankDetail.objects.create(user=kwargs['instance'])

	def get_absolute_url(self):
		return reverse('wallet')