from django.urls import path
from . import views

from .views import ProjectListView
                   

urlpatterns=[


    path('projects/',ProjectListView.as_view(), name='allproject'),
    
]
