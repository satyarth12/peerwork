from django.db import models
from django.conf import settings
from django.db.models.signals import post_save, pre_save
from django.utils.text import slugify
from blog.models import Post
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
import random
import hashlib


class Friend(models.Model):
	admin_user=models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,null=True,related_name='admin_user')
	doer_user=models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,null=True,related_name='doer_user')
	work_id=models.CharField(max_length=2000,default="")
	ongoing_project=models.OneToOneField(Post,on_delete=models.CASCADE,related_name='ongoing_project',null=True)

	order_id=models.CharField(max_length=1000,default="No Payment")
	
	paid=models.BooleanField(default=False,blank=True)
	completed=models.BooleanField(default=False,blank=True)

	paid_by_peerwork=models.BooleanField(default=False,blank=True)
	
	def __str__(self):
		return f'{self.ongoing_project}'

	def get_absolue_url(self):
		return "/friend/{}".format(self.slug)

	def create_friend(sender,**kwargs):
		if kwargs['created']:
			user_friend=Friend.objects.create(user=kwargs['instance'])



class FriendRequest(models.Model):
	to_user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE, related_name='to_user',null=True)
	from_user=models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='from_user',null=True)
	slug=models.SlugField(unique=True,default="")
	project=models.ForeignKey(Post,on_delete=models.CASCADE,related_name='project',null=True)
	pitch=models.TextField(max_length=1000,verbose_name="Project Pitch")
	timestamp=models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return "From {}, to {}".format(self.from_user.username,self.to_user.username)

	def get_absolute_url(self):
		return reverse('invite',kwargs={'pk':self.pk})
	
def pre_save_frequest_receiver(sender, instance, *args, **kwargs):
	short_slug_hash=hashlib.sha1(str(random.random()).encode('utf-8')).hexdigest()[:5]
	base=str(instance.project)
	short_slug=hashlib.sha1((short_slug_hash+base).encode('utf-8')).hexdigest()
	slug="%s-%s" %((slugify(short_slug)),base)
	instance.slug=slug

pre_save.connect(pre_save_frequest_receiver, sender=FriendRequest)




class Invoice(models.Model):
 	user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE, related_name='invoice_user',null=True)
 	document = models.FileField(blank=True,upload_to='invoice_docs')
 	invoice_project=models.OneToOneField(Post,on_delete=models.CASCADE,related_name='invoice_project',null=True)
 	uploaded_at = models.DateTimeField(auto_now_add=True)

 	def __str__(self):
 		return "For project: {},  project/invoice user: {}".format(self.invoice_project,self.user)