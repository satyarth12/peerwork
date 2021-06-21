from django.db import models
from account.models import Account
from taggit.managers import TaggableManager

from django.conf import settings
from PIL import Image
from django.urls import reverse
from django.db.models.signals import post_save
from multiselectfield import MultiSelectField
from django.db.models import Q
from blog.validators import (validate_geeks2,validate_budget,validate_days,term)


class Profile(models.Model):
	user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
	achievments=models.CharField(max_length=1000,default="",validators=[validate_geeks2])
	details=models.TextField(max_length=1000,default="", help_text='Describe Your Achievments in a fun and brief way.',validators=[validate_geeks2])

	def __str__(self):
		return f'{self.user.username} Profile'


	def save(self, *args, **kwargs):#save method is being override of the profile model for resizing large profile pics
		super(Profile,self).save(*args, **kwargs) #super is used to acess the save method of the parent class

	def create_profile(sender,**kwargs):
		if kwargs['created']:
			user_profile=Profile.objects.create(user=kwargs['instance'])
			

	def get_absolute_url(self):
		return reverse('edu-home')





skill=(
		#marketing
		('1','Advertising'),
		('2','Marketing'),
		('3','Public Relations'),
		('4','Publicity'),
		('5','Sales'),
		('6','Performance Advertising'),
		('7','Social Media Advertising'),
		('8','SEO'),
		('9','Digital Marketing'),
		('10','Social Media Influencer'),


		#Hospitality
		('11','Event Management'),
		('12','Hotel Management'),
		('13','Cooking'),
		('14','Catering'),


		#Legal
		('15','Intellectual Property Law'),
		('16','Estate Planning Law'),
		('17','Bankruptcy Law'),
		('18','Corporate Law'),
		('19','Criminal Law'),
		('20','Employment Law'),
		('21','Tax'),
		('22','Civil Litigaion'),


		#Customer Service
		('23','Data Entry'),
		('24','Import and Export'),
		('25','Architecture'),
		('26','Interior Design'),
		('27','HR'),


		#Design
		('28','Adobe Photoshop'),
		('29','Adobe Illustrator'),
		('30','Adobe InDesign'),
		('31','Adobe Animate'),
		('32','Corel Draw'),
		('33','Adobe Flash'),
		('34','AutoCad'),
		('35','Sketch'),
		('36','Autodesk'),
		('37','Inkscape'),
		('38','Adobe XD'),
		('39','Invision Studio'),
		('40','Animation'),
		('41','Graphic Design'),
		('42','Photo Editing'),


		#General Skills
		('43','Communication Skill'),
		('44','Leadership'),
		('44','Entrepreneurship'),
		('45','Team Player'),


		#Finance
		('46','Accounting'),
		('47','Stock Marketing'),
		('48','Corporate Finance'),


		#Creative
		('49','Photography'),
		('50','Journalism'),
		('51','Content Writing'),
		('52','Blogging'),
		('53','Video Making'),
		('54','Acting'),
		('55','Music'),
		('56','Video Editing'),


		#Technical
		('57','Computer Networking'),
		('58','C'),
		('59','C++'),
		('60','Java'),
		('61','Javascript'),
		('61','Node JS'),
		('63','Angluar JS'),
		('64','Vue Js'),
		('65','Express JS'),
		('66','MySQL'),
		('67','PHP'),
		('68','HTML'),
		('69','CSS'),
		('70','Robotics'),
		('71','Ethical Hacking'),
		('72','Android Dev'),
		('73','Web Development'),
		('74','iOS Development'),
		('75','Wordpress'),
		('76','Python'),
		('77','R'),
		('78','Ruby on rails'),
		('79','React JS'),
		('80','React Native'),
		('81','C#'),
		('82','MongoDB'),
		('83','Rest API'),
		('84','Internet Of Things'),
		('85','Data Science'),
		('86','Docker'),
		('87','AWS'),
		('88','Machine Learning'),
		('89','Block Chain'),
		('90','Django')
	)


class PreferenceQuerySet(models.QuerySet):
	def search(self,query=None):
		qs=self
		if query !="" and query is not None:
			or_lookup=(Q(skillsets__icontains=query) 
						)

			qs=qs.filter(or_lookup).distinct()
		return qs

class PreferenceManager(models.Manager):
    def get_queryset(self):
    	return PreferenceQuerySet(self.model, using=self._db)
	
    def search(self,query=None):   
        return self.get_queryset().search(query=query)

class Preference(models.Model):
	user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)

	skillsets=TaggableManager(verbose_name="Skillsets",help_text="NOTE: Create your custom skills tag, if not in the list.")

	objects=PreferenceManager()

	def __str__(self):
		return f'{self.user.username} Preference'

	def save(self, *args, **kwargs):
		super(Preference,self).save(*args, **kwargs) 
		
	def create_preference(sender,**kwargs):
		if kwargs['created']:
			user_preference=Preference.objects.create(user=kwargs['instance'])
	

	def get_absolute_url(self):
		return reverse('edu-home')







class Verify(models.Model):
	user=models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
	name=models.CharField(max_length=300, verbose_name="College or educational institute name")
	image1=models.ImageField(default='', upload_to='student_docs',verbose_name="Front Side Of ID Card")
	image2=models.ImageField(default='', upload_to='student_docs',verbose_name="Back Side Of ID Card")
	check=models.BooleanField(default=False,blank=True)

	def __str__(self):
		return f'{self.user} Proofs'

	def save(self, *args, **kwargs):
		super(Verify,self).save(*args, **kwargs) 
		
	def create_verify(sender,**kwargs):
		if kwargs['created']:
			user_verify=Verify.objects.create(user=kwargs['instance'])
			
	def get_absolute_url(self):
		return reverse('verify')







courses=(
	('Engineering','Engineering'),
	('Management','Management'),
	('Animation & Multimedia','Animation & Multimedia'),
	('Health Science','Health Science'),
	('Agricultural Science','Agricultural Science'),
	('Arts & Humanities','Arts & Humanities'),
	('Hospitality','Hospitality'),
	('Other','Other')

)

education = (
    ('SE','Secondary Education'),
    ('SSE','Senior Secondary Education'),
    ('U','Undergraduation'),
    ('PG','Post Graduation'),
    ('Dip','Diploma'),
    ('Doc','Ph.D'),
    ('Self','Self Taught/Professional Certifications')
)
class Education(models.Model):
    user=models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    institution_type=models.CharField(max_length=4,choices=education)
    institution_name=models.CharField(max_length=100,default='')

    course=models.CharField(max_length=25,choices=courses)
    #board=models.CharField(max_length=100,default='')

    score=models.FloatField()
    start_year=models.DateField(auto_now_add=False,auto_now=False)
    end_year=models.DateField(auto_now_add=False,auto_now=False)
     
    def __str__(self):
        return f'{self.user.username} Education'

    def save(self, *args, **kwargs):#save method is being override of the profile model for resizing large profile pics
        super(Education,self).save(*args, **kwargs) #super is used to acess the save method of the parent class

    def create_preference(sender,**kwargs):
        if kwargs['created']:
            user_education=Education.objects.create(user=kwargs['instance'])

    def get_absolute_url(self):
    	return reverse('edu-home')

	





class Work(models.Model):
    users=models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    organisation=models.CharField(max_length=200,default='',validators=[validate_geeks2])
    designation=models.CharField(max_length=200,default='',validators=[validate_geeks2])
    description=models.TextField(max_length=1000,default='',validators=[validate_geeks2])
    From=models.DateField(auto_now_add=False,auto_now=False)
    To=models.DateField(auto_now_add=False,auto_now=False)
    def __str__(self):
        return f'{self.users.username} Work'

    def save(self, *args, **kwargs):#save method is being override of the profile model for resizing large profile pics
        super(Work,self).save(*args, **kwargs) #super is used to acess the save method of the parent class

    def create_preference(sender,**kwargs):
        if kwargs['created']:
            user_work=Work.objects.create(user=kwargs['instance'])

    def get_absolute_url(self):
    	return reverse('edu-home')






class Projects(models.Model):
	user=models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	project_title=models.CharField(blank=True,max_length=200,default="",validators=[validate_geeks2],verbose_name='Project Title')
	#project_image=models.ImageField(default='',upload_to='images',verbose_name="Sample of your project")
	project_description=models.TextField(blank=True,max_length=500,default="")
	project_link=models.URLField(blank=True,max_length=200,help_text="Only GitHub Link is Accepted")

	def __str__(self):
	    return f'{self.user.username} Projects'


	def save(self, *args, **kwargs):#save method is being override of the profile model for resizing large profile pics
	    super(Projects,self).save(*args, **kwargs) #super is used to acess the save method of the parent class


	def create_projects(sender,**kwargs):
	    if kwargs['created']:
	        user_projects=Projects.objects.create(user=kwargs['instance'])


	def get_absolute_url(self):
		return reverse('edu-home')



class SampleLink(models.Model):
	user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
	blog_link=models.URLField(blank=True,max_length=200)
	github_link=models.URLField(blank=True,max_length=200)
	playstore_link=models.URLField(blank=True,max_length=200)
	other_link=models.URLField(blank=True,max_length=200)


	def __str__(self):
	    return f'{self.user.username} SampleLink'


	def save(self, *args, **kwargs):
	    super(SampleLink,self).save(*args, **kwargs)


	def create_samplelink(sender,**kwargs):
	    if kwargs['created']:
	        user_samplelink=SampleLink.objects.create(user=kwargs['instance'])