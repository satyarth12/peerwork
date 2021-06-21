#from django.db.models.signals import post_save#
#from django.dispatch import receiver
#from .models import Preference, Verify
#from account.models import Account




#@receiver(post_save, sender=Account)
#def create_verify(sender,instance,created,**kwargs):
	#if created:
		#Verify.objects.create(user=instance)

#@receiver(post_save,sender=Account)
#def save_verify(sender,instance,**kwargs):
	#instance.verify.save()