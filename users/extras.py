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

from .forms import VerifyForm          
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login,authenticate,logout

from django.db.models import Q
from blog.models import Post
from account.models import Account, EmailConfirmed, CrudUser
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
	paginate_by=10
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
    


class EduListView(LoginRequiredMixin,ListView):
	def form_valid(self,form): #to avoid the problem of null user after submitting the form
		form.instance.user=self.request.user	#before submitting the form, take the instance and set the author as the current logged in user
		return super().form_valid(form)	
	model=Education
	template_name='users/education_posts.html' 	#<apps>/<model>_<viewtype>.html in the blog/urls 	#the name is used as default and it is used because the listview doesnt know what variable is to be called and looped for the display
	paginate_by=5 #pagination functionality in the website	
	def get_context_data(self, **kwargs):
		name=self.request.user
		context=super(EduListView,self).get_context_data(**kwargs)
		context['education_list']=Education.objects.filter(user=name)
		context['work_list'] = Work.objects.filter(users=name)
		context['projects_list'] = Projects.objects.filter(user=name)
		context['profile_list'] = Profile.objects.filter(user=name)
		context['preference_list'] = Preference.objects.filter(user=name)
		return context



class EduCreateView(LoginRequiredMixin,CreateView): #you need to login(if loged out) before submitting the new post form
	model=Education
	fields=['institution_type','institution_name','course','score','start_year','end_year'] #fields needed to be created by every user 

	def form_valid(self,form): #to avoid the problem of null user after submitting the form
		form.instance.user=self.request.user	#before submitting the form, take the instance and set the author as the current logged in user
		return super().form_valid(form) #running the valid form on the parent class and returning it
		#we will the reverse(in models.py) to return the full url to the route so that views can handle the redirect. we wont use redirect here

class EduUpdateView(LoginRequiredMixin,UserPassesTestMixin,UpdateView): #userpassestest will run a test to match if the current user is the same user of the "wannabe" update post
	model=Education
	fields=['institution_type','institution_name','course','score','start_year','end_year'] 
	def form_valid(self,form):
		form.instance.user=self.request.user
		return super().form_valid(form)

	def test_func(self):  #test
		education=self.get_object()
		if self.request.user==education.user:
			return True
		return False

class EduDeleteView(LoginRequiredMixin,UserPassesTestMixin,DeleteView):
	model=Education
	success_url='education/'
	fields=['institution_type','institution_name','course','score','start_year','end_year'] 
	def test_func(self):  #test
		education=self.get_object()
		if self.request.user==education.user:
			return True
		return False
	def get_success_url(self):
		return reverse('edu-home')







class WorkCreateView(LoginRequiredMixin,CreateView): 
	model=Work
	fields=['organisation','designation','description','From','To'] 

	def form_valid(self,form): 
		form.instance.users=self.request.user
		return super().form_valid(form)

class WorkUpdateView(LoginRequiredMixin,UserPassesTestMixin,UpdateView):
	model=Work
	fields=['organisation','designation','description','From','To'] 
	def form_valid(self,form):
		form.instance.users=self.request.user
		return super().form_valid(form)

	def test_func(self):  #test
		work=self.get_object()
		if self.request.user==work.users:
			return True
		return False

class WorkDeleteView(LoginRequiredMixin,UserPassesTestMixin,DeleteView):
	model=Work
	#template_name='users/work_form.html'
	success_url='education/' 
	def test_func(self):  #test
		work=self.get_object()
		if self.request.user==work.users:
			return True
		return False
	def get_success_url(self):
		return reverse('edu-home')







class ProjectsCreateView(LoginRequiredMixin,CreateView): 
	model=Projects
	fields=['project_title','project_description','project_link'] 

	def form_valid(self,form): 
		form.instance.user=self.request.user
		return super().form_valid(form)

class ProjectsUpdateView(LoginRequiredMixin,UserPassesTestMixin,UpdateView):
	model=Projects
	fields=['project_title','project_description','project_link'] 
	def form_valid(self,form):
		form.instance.user=self.request.user
		return super().form_valid(form)

	def test_func(self):  #test
		projects=self.get_object()
		if self.request.user==projects.user:
			return True
		return False

class ProjectsDeleteView(LoginRequiredMixin,UserPassesTestMixin,DeleteView):
	model=Projects
	success_url='education/' 
	def test_func(self):  #test
		projects=self.get_object()
		if self.request.user==projects.user:
			return True
		return False
	def get_success_url(self):
		return reverse('edu-home')







class ProfileCreateView(LoginRequiredMixin,CreateView): 
	model=Profile
	fields=['achievments','details'] 

	def form_valid(self,form): 
		form.instance.user=self.request.user
		return super().form_valid(form)

class ProfileUpdateView(LoginRequiredMixin,UserPassesTestMixin,UpdateView):
	model=Profile
	fields=['achievments','details'] 
	def form_valid(self,form):
		form.instance.user=self.request.user
		return super().form_valid(form)

	def test_func(self):  #test
		profile=self.get_object()
		if self.request.user==profile.user:
			return True
		return False

class ProfileDeleteView(LoginRequiredMixin,UserPassesTestMixin,DeleteView):
	model=Profile
	success_url='education/' 
	def test_func(self):  #test
		work=self.get_object()
		if self.request.user==profile.user:
			return True
		return False
	def get_success_url(self):
		return reverse('edu-home')





class PrefCreateView(LoginRequiredMixin,CreateView): 
	model=Preference
	fields=['freelancing'] 

	def form_valid(self,form): 
		form.instance.user=self.request.user
		return super().form_valid(form)

class PrefUpdateView(LoginRequiredMixin,UserPassesTestMixin,UpdateView):
	model=Preference
	fields=['freelancing'] 
	def form_valid(self,form):
		form.instance.user=self.request.user
		return super().form_valid(form)

	def test_func(self):  #test
		preference=self.get_object()
		if self.request.user==preference.user:
			return True
		return False

class PrefDeleteView(LoginRequiredMixin,UserPassesTestMixin,DeleteView):
	model=Preference
	success_url='education/' 
	def test_func(self):  #test
		preference=self.get_object()
		if self.request.user==preference.user:
			return True
		return False
	def get_success_url(self):
		return reverse('edu-home')


@login_required
def resume_list(request):
	name=request.user
	education_list=Education.objects.filter(user=name)
	work_list= Work.objects.filter(users=name)
	projects_list = Projects.objects.filter(user=name)
	profile_list= Profile.objects.filter(user=name)
	preference_list= Preference.objects.filter(user=name)

	context={
		'education_list'=education_list,
		'work_list'=work_list,
		'projects_list'=projects_list,
		'profile_list'=profile_list,
		'preference_list'=preference_list	
		}
	return render(request, 'users/resume_list.html', context)
    
def save_book_form(request, form, template_name):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
            books = Book.objects.all()
            data['html_book_list'] = render_to_string('books/includes/partial_book_list.html', {
                'books': books
            })
        else:
            data['form_is_valid'] = False
    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)


def book_create(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
    else:
        form = BookForm()
    return save_book_form(request, form, 'books/includes/partial_book_create.html')


def book_update(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
    else:
        form = BookForm(instance=book)
    return save_book_form(request, form, 'books/includes/partial_book_update.html')
    
def book_delete(request, pk):
    book = get_object_or_404(Book, pk=pk)
    data = dict()
    if request.method == 'POST':
        book.delete()
        data['form_is_valid'] = True  # This is just to play along with the existing code
        books = Book.objects.all()
        data['html_book_list'] = render_to_string('books/includes/partial_book_list.html', {
            'books': books
        })
    else:
        context = {'book': book}
        data['html_form'] = render_to_string('books/includes/partial_book_delete.html',
            context,
            request=request,
        )
    return JsonResponse(data)

