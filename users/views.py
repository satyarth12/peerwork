from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth import get_user_model

from django.http import JsonResponse
from django.core import serializers
import json

from django.template.loader import render_to_string

from validate_email import validate_email 

from django.core.mail import send_mail, EmailMessage

from .forms import VerifyForm, EducationForm    
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login,authenticate,logout

from django.db.models import Q
from blog.models import Post
from account.models import Account, EmailConfirmed
from .models import Preference,Education,Work,Projects,Profile,Verify


from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse


class ProjectListView(LoginRequiredMixin,ListView):
	def form_valid(self,form): 
		form.instance.user=self.request.user	
		return super().form_valid(form)	
	
	model=Post
	template_name='users/allproject.html' 	
	# paginate_by=10
	count = 0
	def get_context_data(self,*args,**kwargs):
		name=self.request.user
		qs= Post.objects.exclude(user=name)

		project_query=self.request.GET.get('project')

		if project_query !="" and project_query is not None:
			qs=qs.filter(Q(Type__icontains=project_query)| 
				Q(title__icontains=project_query)| 
				Q(skills_required__icontains=project_query)|
				Q(budget__icontains=project_query))


		context=super(ProjectListView,self).get_context_data(*args,**kwargs)
		
		context['queryset']=qs
		context['count'] = self.count or 0
		context['query'] = self.request.GET.get('project')

		return context







class Verifying(LoginRequiredMixin,CreateView): 
  model=Verify
  fields=['image1','image2','name'] 

  def form_valid(self,form): 
    form.instance.user=self.request.user
    return super().form_valid(form)

  def get_context_data(self, **kwargs):
    name=self.request.user
    context=super(Verifying,self).get_context_data(**kwargs)
    context['is_verify']=Verify.objects.filter(user=name)
    return context
    

