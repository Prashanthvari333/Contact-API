from django.urls import path
from . import views

urlpatterns = [
    path('spam/', views.get_spam_report_list, name='spam-report-list'),
    path('spam/<int:pk>/', views.get_spam_report_detail, name='spam-report-detail'),
    path('mark-spam', views.mark_as_spam, name='mark_as_spam'),
]