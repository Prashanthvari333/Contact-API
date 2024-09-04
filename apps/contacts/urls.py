from django.urls import path
from . import views

urlpatterns = [
    path('add_contact',views.add_contact, name = 'add-contact'),
    path('contacts/', views.get_contact_list, name='contact-list'),
    path('contacts/<int:pk>/', views.contact_details, name='contact-detail'),
    path('search-contacts/', views.get_search_contacts, name='search_contacts'),
    path('search/<str:phone_number>/<int:id>', views.get_details_by_number,name = 'get_details_by_number')
]