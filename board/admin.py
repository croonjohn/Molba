from django.contrib import admin
from .models import (
    Nickname,
    FreePost, ReportPost, ProposalPost, NoticePost, 
    FreeComment, ReportComment, ProposalComment, NoticeComment,
    FreeImages, ReportImages, ProposalImages, NoticeImages,
    Notification
)
# Register your models here.

admin.site.register(Nickname)

admin.site.register(FreePost)
admin.site.register(ReportPost)
admin.site.register(ProposalPost)
admin.site.register(NoticePost)

admin.site.register(FreeComment)
admin.site.register(ReportComment)
admin.site.register(ProposalComment)
admin.site.register(NoticeComment)

admin.site.register(FreeImages)
admin.site.register(ReportImages)
admin.site.register(ProposalImages)
admin.site.register(NoticeImages)

admin.site.register(Notification)