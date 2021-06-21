from django.urls import path
from . import views
from .views import (PostListView, PostDetailView, PostCreateView, 
                    PostUpdateView, PostDeleteView, user_detail,
                    review_delete, create_order, payment_status, 
                    request_submission, final_submission, grant_time,
                    release_payment, rating, review_delete)

from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
	path('', views.Mainhome, name='blog-mainhome'),
    path('home/', PostListView.as_view(), name='blog-home'), #we can't pass the class normally, it has to be converted into an actual view

    path('user/75y68hf_/<int:pk>', views.user_detail, name='user-posts'),
    path('review/<int:pk>/delete', views.review_delete, name='review_delete'),

    path('post/new/', PostCreateView.as_view(), name='post-create'), #new template named as post_form is needed to be created for this because of django
    path('post/<slug:slug>/', PostDetailView.as_view(), name='post-detail'),  #pk is the primary key and the unique id for each post and int the the dataype of it
    path('post/<slug:slug>/update/', PostUpdateView.as_view(), name='post-update'), #update,create and delete are linked with the same post_form
    path('post/<slug:slug>/delete/', PostDeleteView.as_view(), name='post-delete'), #delete will ask for a template(post_confirm_delete) which will ask the user to delete the post or not
    
    path('confirm_order/<slug:slug>', views.create_order, name = 'create_order'),
    path('payment_status', views.payment_status, name = 'payment_status'),
    
    path('request/submission/<slug:slug>',views.request_submission, name='request_submission'),
    path('final/submission/<slug:slug>',views.final_submission, name='final_submission'),
    path('grant/time/<slug:slug>',views.grant_time, name='grant_time'),
    path('release/payment/<slug:slug>',views.release_payment, name='release_payment'),

    path('rating/<slug:slug>', views.rating, name='user-rating'),
    path('delete/rating/<int:pk>', views.review_delete, name='delete-rating'),

    path('about/', views.about, name='blog-about')
]