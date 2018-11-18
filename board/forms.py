from django import forms
from .models import (
    FreePost, ReportPost, ProposalPost, NoticePost, FreeComment, ReportComment, ProposalComment, NoticeComment
)
from django.contrib.auth.models import User

class FreePostForm(forms.ModelForm):

    class Meta:
        model = FreePost
        fields = ('title', 'content', 'image',)
        labels = {
            'title': '제목',
            'content': '내용',
            'image': '이미지'
        }

class ReportPostForm(forms.ModelForm):

    class Meta:
        model = ReportPost
        fields = ('title', 'area', 'specific_area', 'image', 'content',)
        labels = {
            'title': '제목',
            'area': '지역',
            'specific_area': '상세 지역',
            'image': '증거 이미지 (필수)',
            'content': '내용'
        }

class ProposalPostForm(forms.ModelForm):

    class Meta:
        model = ProposalPost
        fields = ('title', 'proposal_type','content', 'image',)
        labels = {
            'title': '제목',
            'proposal_type': '건의/신고',
            'content': '내용',
            'image': '이미지'
        }

class NoticePostForm(forms.ModelForm):

    class Meta:
        model = NoticePost
        fields = ('title', 'notice_type','content', 'image',)
        labels = {
            'title': '제목',
            'notice_type': '상단 고정 여부',
            'content': '내용',
            'image': '이미지'
        }

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

class UserForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ('username', 'nickname','password')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'150자 이내로 입력 가능합니다.'}),
            'nickname': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'150자 이내로 입력 가능합니다.'}),
            'password' : forms.PasswordInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'username': '아이디',
            'nickname': '닉네임',
            'password': '비밀번호'
        }

class UserChangeForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ('nickname','password')
        widgets = {
            'nickname': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'150자 이내로 입력 가능합니다.'}),
            'password' : forms.PasswordInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'nickname': '닉네임',
            'password': '비밀번호'
        }

class SearchForm(forms.Form):
    filter_content = forms.CharField(max_length=100)