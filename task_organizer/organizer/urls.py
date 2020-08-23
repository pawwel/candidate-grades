# organizer URLS.py

from django.urls import path
from . import views

app_name = 'organizer'

urlpatterns =[
    path('api/add-mark/', views.CreateGrade.as_view(), name='mark'),
    path('json_view/', views.candidate_list,name='json_list'),
]
