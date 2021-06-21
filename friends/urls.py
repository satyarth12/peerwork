from django.urls import path
from . import views
from .views import (
	users_list, 
	profile_view, 
	#send_friend_request, 
	#cancel_friend_request,
	SendFriendRequest,
	CancelFriendRequest,
	accept_friend_request,
	delete_friend_request,
	cancel_order
	)

urlpatterns = [
    path(r'posted/projects/', views.users_list, name='list'),
    path(r'friend/<int:pk>', views.profile_view, name='invite'),

    path('post/<slug:slug>/project-request', views.SendFriendRequest, name='friend-request'),  
    path(r'friend/friend-request/cancel/<slug>', views.CancelFriendRequest,name='canel-request'),

    path(r'friend/friend-request/accept/<int:id>', views.accept_friend_request,name='accept-request'),
    path(r'friend/friend-request/delete/<int:id>', views.delete_friend_request),

    path(r'project/assignment/delete/<slug:slug>', views.cancel_order,name="cancel_order"),
] 