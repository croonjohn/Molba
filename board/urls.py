from django.urls import path
from . import views
from django.conf import settings

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
    path('free/new', views.freepost_new, name='freepost_new'),
    path('report/new', views.reportpost_new, name='reportpost_new'),
    path('proposal/new', views.proposalpost_new, name='proposalpost_new'),
    path('notice/new', views.noticepost_new, name='noticepost_new'),
    path('free/<int:pk>/edit/', views.freepost_edit, name='freepost_edit'),
    path('report/<int:pk>/edit/', views.reportpost_edit, name='reportpost_edit'),
    path('proposal/<int:pk>/edit/', views.proposalpost_edit, name='proposalpost_edit'),
    path('notice/<int:pk>/edit/', views.noticepost_edit, name='noticepost_edit'),
    path('free/<int:pk>/remove/', views.freepost_remove, name='freepost_remove'),
    path('report/<int:pk>/remove/', views.reportpost_remove, name='reportpost_remove'),
    path('proposal/<int:pk>/remove/', views.proposalpost_remove, name='proposalpost_remove'),
    path('notice/<int:pk>/remove/', views.noticepost_remove, name='noticepost_remove'),
    path('free/<int:pk>/comment/', views.add_freecomment_to_freepost, name='add_freecomment_to_freepost'),
    path('report/<int:pk>/comment/', views.add_reportcomment_to_reportpost, name='add_reportcomment_to_reportpost'),
    path('proposal/<int:pk>/comment/', views.add_proposalcomment_to_proposalpost, name='add_proposalcommnet_to_proposalpost'),
    path('notice/<int:pk>/comment/', views.add_noticecomment_to_noticepost, name='add_noticecomment_to_noticepost'), 
]