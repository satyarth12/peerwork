from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include


from django.conf import settings
from django.conf.urls.static import static

from account import views as acc_views
from users import views as user_views
from search import views as search_views
from django.views import defaults as default_views

urlpatterns = [ 
    path('admin/', admin.site.urls),
    
    path('verify/', user_views.Verifying.as_view(), name='verify'),
       
    path('logout/', auth_views.LogoutView.as_view(template_name='blog/beforeloginhome.html'), name="logout"),
    path('',include('blog.urls')),
    path('',include('books.urls')),
    path('taggit_autosuggest/', include('taggit_autosuggest.urls')),
    path('grappelli/', include('grappelli.urls')),
    path('',include('users.urls')),
    path('',include('account.urls')),

    path('accounts/activate/<activation_key>',acc_views.activation_view, name='activation_view'),

    path('reset-password/',auth_views.PasswordResetView.as_view(template_name='users/password_reset.html'),name='reset_password'),
    path('reset-password-sent/',auth_views.PasswordResetDoneView.as_view(template_name='users/password_reset_done.html'),name='password_reset_done'),
    path('reset-password/<uidb64>/<token>',auth_views.PasswordResetConfirmView.as_view(template_name='users/password_reset_confirm.html'),name='password_reset_confirm'),
    path('reset-password-complete/',auth_views.PasswordResetCompleteView.as_view(template_name='users/password_reset_complete.html'),name='password_reset_complete'),


    path('students/', search_views.SearchView.as_view(), name="students"),
    path('', include('friends.urls')),
    
]




if settings.DEBUG:
	urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 
