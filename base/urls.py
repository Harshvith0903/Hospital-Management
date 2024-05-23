from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login', views.user_login, name='user_login'),
    path('register', views.user_register, name='user_register'),
    path('logout', views.user_logout, name='logout'),
    path('doc_in_hospital', views.view_doc_and_hospital, name='doc_in_hospital'),
    path('view_hospitals', views.search_hospital, name='view_hospitals'),
    path('view_doctors', views.search_doctor, name='view_doctors'),
    path('create_emergency', views.appoint_emergency, name='create_emergency'),
    path('create_appointment', views.create_appointment, name='create_appointment'),
    path('list_appointments', views.list_appointment, name='list_appointments'),
    path('delete_appointment/<int:appointment_id>', views.delete_appointment, name='delete_appointment')
]
