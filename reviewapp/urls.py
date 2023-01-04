from . import views
from django.urls import path

urlpatterns = [
    path('',views.home,name="home"),
    path('header/',views.header),
    path('get_img/',views.get_img),
    
    
]
