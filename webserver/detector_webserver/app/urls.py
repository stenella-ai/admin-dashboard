from django.urls import path, re_path
from app import views

urlpatterns = [
    re_path(r'^.*\.html', views.gentella_html, name='gentella'),
    path('', views.index, name='index'),
]
