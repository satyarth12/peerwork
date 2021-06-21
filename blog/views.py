from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponse,HttpResponseRedirect,JsonResponse

from django.core.files.base import ContentFile
from io import BytesIO
from django.core.files import File
from django.template.loader import get_template
from xhtml2pdf import pisa

from account.models import Account
from .models import Post, SubmitForm, RawProject
from .forms import PostForm, Submit, RawProjectForm
from django.views.decorators.csrf import csrf_exempt
import razorpay
from friends.forms import FriendRequestForm

from django.core.mail import send_mail, EmailMessage
from django.conf import settings
from users.models import Preference,Education,Work,Projects,Profile,Verify
from django.views.generic import RedirectView, ListView, DetailView, CreateView, UpdateView, DeleteView, View

from django.contrib.auth.decorators import login_required
from django.urls import reverse

from account.models import Account, EmailConfirmed, UserProfile, Review
from account.forms import ReviewForm
from friends.models import Friend, FriendRequest, Invoice
from taggit.models import Tag

from django.views.generic.edit import FormMixin
from django.template.loader import render_to_string


#function view
def Mainhome(request):
    return render(request, 'blog/beforeloginhome.html')



#in class view we have to only declare some variables but in the function view we have to explicitly pass the info and render that function
class PostListView(LoginRequiredMixin,ListView):
    def form_valid(self,form): #to avoid the problem of null user after submitting the form
        form.instance.user=self.request.user    #before submitting the form, take the instance and set the author as the current logged in user
        return super().form_valid(form) 
    def get_context_data(self, **kwargs):
        name=self.request.user
        #user=UserProfile.objects.get(user=name)

        context=super(PostListView,self).get_context_data(**kwargs)
        context['posts']=Post.objects.exclude(user=name).order_by('-id')[0:12]
        context['posts_rate']=Post.objects.exclude(user=name).order_by('-id')[0:12]
        context['verify'] = Verify.objects.filter(user=name)
        return context

    model=Post
    template_name='blog/home.html' 
    ordering=['-date_posted']       
        

    


@login_required
def user_detail(request,pk):
    current_user=get_object_or_404(Account, pk=pk)
    reviews = Review.objects.filter(for_user=current_user).order_by('-id')
    

    education_list=Education.objects.filter(user=current_user)
    work_list=Work.objects.filter(users=current_user)
    projects_list=Projects.objects.filter(user=current_user)
    profile_list=Profile.objects.filter(user=current_user)
    preference_list=Preference.objects.filter(user=current_user)

    context={
        'current_user':current_user,
        'reviews' : reviews,
        'education_list' : education_list,
        'work_list' : work_list,
        'projects_list' : projects_list,
        'profile_list' : profile_list,
        'preference_list' : preference_list,
        
    }

    return render(request,'blog/user_posts.html',context)





client=razorpay.Client(auth=('rzp_test_iQX9MSSRT24JZQ','Af7RFQHpMAnVA7rUWv7XZCYW'))
@login_required
def create_order(request,slug):
    current_project=get_object_or_404(Post, slug=slug)

    try:
        friends=Friend.objects.get(admin_user=current_project.user,ongoing_project=current_project)
    except Friend.DoesNotExist:
        friends=None

    context = {}
    if request.method == 'POST':
        print("INSIDE Create Order!!!")
        order_amount = current_project.budget
        product = current_project

        order_currency = 'INR'
        order_receipt = 'order_rcptid_11'
        notes = {
            'Shipping address': 'Bommanahalli, Bangalore'}

        # CREAING ORDER
        response = client.order.create(dict(amount=order_amount*100, currency=order_currency, receipt=order_receipt, notes=notes, payment_capture='0'))
        order_id = response['id']
        friends.order_id=response['id']
        friends.save()
        order_status = response['status']

        print(order_id)
        if order_status=='created':

            # Server data for user convinience
            context['product_id'] = product
            context['price'] = order_amount

            # data that'll be send to the razorpay for
            context['order_id'] = order_id

            if friends:
                context['email']=friends.doer_user
                context['phone']=friends.doer_user.phone
                context['name']=friends.doer_user.first_name + friends.doer_user.last_name
            
            
            return render(request, 'blog/confirm_order.html', context)

    return HttpResponse('<h1>Error in  create order function</h1>')


def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html  = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return result.getvalue()
    return None


@csrf_exempt
@login_required
def payment_status(request, *args, **kwargs):
    if request.method == "POST":
        a =  (request.POST)

        params_dict = {
        'razorpay_payment_id' : a['razorpay_payment_id'],
        'razorpay_order_id' : a['razorpay_order_id'],
        'razorpay_signature' : a['razorpay_signature']
        }

        print(a)

        order_id = ""
        for key , val in a.items():
            if key == "razorpay_order_id":
                order_id = val
                break

        # try:
        status = client.utility.verify_payment_signature(params_dict)
        
        user = Friend.objects.filter(order_id = order_id).first()
        user.paid = True
        user.save()

        live= Post.objects.filter(user=user.admin_user,id=user.ongoing_project.id).first()
        slug=user.ongoing_project.slug
        live.slug=slug
        live.in_progress=True
        send_mail(
            'Regarding money deposit for project {}'.format(user.ongoing_project),
            'Please check whether money deposition is done or not for project {} by {}'.format(user.ongoing_project,user.admin_user),
            settings.DEFAULT_FROM_EMAIL,
            [settings.DEFAULT_FROM_EMAIL,],
        )
        
        live.save() 

        data = {
        "admin_user": user.admin_user,
        "status":'Successfull',
        "phone": user.admin_user.phone,
        "email": user.admin_user.email,
        "project": live,
        'doer_user':user.doer_user,
        "invoice_id":user.order_id
        }
        pdf = render_to_pdf('blog/invoice.html', data)

        try:
            invoice_instance=Invoice.objects.filter(invoice_project=live).first()
        except Invoice.DoesNotExist:
            invoice_instance=None

        
        mail = EmailMessage(
            'Regarding Project Monet deposition.',
            "Congratulations!. You've successfully desposited Rs. {} (excluding peerwork charges) for the project {}. Your freelancer is {}.".format(live.budget,live,user.doer_user),
            settings.DEFAULT_FROM_EMAIL,
            [user.admin_user.email],
        )
        mail.attach('invoice.pdf', pdf)
        mail.send()

        return render(request, 'blog/order_summary.html',data)
    
        
        
    return render(request, "blog/order_summary.html")




class PostDetailView(LoginRequiredMixin,DetailView):

    model=Post
    slug_url_kwarg = 'slug'

    def get_context_data(self,**kwargs):
        current=self.request.user
        #project=kwargs
        context=super(PostDetailView,self).get_context_data(**kwargs)

        instance=EmailConfirmed.objects.filter(user=current)[0]
        project=context['post']

        try:
            reviews=Review.objects.get(by_user=self.request.user,project=project)
        except Review.DoesNotExist:
            reviews=None

        if reviews:
            context['reviews']=reviews
        
        try:
            friend_list=FriendRequest.objects.get(from_user=self.request.user,to_user=project.user,project=project)
        
        except FriendRequest.DoesNotExist:
            friend_list=None

        if friend_list:
            context['friend_list']=friend_list

        if Verify.objects.filter(user=current).exists() and instance is not None and instance.confirmed:
            ver = Verify.objects.filter(user=current)[0]
            if ver.check:
                context['sure']=instance


        if instance is not None and Verify.objects.filter(user=current).exists() and instance.confirmed:
            ver = Verify.objects.filter(user=current)[0]
            if not ver.check:
                context['only_email']=instance

        if instance is not None and Verify.objects.filter(user=current).exists() and instance.confirmed is False:
            ver = Verify.objects.filter(user=current)[0]
            if ver.check:
                context['only_verify']=ver

        if not Verify.objects.filter(user=current).exists():
            context['no_verify']=instance

        if not Verify.objects.filter(user=current).exists() and not EmailConfirmed.objects.filter(user=current).exists():
            context['nothing']=instance

        try:
            project_exists=Friend.objects.get(admin_user=project.user,ongoing_project=project)
        
        except Friend.DoesNotExist:
            project_exists=None

        if project_exists:
            if not project_exists.paid:
                context['project_exists']=project_exists

            else:
                context['project_exists_payment']=project_exists

        context['FriendRequestForm']=FriendRequestForm
        context['Submit']=Submit
        context['RawProjectForm']=RawProjectForm
        context['ReviewForm']=ReviewForm


        try:
            request_submission=SubmitForm.objects.get(on_project=project)
        
        except SubmitForm.DoesNotExist:
            request_submission=None

        context['request_submission']=request_submission


        try:
            final_submission=RawProject.objects.filter(project_name=project).latest('id')
        
        except RawProject.DoesNotExist:
            final_submission=None

        try:
            total_submission=RawProject.objects.filter(project_name=project)
        
        except RawProject.DoesNotExist:
            total_submission=None

        context['total_submission']=total_submission
        context['final_submission']=final_submission
        
        return context
    
 
   
class PostCreateView(LoginRequiredMixin,CreateView):
    model=Post
    form_class = PostForm

    def form_valid(self,form):
        form.instance.user=self.request.user 
        return super().form_valid(form) 



class PostUpdateView(LoginRequiredMixin,UserPassesTestMixin,UpdateView):
    model=Post
    form_class = PostForm
   
    def form_valid(self,form):
        form.instance.user=self.request.user
        return super().form_valid(form)

    def test_func(self): 
        post=self.get_object()
        if self.request.user==post.user:
            return True
        return False

    def get_context_data(self,**kwargs):
        current=self.request.user
        context=super(PostUpdateView,self).get_context_data(**kwargs)
        for key, value in context.items():
            if key =='post':
                project=context['post']
                break
        friend=Friend.objects.filter(ongoing_project=project)
        context['friend']=friend
        return context

class PostDeleteView(LoginRequiredMixin,UserPassesTestMixin,DeleteView):
    model=Post
    def test_func(self):  #test
        post=self.get_object()
        if self.request.user==post.user:
            return True
        return False

    def get_success_url(self):
        return reverse('blog-home')

def about(request):
    return render(request,'blog/about.html', {'title':'About'})




@login_required
def request_submission(request,slug):
    url=request.META.get('HTTP_REFERER')
    for_project=get_object_or_404(Post, slug=slug)
    friends=Friend.objects.filter(ongoing_project=for_project).first()

    try:
        instance=SubmitForm.objects.get(project_user=for_project.user,
            project_doer_user=friends.doer_user,
            on_project=for_project)

    except SubmitForm.DoesNotExist:
        instance=None


    try:
        instance2=RawProject.objects.filter(project_name=for_project)

    except RawProject.DoesNotExist:
        instance2=None


    if instance is None and instance2.count() != 2:
        if friends.admin_user==request.user:
            submit=SubmitForm.objects.create(
                project_user=request.user,
                project_doer_user=friends.doer_user,
                on_project=for_project,
                request_submit=True,
                reason="Hi!, I hope you've completed the project. Please submit it to the Peerwork platform for further verifications.")
            return HttpResponseRedirect(url)

    elif instance is not None and instance.project_user==request.user:
        if  instance2.count() != 2:
            instance.request_submit=True
            instance.granted=False
            instance.reason="Hi!, I hope you've completed the project. Please submit it to the Peerwork platform for further verifications."
            instance.save()
            return HttpResponseRedirect(url)
        return HttpResponseRedirect(url)

    elif instance is not None and instance.project_doer_user==request.user:
        if  instance2.count() != 2:
            instance.delete()
            if request.method=="POST":
                form=Submit(request.POST)
                form.instance.project_doer_user=request.user
                form.instance.project_user=for_project.user
                form.instance.on_project=for_project
                form.instance.request_submit=False
                form.instance.granted=False
                form.save()

            return HttpResponseRedirect(url)
        return HttpResponseRedirect(url)
    return HttpResponseRedirect(url)

@login_required
def grant_time(request, slug):
    url=request.META.get('HTTP_REFERER')
    for_project=get_object_or_404(Post, slug=slug)
    friends=Friend.objects.filter(ongoing_project=for_project).first()

    try:
        instance=SubmitForm.objects.get(project_user=for_project.user,
            project_doer_user=friends.doer_user,
            on_project=for_project)

    except SubmitForm.DoesNotExist:
        instance=None

    if instance and instance.project_user==request.user:
        if instance.request_submit==False and instance.granted==False:
            instance.granted=True
            send_mail(
                'Regarding {}'.format(for_project),
                'You have been granted more time from the project admin - {}, for the project'.format(for_project.user.username),
                settings.DEFAULT_FROM_EMAIL,
                [friends.doer_user.email],
                fail_silently=False,
            )
            instance.save()
        return HttpResponseRedirect(url)
    return HttpResponseRedirect(url)


@login_required
def final_submission(request,slug):
    url=request.META.get('HTTP_REFERER')
    raw_project=get_object_or_404(Post, slug=slug)
    friends=Friend.objects.filter(ongoing_project=raw_project).first()

    try:
        request_sub=SubmitForm.objects.get(on_project=raw_project,project_user=raw_project.user)

    except SubmitForm.DoesNotExist:
        request_sub=None

    if friends.doer_user==request.user:
        if request.method=="POST":
            form=RawProjectForm(request.POST)
            form.instance.project_name=raw_project
            form.save()
            request_sub.delete()
            try:
                project_submit=RawProject.objects.filter(project_name=raw_project).latest('id')

            except RawProject.DoesNotExist:
                project_submit=None

            send_mail(
                'Regarding project submission',
                '''A GitHub submission link has been send to you from {} for your project{}.
                    Github Link : {} '''.format(friends.doer_user.username,raw_project,project_submit.link),
                settings.DEFAULT_FROM_EMAIL,
                [friends.admin_user.email],
                fail_silently=False,
            )
        return HttpResponseRedirect(url)

    return HttpResponseRedirect(url)



@login_required
def release_payment(request,slug):
    url=request.META.get('HTTP_REFERER')
    for_project=get_object_or_404(Post,slug=slug)
    try:
        friends=Friend.objects.get(ongoing_project=for_project)
    except Friend.DoesNotExist:
        friends=None
    try:
        raw_project=RawProject.objects.filter(project_name=for_project).latest('id')
    except RawProject.DoesNotExist:
        raw_project=None

    if raw_project and friends:
        if friends.admin_user==request.user and friends.ongoing_project==raw_project.project_name:
            friends.completed=True
            friends.save()
            raw_project.done=True
            send_mail(
                'Regarding project submission',
                "Please check whether {} has requested for releasing payment for {} or not".format(friends.doer_user.username,for_project),
                settings.DEFAULT_FROM_EMAIL,
                [settings.DEFAULT_FROM_EMAIL],
                fail_silently=False,
            )
            raw_project.save()
            send_mail(
                'Regarding project payment',
                '''You payment has been released by {} for the project {}. 
                Kindly check your peerwork wallet for withdrawal process'''.format(friends.admin_user.username,for_project),
                settings.DEFAULT_FROM_EMAIL,
                [friends.doer_user.email],
                fail_silently=False,
            )
            return HttpResponseRedirect(url)
    return HttpResponseRedirect(url)




@login_required
def rating(request,slug):
    url=request.META.get('HTTP_REFERER')
    for_project=get_object_or_404(Post,slug=slug)
    friends=Friend.objects.filter(ongoing_project=for_project).first()
    if request.method=="POST" and friends.admin_user==request.user:
        review_form=ReviewForm(request.POST or None)
        if review_form.is_valid():
            review=request.POST.get('review')
            reaction=request.POST.get('reaction')
            rating=request.POST.get('rating')
            comment_form=Review.objects.create(
                    for_user=friends.doer_user,
                    by_user=request.user,
                    project=for_project,
                    reaction=reaction,
                    review=review,
                    rating=rating)
            comment_form.save()
            return HttpResponseRedirect(url)

    else:
        review_form=ReviewForm()

    return HttpResponseRedirect(url)


@login_required
def review_delete(request,pk):
    url=request.META.get('HTTP_REFERER')
    current_review=get_object_or_404(Review, pk=pk)
    review=Review.objects.filter(for_user=current_review.for_user,by_user=current_review.by_user,
                                reaction=current_review.reaction,review=current_review.review,
                                rating=current_review.rating).first()

    if request.user==current_review.by_user:
        review.delete()
        return HttpResponseRedirect(url)
    return HttpResponseRedirect(url)