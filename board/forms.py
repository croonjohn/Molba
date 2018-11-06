from django import forms
from .models import (
    FreePost, ReportPost, ProposalPost, NoticePost, FreeComment, ReportComment, ProposalComment, NoticeComment
)

class FreePostForm(forms.ModelForm):

    class Meta:
        model = FreePost
        fields = ('title', 'content', 'image',)

class ReportPostForm(forms.ModelForm):

    class Meta:
        model = ReportPost
        fields = ('title', 'area', 'specific_area', 'image', 'content', )

class ProposalPostForm(forms.ModelForm):

    class Meta:
        model = ProposalPost
        fields = ('title', 'proposal_type','content', 'image',)

class NoticePostForm(forms.ModelForm):

    class Meta:
        model = NoticePost
        fields = ('title', 'notice_type','content', 'image',)

class FreeCommentForm(forms.ModelForm):

    class Meta:
        model = FreeComment
        fields = ('content',)

class ReportCommentForm(forms.ModelForm):

    class Meta:
        model = ReportComment
        fields = ('content',)

class ProposalCommentForm(forms.ModelForm):

    class Meta:
        model = ProposalComment
        fields = ('content',)

class NoticeCommentForm(forms.ModelForm):

    class Meta:
        model = NoticeComment
        fields = ('content',)





