from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='home'),
    path('free/', views.freepost_list, name='freepost_list'),
    path('report/', views.reportpost_list, name='reportpost_list'),
    path('proposal/', views.proposalpost_list, name='proposalpost_list'),
    path('notice/', views.noticepost_list, name='noticepost_list'),
    path('best/', views.bestpost_list, name='bestpost_list'),
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
    path('proposal/<int:pk>/comment/', views.add_proposalcomment_to_proposalpost, name='add_proposalcomment_to_proposalpost'),
    path('notice/<int:pk>/comment/', views.add_noticecomment_to_noticepost, name='add_noticecomment_to_noticepost'),
    path('signup/', views.signup, name='signup'),
    path('freepost_like/', views.freepost_like, name='freepost_like'),
    path('freepost_hate/', views.freepost_hate, name='freepost_hate'),
    path('reportpost_like/', views.reportpost_like, name='reportpost_like'),
    path('reportpost_hate/', views.reportpost_hate, name='reportpost_hate'),
    path('proposalpost_like/', views.proposalpost_like, name='proposalpost_like'),
    path('proposalpost_hate/', views.proposalpost_hate, name='proposalpost_hate'),
    path('noticepost_like/', views.noticepost_like, name='noticepost_like'),
    path('noticepost_hate/', views.noticepost_hate, name='noticepost_hate'),
    path('freecomment_like/', views.freecomment_like, name='freecomment_like'),
    path('freecomment_hate/', views.freecomment_hate, name='freecomment_hate'),
    path('reportcomment_like/', views.reportcomment_like, name='reportcomment_like'),
    path('reportcomment_hate/', views.reportcomment_hate, name='reportcomment_hate'),
    path('proposalcomment_like/', views.proposalcomment_like, name='proposalcomment_like'),
    path('proposalcomment_hate/', views.proposalcomment_hate, name='proposalcomment_hate'),
    path('noticecomment_like/', views.noticecomment_like, name='noticecomment_like'),
    path('noticecomment_hate/', views.noticecomment_hate, name='noticecomment_hate'),
    path('free/comment/<int:pk>/edit/', views.freecomment_edit, name='freecomment_edit'),
    path('report/comment/<int:pk>/edit/', views.reportcomment_edit, name='reportcomment_edit'),
    path('proposal/comment/<int:pk>/edit/', views.proposalcomment_edit, name='proposalcomment_edit'),
    path('notice/comment/<int:pk>/edit/', views.noticecomment_edit, name='noticecomment_edit'),
    path('free/comment/<int:pk>/remove/', views.freecomment_remove, name='freecomment_remove'),
    path('report/comment/<int:pk>/remove/', views.reportcomment_remove, name='reportcomment_remove'),
    path('proposal/comment/<int:pk>/remove/', views.proposalcomment_remove, name='proposalcomment_remove'),
    path('notice/comment/<int:pk>/remove/', views.noticecomment_remove, name='noticecomment_remove'),
    path('member/<member_pk>/posts/', views.memberpost_list, name='memberpost_list'),
    path('member/<member_pk>/comments/', views.membercomment_list, name='membercomment_list'),
    path('member/<member_pk>/info/', views.member_info, name='member_info'),
    path('member/<member_pk>/info/change', views.member_info_change, name='member_info_change'),
    path('search/', views.top_search_view, name='top_search_view'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)