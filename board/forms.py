from django import forms
from .models import (
    Nickname,
    FreePost, ReportPost, ProposalPost, NoticePost, 
    FreeComment, ReportComment, ProposalComment, NoticeComment,
    FreeImages, ReportImages, ProposalImages, NoticeImages
)
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import (
    authenticate, get_user_model, password_validation,
)
import unicodedata
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm

class FreePostForm(forms.ModelForm):

    class Meta:
        model = FreePost
        fields = ('title', 'image','content',)
        labels = {
            'title': '제목',
            'image': '이미지',
            'content': '내용',
        }
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': '50자 이하'}),
        }

class ReportPostForm(forms.ModelForm):

    class Meta:
        model = ReportPost
        fields = ('title', 'area', 'specific_area', 'image', 'content',)
        labels = {
            'title': '제목',
            'area': '지역',
            'specific_area': '상세 지역',
            'image': '증거 이미지(필수)',
            'content': '내용',
        }
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': '50자 이하'}),
            'specific_area': forms.TextInput(attrs={'placeholder': '30자 이하'}),
        }

class ProposalPostForm(forms.ModelForm):

    class Meta:
        model = ProposalPost
        fields = ('title', 'proposal_type', 'image', 'content',)
        labels = {
            'title': '제목',
            'proposal_type': '건의/신고',
            'image': '이미지',
            'content': '내용',
        }

        widgets = {
            'title': forms.TextInput(attrs={'placeholder': '50자 이하'}),
        }

class NoticePostForm(forms.ModelForm):

    class Meta:
        model = NoticePost
        fields = ('title', 'notice_type', 'image', 'content',)
        labels = {
            'title': '제목',
            'notice_type': '상단 고정 여부',
            'image': '이미지',
            'content': '내용',
        }

        widgets = {
            'title': forms.TextInput(attrs={'placeholder': '50자 이하'}),
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

class SearchForm(forms.Form):
    filter_content = forms.CharField(max_length=100)

class FreeImagesForm(forms.ModelForm):
    image = forms.ImageField(label="이미지")
    
    class Meta:
        model = FreeImages
        fields = ('image',)
        labels = {
            'image': '이미지'
        }

class ReportImagesForm(forms.ModelForm):
    image = forms.ImageField(label="증거 이미지")
    
    class Meta:
        model = ReportImages
        fields = ('image',)
        labels = {
            'image': '증거 이미지'
        }

class ProposalImagesForm(forms.ModelForm):
    image = forms.ImageField(label="이미지")
    
    class Meta:
        model = ProposalImages
        fields = ('image',)
        labels = {
            'image': '이미지'
        }

class NoticeImagesForm(forms.ModelForm):
    image = forms.ImageField(label="이미지")
    
    class Meta:
        model = NoticeImages
        fields = ('image',)
        labels = {
            'image': '이미지'
        }
class UsernameField(forms.CharField):
    def to_python(self, value):
        return unicodedata.normalize('NFKC', super().to_python(value))

class SignupForm(UserCreationForm):
    pass

class NicknameForm(forms.ModelForm):

    class Meta:
        model = Nickname
        fields = ('nickname',)
        labels = {
            'nickname': '닉네임'
        }

class ChangePasswordForm(PasswordChangeForm):
    pass