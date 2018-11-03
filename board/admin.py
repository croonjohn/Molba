from django.contrib import admin
from .models import FreePost, ReportPost, ProposalPost, NoticePost
# Register your models here.

admin.site.register(FreePost)
admin.site.register(ReportPost)
admin.site.register(ProposalPost)
admin.site.register(NoticePost)