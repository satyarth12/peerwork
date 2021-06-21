from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from django.contrib import messages
# import stripe

from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Friend, FriendRequest, Invoice
from.forms import FriendRequestForm
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from blog.models import Post
from django.views.generic import RedirectView


post=Post.objects.all()
User = get_user_model()

def users_list(request):
    payment_pending_projects = Friend.objects.filter(admin_user=request.user,paid=False,completed=False)
    paid_projects=Friend.objects.filter(admin_user=request.user,paid=True,completed=False)
    completed_projects=Friend.objects.filter(admin_user=request.user,completed=True)
    all_projects=Post.objects.filter(user=request.user)
    context = {
        'payment_pending_projects': payment_pending_projects,
        'paid_projects':paid_projects,
        'completed_projects':completed_projects,
        'all_projects':all_projects
    }
    return render(request, "friends/home.html", context)



@login_required
def SendFriendRequest(request,slug):
    #slug=self.kwargs.get("slug")
    url=request.META.get('HTTP_REFERER')
    project = get_object_or_404(Post, slug=slug)
    url_=project.get_absolute_url()

    try:
        instance=Friend.objects.get(admin_user=project.user,
            doer_user=request.user,
            ongoing_project=project)

    except Friend.DoesNotExist:
        instance=None

    if instance is None:
        if request.method=="POST":
            form=FriendRequestForm(request.POST)
            form.instance.from_user=request.user
            form.instance.to_user=project.user
            form.instance.project=project
            messages.success(request, f"Applied for the project") 
            form.save()
            return HttpResponseRedirect(url)

    return HttpResponseRedirect(url)


@login_required
def CancelFriendRequest(request,slug):
    url=request.META.get('HTTP_REFERER')
    project = get_object_or_404(Post, slug=slug)
    frequest = FriendRequest.objects.filter(from_user=request.user, to_user=project.user,project=project).first()
    frequest.delete()
    return HttpResponseRedirect(url)


@login_required
def accept_friend_request(request, id):
    from_user = get_object_or_404(User, id=id)
    frequest = FriendRequest.objects.filter(from_user=from_user, to_user=request.user).first()
    work_id=frequest.slug
    ongoing_project=frequest.project
    
    project=Post.objects.filter(user=frequest.to_user,id=ongoing_project.id).first()

    try:
        instance=Friend.objects.get(admin_user=ongoing_project.user,
            doer_user=from_user,
            work_id=work_id,
            ongoing_project=ongoing_project)

    except Friend.DoesNotExist:
        instance=None

    try:
        other_requests=FriendRequest.objects.filter(project=ongoing_project)
    except:
        other_requests=None

    if instance is None:

        friend = Friend.objects.create(
            admin_user=ongoing_project.user,
            doer_user=from_user,
            work_id=work_id,
            ongoing_project=ongoing_project)
        
        project.accepted=True
        slug=friend.ongoing_project.slug
        project.slug=slug
        project.save()

        if other_requests is not None:
            other_requests.delete()
        if frequest:
            frequest.delete()
        

    return redirect('list')

@login_required
def delete_friend_request(request, id):
    url=request.META.get('HTTP_REFERER')
    from_user = get_object_or_404(User, id=id)
    frequest = FriendRequest.objects.filter(from_user=from_user, to_user=request.user).first()
    frequest.delete()
    return HttpResponseRedirect(url)



@login_required
def cancel_order(request,slug):
    url=request.META.get('HTTP_REFERER')
    project = get_object_or_404(Post, slug=slug)
    try:
        friend=Friend.objects.get(ongoing_project=project)
    except Friend.DoesNotExist:
        friend=None

    if friend is not None and friend.admin_user==request.user:
        project.accepted=False
        project.save()
        friend.delete()
        return HttpResponseRedirect(url)
    return HttpResponseRedirect(url)



@login_required
def profile_view(request,pk):
    pk_user=get_object_or_404(User, pk=pk)
    if pk_user==request.user:
        p = Friend.objects.filter(admin_user=pk_user).first()
        u = request.user
        sent_friend_requests = FriendRequest.objects.filter(from_user=u)
        rec_friend_requests = FriendRequest.objects.filter(to_user=u)

        #friends = p.friends.all()

        # is this user our friend
        button_status = 'none'
        #if p not in request.user.friend.friends.all():
            #button_status = 'not_friend'

            # if we have sent him a friend request
            #if len(FriendRequest.objects.filter(
                #from_user=request.user).filter(to_user=p.user)) == 1:
                    #button_status = 'friend_request_sent'

        context = {
            'u': u,
            'button_status': button_status,
            #'friends_list': friends,
            'sent_friend_requests': sent_friend_requests,
            'rec_friend_requests': rec_friend_requests
        }

        return render(request, "friends/profile.html", context)
    return redirect('blog-home')


def follow_user(request, user):
    user = User.objects.get(email=user)
    ...
    dofollow
    ...

    notify.send(request.user, recipient=user, actor=request.user
        ,verb='followed you.', nf_type='followed_by_one_user')

    return YourResponse




# @login_required
