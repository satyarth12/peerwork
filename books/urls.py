from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views
from .views import (education_delete,education_update,education_create,resume_list,
					work_delete,work_update,work_create,
					project_delete,project_update,project_create,
					profile_delete,profile_update,project_create,
					preference_delete,preference_update,preference_create,
					link_delete,link_update,link_create)


urlpatterns = [
	path(r'^(?P<pk>\d+)/delete/$', views.education_delete, name='education_delete'),
	path(r'^(?P<pk>\d+)/update/$', views.education_update, name='education_update'),
    path(r'^create/$', views.education_create, name='education_create'),


    path(r'^work/(?P<pk>\d+)/delete/$', views.work_delete, name='work_delete'),
	path(r'^work/(?P<pk>\d+)/update/$', views.work_update, name='work_update'),
    path(r'^work/create/$', views.work_create, name='work_create'),


    path(r'^project/(?P<pk>\d+)/delete/$', views.project_delete, name='project_delete'),
	path(r'^project/(?P<pk>\d+)/update/$', views.project_update, name='project_update'),
    path(r'^project/create/$', views.project_create, name='project_create'),



    path(r'^profile/(?P<pk>\d+)/delete/$', views.profile_delete, name='profile_delete'),
	path(r'^profile/(?P<pk>\d+)/update/$', views.profile_update, name='profile_update'),
    path(r'^profile/create/$', views.profile_create, name='profile_create'),


    path(r'^preference/(?P<pk>\d+)/delete/$', views.preference_delete, name='preference_delete'),
	path(r'^preference/(?P<pk>\d+)/update/$', views.preference_update, name='preference_update'),
    path(r'^preference/create/$', views.preference_create, name='preference_create'),


    path(r'^link/(?P<pk>\d+)/delete/$', views.link_delete, name='link_delete'),
	path(r'^link/(?P<pk>\d+)/update/$', views.link_update, name='link_update'),
    path(r'^link/create/$', views.link_create, name='link_create'),


    path(r'resume/', views.resume_list, name='resume'),


]	
if settings.DEBUG:
	urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 


	