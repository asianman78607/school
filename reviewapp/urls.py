from . import views
from django.urls import path

urlpatterns = [
    path('save_excel/',views.savedata),
    path('header/',views.header),
    path('dev/',views.dev),
    path('get_img/',views.get_img),
    path('',views.home,),
    path('login_form/',views.login_form),
    path('login_form_validate/',views.login_form_validate),
    path('face_train/<prn>',views.face_train),
    path('face_train_save_img/<prn>',views.face_train_save_img),
    path('train',views.train),
    
    
]
