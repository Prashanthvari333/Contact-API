from django.urls import path
from . import views

urlpatterns = [
    path('contacts/', views.contact_list, name='contact-list'),
    path('contacts/<int:pk>/', views.contact_detail, name='contact-detail'),
]