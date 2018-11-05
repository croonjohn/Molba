from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('free/', views.freepost_list, name='freepost_list'),
    path('report/', views.reportpost_list, name='reportpost_list'),
    path('proposal/', views.proposalpost_list, name='proposalpost_list'),
    path('notice/', views.noticepost_list, name='noticepost_list'),
    path('free/<int:pk>', views.freepost_detail, name='freepost_detail'),
    path('report/<int:pk>', views.reportpost_detail, name='reportpost_detail'),
    path('proposal/<int:pk>', views.proposalpost_detail, name='proposalpost_detail'),
    path('notice/<int:pk>', views.noticepost_detail, name='noticepost_detail'),
]