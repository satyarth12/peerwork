import re
from django.shortcuts import render, redirect,Http404
from django.contrib import messages

from django.conf import settings

from django.http import JsonResponse,HttpResponseRedirect
from django.core import serializers
import json
import requests

from validate_email import validate_email 
from django.core.mail import send_mail, EmailMessage
from django.contrib.auth import get_user_model


from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, UserUpdateForm, UserProfileForm

from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View
from .models import UserProfile, Account, EmailConfirmed, BankDetail

from friends.models import Friend
from blog.models import Post

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth import login,authenticate,logout

from django.shortcuts import get_object_or_404

from django.urls import reverse
from blog.models import Post



SHA1_RE=re.compile('^[a-f0-9]{40}$')

def activation_view(request, activation_key):
	if SHA1_RE.search(activation_key):
		print("activation key is real")
		try:
			instance=EmailConfirmed.objects.get(activation_key=activation_key)
		
		except EmailConfirmed.DoesNotExist:
			instance=None
			raise Http404

		if instance is not None and not instance.confirmed:
			page_message="Confirmation Successful !!. Welcome"
			instance.confirmed=True
			instance.activation_key="Confirmed"
			instance.user.is_active=True
			instance.save()

		elif instance is not None and instance.confirmed:
			page_message="Already Confirmed"

		else:
			page_message=""
		context={

		}

		return redirect(request,"account/activation_complete.html",context)

	else:
		raise Http404




def loginpage(request):
    logout(request)
    username = password = ''
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(email=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                #user.emailconfirmed.activate_user_email()
                return redirect('blog-home')
            else:
            	print("Account is not active")
            	return redirect('login')
    return render(request,'users/login.html')


def register(request):
	logout(request)
	if 	request.method=='POST':
		form=UserRegisterForm(request.POST)
		if form.is_valid():
			user=form.save(commit=False)
			email=form.cleaned_data.get('email')
			username=form.cleaned_data.get('username') 
			password1=form.cleaned_data.get('password1')
			user.set_password(password1)
			user.save()
			account=authenticate(email=email,password=password1) 
		
			messages.success(request, f'''Your Account Has Been Created Succesfully.
										Please confirm your email now.''') 
			return redirect('login')
	
	else:		
		form=UserRegisterForm()
	return render(request,'users/register.html', {'form':form})  


class UsernameValidationView(View):
	def post(self,request):
		User=get_user_model()
		data=json.loads(request.body)
		username=data['username']

		if User.objects.filter(username=username).exists():
			return JsonResponse({'username_error': 'Sorry, the username already exists'}, status=409)


		return JsonResponse({'username_valid':True})



class EmailValidationView(View):
	def post(self,request):
		User=get_user_model()
		data=json.loads(request.body)
		email=data['email']

		if not validate_email(email):
			return JsonResponse({'email_error': 'Email is Invalid'}, status=400)

		if User.objects.filter(email=email).exists():
			return JsonResponse({'email_error': 'The Email is already in use'}, status=409)


		return JsonResponse({'email_valid':True})

		

@login_required
def profile2(request):
	
	if request.is_ajax and request.method=='POST':
		u_form=UserUpdateForm(request.POST,request.FILES,instance=request.user)  	
		all_users=get_user_model().objects.all()
		all_users2=get_user_model().objects.all()

		if u_form.is_valid():
			email=u_form.cleaned_data.get('email')
			username=u_form.cleaned_data.get('username')
	
			instance=u_form.save()

			ser_instance = serializers.serialize('json', [ instance, ])
			messages.success(request, f'Profile Updated Succesfully')

			#return JsonResponse({"instance": ser_instance}, status=200)
			return redirect('profile') 
	else:
		u_form=UserUpdateForm(instance=request.user)	
		all_users2=get_user_model().objects.all()
		#return JsonResponse({"error": u_form.errors}, status=400)
	
	projects=Post.objects.filter(user=request.user)	
	projects_count=Post.objects.filter(user=request.user).count()
	context={ 
	"u_form":u_form, 
	'all_users2':all_users2,
	'projects':projects,
	'projects_count':projects_count

	}
	return render(request, 'users/profile.html',context)



@login_required
def user_profile(request):
	if 	request.method=='POST':
		form=UserProfileForm(request.POST,instance=request.user.userprofile)
		if form.is_valid():
			instance=form.save() 
			ser_instance = serializers.serialize('json', [ instance, ])
			messages.success(request, f"Your Dashboard Has Been Updated Succesfully.") 
			return redirect('profile')
	else:		
		form=UserProfileForm(instance=request.user.userprofile)

	projects=Post.objects.filter(user=request.user)	
	projects_count=Post.objects.filter(user=request.user).count()
	
	context={ 
	"form":form, 	
	'projects':projects,
	'projects_count':projects_count

	}
	return render(request,'users/dashboard.html', context)



class BankView(LoginRequiredMixin,CreateView):

	model=BankDetail
	fields=['acc_no','ifsc','name']
	template_name='account/bank.html'

	def form_valid(self,form): 
		form.instance.user=self.request.user
		send_mail(
	    'New Bank Details added ',
	    '''Bank details has been added for {}.
	    Verify it at the backend'''.format(self.request.user),
	    settings.DEFAULT_FROM_EMAIL,
		[settings.DEFAULT_FROM_EMAIL],
	    fail_silently=False,
		)
		return super().form_valid(form)

	def get_context_data(self, **kwargs):
		name=self.request.user
		context=super(BankView,self).get_context_data(**kwargs)
		try:
			bank=BankDetail.objects.get(user=name)

		except BankDetail.DoesNotExist:
			bank=None

		if bank:
			context['bank']=bank
		context['project']=Friend.objects.filter(doer_user=name,paid_by_peerwork=False)
		return context


# class BankUpdateView(LoginRequiredMixin,UserPassesTestMixin,UpdateView):
#     model=BankDetail
#     fields=['acc_no','ifsc','name']
#     template_name='account/bank.html'
   
#     def form_valid(self,form):
#         form.instance.user=self.request.user
#         return super().form_valid(form)

#     def test_func(self): 
#         bank=self.get_object()
#         if self.request.user==bank.user:
#             return True
#         return False

#     def get_object(self):
#     	return get_object_or_404(BankDetail, pk=self.request.id)

#     def get_context_data(self, **kwargs):
#     	name=self.request.user
#     	context=super(BankView,self).get_context_data(**kwargs)
#     	try:
#     		bank=BankDetail.objects.get(user=name)
#     	except BankDetail.DoesNotExist:
#     		bank=None

#     	if bank:
#     		context['bank']=bank

#     	context['project']=Friend.objects.filter(doer_user=name,paid_by_peerwork=False)
#     	return context

	

@login_required
def withdrawl(request,slug):
	url=request.META.get('HTTP_REFERER')
	for_project=get_object_or_404(Post, slug=slug)
	friends=Friend.objects.filter(ongoing_project=for_project).first()

	if friends.paid_by_peerwork==False and friends.doer_user==request.user:
		if friends.completed==True and friends.paid==True:
			friends.paid_by_peerwork=True

			send_mail(
			'Regarding withdrawl',
			'{} has requested for withdrawl process for {} . Confirm this at backend.'.format(friends.doer_user, for_project),
			settings.DEFAULT_FROM_EMAIL,
			[settings.DEFAULT_FROM_EMAIL],
			fail_silently=False,
			)

			friends.save()


			send_mail(
			'Regarding withdrawl and money transfer',
			'''As per your withdrawl request, peerwork has initiated your transfer process.
			Money will be transfered into your given account details by 2 hours from now.
			Thankyou.''',
			settings.DEFAULT_FROM_EMAIL,
			[friends.doer_user.email],
			fail_silently=False,
			)

			return HttpResponseRedirect(url)
		return HttpResponseRedirect(url)
	return HttpResponseRedirect(url)