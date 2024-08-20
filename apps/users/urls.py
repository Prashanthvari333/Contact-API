from django.urls import path 
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('register', views.register, name='register'),
    path('login', views.signin, name='signin'),
    path('users/', views.user_list, name='user-list'),
    path('users/<int:pk>/', views.user_detail, name='user-detail'),
    path('user_contacts', views.get_contacts_by_user, name="get-contacts-by-user")
]
