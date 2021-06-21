from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import UserProfile,Account


@receiver(post_save,sender=Account) 
def create_userprofile(sender,instance,created,**kwargs):
	if created:
		UserProfile.objects.create(user=instance)
		print('UserProfile created')


@receiver(post_save,sender=Account)
def update_userprofile(sender,instance,created,**kwargs):
	if created==False:
		instance.userprofile.save()