from django.contrib import admin
from .models import (FreePost, ReportPost, ProposalPost, NoticePost, FreeComment, ReportComment, ProposalComment, NoticeComment
)
# Register your models here.

admin.site.register(FreePost)
admin.site.register(ReportPost)
admin.site.register(ProposalPost)
admin.site.register(NoticePost)

admin.site.register(FreeComment)
admin.site.register(ReportComment)
admin.site.register(ProposalComment)
admin.site.register(NoticeComment)