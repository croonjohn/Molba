from .models import (
    Nickname,
    FreePost, ReportPost, ProposalPost, NoticePost, 
    FreeComment, ReportComment, ProposalComment, NoticeComment,
    FreeImages, ReportImages, ProposalImages, NoticeImages,
    Notification
)
from .forms import (
    FreePostForm, ReportPostForm, ProposalPostForm, NoticePostForm,
    FreeCommentForm, ReportCommentForm, ProposalCommentForm, NoticeCommentForm,
    FreeImagesForm, ReportImagesForm, ProposalImagesForm, NoticeImagesForm,
    SignupForm, NicknameForm, ChangePasswordForm,
)
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import login, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Q
from django.forms import modelformset_factory
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_POST
try:
    from django.utils import simplejson as json
except ImportError:
    import json
from hitcount.models import HitCount
from hitcount.views import HitCountMixin
from itertools import chain
import operator

def freepost_list(request):
    freepost_listing = FreePost.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')

    filter_content = request.GET.get('q', '')
    filter_type = request.GET.get('search-option', '')

    if filter_content: 
        if filter_type == "title":
            freepost_listing = freepost_listing.filter(title__icontains=filter_content)
        elif filter_type == "content":
            freepost_listing = freepost_listing.filter(content__icontains=filter_content)
        elif filter_type == "title-content":
            freepost_listing = sorted(
                chain(
                    FreePost.objects.filter(title__icontains=filter_content),
                    FreePost.objects.filter(content__icontains=filter_content),
                ),
                key=lambda post: post.published_date, reverse=True
            )
            freepost_listing = sorted(list(set(freepost_listing)), key=lambda post: post.published_date, reverse=True)
        else:
            freepost_listing = freepost_listing.filter(author_nickname__icontains=filter_content)
    
    notice_tops = NoticePost.objects.filter(notice_type=1, published_date__lte=timezone.now()).order_by('-published_date')
    paginator = Paginator(freepost_listing, 20)
    page = request.GET.get('page')
    freeposts = paginator.get_page(page)
    return render(request,'board/freepost_list.html', {'freeposts': freeposts, 'notice_tops': notice_tops, 'q': filter_content, 'filter_type': filter_type})

def reportpost_list(request):
    area_for_search = {
        '서울': 'SE', 
        '인천': 'IC', 
        '경기': 'GG', 
        '대전': 'DJ', 
        '세종': 'SJ', 
        '충북': 'CB', 
        '충남': 'CN', 
        '강원': 'GW', 
        '광주': 'GJ', 
        '전북': 'JB', 
        '전남': 'JN', 
        '부산': 'BS', 
        '대구': 'DG', 
        '울산': 'US', 
        '경북': 'GB', 
        '경남': 'GN', 
        '제주': 'JJ'
    }

    reportpost_listing = ReportPost.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')

    filter_content = request.GET.get('q', '')
    filter_type = request.GET.get('search-option', '')

    if filter_content: 
        if filter_type == "area":
            reportpost_listing = reportpost_listing.filter(area__icontains=area_for_search[filter_content])
        elif filter_type == "specific-area":
            reportpost_listing = reportpost_listing.filter(specific_area__icontains=filter_content)
        elif filter_type == "title":
            reportpost_listing = reportpost_listing.filter(title__icontains=filter_content)
        elif filter_type == "content":
            reportpost_listing = reportpost_listing.filter(content__icontains=filter_content)
        elif filter_type == "title-content":
            reportpost_listing = sorted(
                chain(
                    ReportPost.objects.filter(title__icontains=filter_content),
                    ReportPost.objects.filter(content__icontains=filter_content),
                ),
                key=lambda post: post.published_date, reverse=True
            )
            reportpost_listing = sorted(list(set(reportpost_listing)), key=lambda post: post.published_date, reverse=True)
        else:
            reportpost_listing = reportpost_listing.filter(author_nickname__icontains=filter_content)
    
    notice_tops = NoticePost.objects.filter(notice_type=1, published_date__lte=timezone.now()).order_by('-published_date')
    paginator = Paginator(reportpost_listing, 20)
    page = request.GET.get('page')
    reportposts = paginator.get_page(page)
    return render(request,'board/reportpost_list.html', {'reportposts': reportposts, 'notice_tops': notice_tops, 'q': filter_content, 'filter_type': filter_type})

def proposalpost_list(request):
    proposalpost_listing = ProposalPost.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')

    filter_content = request.GET.get('q', '')
    filter_type = request.GET.get('search-option', '')

    if filter_content: 
        if filter_type == "title":
            proposalpost_listing = proposalpost_listing.filter(title__icontains=filter_content)
        elif filter_type == "content":
            proposalpost_listing = proposalpost_listing.filter(content__icontains=filter_content)
        elif filter_type == "title-content":
            proposalpost_listing = sorted(
                chain(
                    ProposalPost.objects.filter(title__icontains=filter_content),
                    ProposalPost.objects.filter(content__icontains=filter_content),
                ),
                key=lambda post: post.published_date, reverse=True
            )
            proposalpost_listing = sorted(list(set(proposalpost_listing)), key=lambda post: post.published_date, reverse=True)
        else:
            proposalpost_listing = proposalpost_listing.filter(author_nickname__icontains=filter_content)
    
    notice_tops = NoticePost.objects.filter(notice_type=1, published_date__lte=timezone.now()).order_by('-published_date')
    paginator = Paginator(proposalpost_listing, 20)
    page = request.GET.get('page')
    proposalposts = paginator.get_page(page)
    return render(request,'board/proposalpost_list.html', {'proposalposts': proposalposts, 'notice_tops': notice_tops, 'q': filter_content, 'filter_type': filter_type})

def noticepost_list(request):
    noticepost_listing = NoticePost.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')

    filter_content = request.GET.get('q', '')
    filter_type = request.GET.get('search-option', '')

    if filter_content: 
        if filter_type == "title":
            noticepost_listing = noticepost_listing.filter(title__icontains=filter_content)
        elif filter_type == "content":
            noticepost_listing = noticepost_listing.filter(content__icontains=filter_content)
        elif filter_type == "title-content":
            noticepost_listing = sorted(
                chain(
                    NoticePost.objects.filter(title__icontains=filter_content),
                    NoticePost.objects.filter(content__icontains=filter_content),
                ),
                key=lambda post: post.published_date, reverse=True
            )
            noticepost_listing = sorted(list(set(noticepost_listing)), key=lambda post: post.published_date, reverse=True)
        else:
            noticepost_listing = noticepost_listing.filter(author_nickname__icontains=filter_content)
    
    notice_tops = NoticePost.objects.filter(notice_type=1, published_date__lte=timezone.now()).order_by('-published_date')
    paginator = Paginator(noticepost_listing, 20)
    page = request.GET.get('page')
    noticeposts = paginator.get_page(page)
    return render(request,'board/noticepost_list.html', {'noticeposts': noticeposts, 'notice_tops': notice_tops, 'q': filter_content, 'filter_type': filter_type})

def bestpost_list(request):
    bestpost_listing = sorted(
        chain(
            FreePost.objects.all(),
            ReportPost.objects.all(),
            ProposalPost.objects.all(),
            NoticePost.objects.all()),
        key=lambda post: post.published_date, reverse=True)
    bestpost_listed = [post for post in bestpost_listing if post.likes_minus_hates >= 15]
    notice_tops = NoticePost.objects.filter(notice_type=1, published_date__lte=timezone.now()).order_by('-published_date')
    paginator = Paginator(bestpost_listed, 20)
    page = request.GET.get('page')
    bestposts = paginator.get_page(page)
    return render(request, 'board/bestpost_list.html', {'bestposts': bestposts, 'notice_tops': notice_tops})

@login_required
def memberpost_list(request, member_pk):
    member = User.objects.get(pk=member_pk)
    memberpost_listed = sorted(
        chain(
            FreePost.objects.filter(author=member),
            ReportPost.objects.filter(author=member),
            ProposalPost.objects.filter(author=member),
            NoticePost.objects.filter(author=member)),
        key=lambda post: post.published_date, reverse=True)
    paginator = Paginator(memberpost_listed, 20)
    page = request.GET.get('page')
    memberposts = paginator.get_page(page)
    return render(request, 'board/memberpost_list.html', {'memberposts': memberposts, 'member': member})

@login_required
def membercomment_list(request, member_pk):
    member = User.objects.get(pk=member_pk)
    membercomment_listed = sorted(
        chain(FreeComment.objects.filter(author=member),
        ReportComment.objects.filter(author=member),
        ProposalComment.objects.filter(author=member),
        NoticeComment.objects.filter(author=member)),
        key=lambda comment: comment.published_date, reverse=True)
    paginator = Paginator(membercomment_listed, 20)
    page = request.GET.get('page')
    membercomments = paginator.get_page(page)
    return render(request, 'board/membercomment_list.html', {'membercomments': membercomments, 'member': member})

@login_required
def member_info(request, member_pk):
    member = User.objects.get(pk=member_pk)
    return render(request, 'board/member_info.html', {'member': member})

@login_required
def change_nickname(request, member_pk):
    member = User.objects.get(pk=member_pk)
    nickname = Nickname.objects.get(user=member)
    original_nickname = str(nickname.nickname)

    if request.method == "POST":
        form = NicknameForm(request.POST, instance=nickname)

        if form.is_valid():
            nickname = form.save(commit=False)
            nickname.save()
            memberpost_listed = sorted(
                chain(
                    FreePost.objects.filter(author_nickname__icontains=original_nickname),
                    ReportPost.objects.filter(author_nickname__icontains=original_nickname),
                    ProposalPost.objects.filter(author_nickname__icontains=original_nickname),
                    NoticePost.objects.filter(author_nickname__icontains=original_nickname)
                ),
                key=lambda post: post.published_date, reverse=True
                )
            for post in memberpost_listed:
                post.author_nickname = str(nickname.nickname)
                post.save()
            
            messages.success(request, "닉네임이 변경되었습니다.")

            return redirect('member_info', member_pk=member_pk)

    else:
        if member == User.objects.get(pk = request.user.pk): 
            form = NicknameForm(instance=nickname)
            return render(request, 'board/change_nickname.html', {'form': form, 'member_pk': member.pk})
        else:
            return HttpResponse("다른 유저의 닉네임은 수정할 수 없습니다.")
    
    return render(request, 'board/change_nickname.html', {'form': form, 'member_pk': member.pk})

@login_required
def change_password(request, member_pk):
    member = User.objects.get(pk=member_pk)

    if request.method == "POST":
        form = ChangePasswordForm(member, request.POST)

        if form.is_valid():
            member_changed = form.save()
            update_session_auth_hash(request, member_changed)
            messages.success(request, "비밀번호가 변경되었습니다.")
            return redirect('member_info', member_pk=member_pk)
        else:
            messages.error(request, "아래의 오류를 수정해주시기 바랍니다.")

    else:
        if member == User.objects.get(pk = request.user.pk): 
            form = ChangePasswordForm(member, request.POST)
            return render(request, 'board/change_password.html', {'form': form, 'member_pk': member.pk})
        else:
            return HttpResponse("다른 유저의 비밀번호는 수정할 수 없습니다.")
    
    return render(request, 'board/change_password.html', {'form': form, 'member_pk': member.pk})


def home(request):
    bestpost_listing = sorted(
        chain(
            FreePost.objects.all(),
            ReportPost.objects.all(),
            ProposalPost.objects.all(),
            NoticePost.objects.all()),
        key=lambda post: post.published_date, reverse=True)
    bestpost_listed = [post for post in bestpost_listing if post.likes_minus_hates >= 15]
    bestposts = bestpost_listed[0:5]

    freepost_listing = FreePost.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
    freeposts = freepost_listing[0:5]

    reportpost_listing = ReportPost.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
    reportposts = reportpost_listing[0:5]

    proposalpost_listing = ProposalPost.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
    proposalposts = proposalpost_listing[0:5]

    noticepost_listing = NoticePost.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
    noticeposts = noticepost_listing[0:5]

    SE = ReportPost.objects.filter(area__icontains="SE").count()
    IC = ReportPost.objects.filter(area__icontains="IC").count()
    GG = ReportPost.objects.filter(area__icontains="GG").count()
    DJ = ReportPost.objects.filter(area__icontains="DJ").count()
    SJ = ReportPost.objects.filter(area__icontains="SJ").count()
    CB = ReportPost.objects.filter(area__icontains="CB").count()
    CN = ReportPost.objects.filter(area__icontains="CN").count()
    GW = ReportPost.objects.filter(area__icontains="GW").count()
    GJ = ReportPost.objects.filter(area__icontains="GJ").count()
    JB = ReportPost.objects.filter(area__icontains="JB").count()
    JN = ReportPost.objects.filter(area__icontains="JN").count()
    BS = ReportPost.objects.filter(area__icontains="BS").count()
    DG = ReportPost.objects.filter(area__icontains="DG").count()
    US = ReportPost.objects.filter(area__icontains="US").count()
    GB = ReportPost.objects.filter(area__icontains="GB").count()
    GN = ReportPost.objects.filter(area__icontains="GN").count()
    JJ = ReportPost.objects.filter(area__icontains="JJ").count()

    context = {
        'bestposts': bestposts, 'freeposts': freeposts, 'reportposts': reportposts, 
        'proposalposts': proposalposts, 'noticeposts': noticeposts,
        'SE': SE, 'IC': IC, 'GG': GG, 'DJ': DJ, 'SJ': SJ, 'CB': CB, 'CN': CN,
        'GW': GW, 'GJ': GJ, 'JB': JB, 'JN': JN, 'BS': BS, 'DG': DG, 'US': US,
        'GB': GB, 'GN': GN, 'JJ': JJ
        }
    return render(request, 'board/home.html', context)

def freepost_detail(request, pk):
    freepost = get_object_or_404(FreePost, pk=pk)
    hit_count = HitCount.objects.get_for_object(freepost)
    hit_count_response = HitCountMixin.hit_count(request, hit_count)

    freecomment_listing=freepost.freecomments.all()
    paginator = Paginator(freecomment_listing, 20)
    page = request.GET.get('page')
    freecomments = paginator.get_page(page)
    return render(request, 'board/freepost_detail.html', {'freepost': freepost, 'freecomments': freecomments})
    
def reportpost_detail(request, pk):
    reportpost = get_object_or_404(ReportPost, pk=pk)
    hit_count = HitCount.objects.get_for_object(reportpost)
    hit_count_response = HitCountMixin.hit_count(request, hit_count)

    reportcomment_listing=reportpost.reportcomments.all()
    paginator = Paginator(reportcomment_listing, 20)
    page = request.GET.get('page')
    reportcomments = paginator.get_page(page)
    return render(request, 'board/reportpost_detail.html', {'reportpost': reportpost, 'reportcomments': reportcomments})

def proposalpost_detail(request, pk):
    proposalpost = get_object_or_404(ProposalPost, pk=pk)
    hit_count = HitCount.objects.get_for_object(proposalpost)
    hit_count_response = HitCountMixin.hit_count(request, hit_count)

    proposalcomment_listing=proposalpost.proposalcomments.all()
    paginator = Paginator(proposalcomment_listing, 20)
    page = request.GET.get('page')
    proposalcomments = paginator.get_page(page)
    return render(request, 'board/proposalpost_detail.html', {'proposalpost': proposalpost, 'proposalcomments': proposalcomments})

def noticepost_detail(request, pk):
    noticepost = get_object_or_404(NoticePost, pk=pk)
    hit_count = HitCount.objects.get_for_object(noticepost)
    hit_count_response = HitCountMixin.hit_count(request, hit_count)

    noticecomment_listing=noticepost.noticecomments.all()
    paginator = Paginator(noticecomment_listing, 20)
    page = request.GET.get('page')
    noticecomments = paginator.get_page(page)
    return render(request, 'board/noticepost_detail.html', {'noticepost': noticepost, 'noticecomments': noticecomments})

@login_required
def freepost_new(request):

    ImageFormSet = modelformset_factory(FreeImages, form=FreeImagesForm, extra=10)

    if request.method == "POST":
        form = FreePostForm(request.POST, request.FILES)
        formset = ImageFormSet(request.POST, request.FILES, queryset=FreeImages.objects.none())
        
        if form.is_valid() and formset.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.author_nickname = request.user.nickname.nickname
            post.save()

            for imageform in formset.cleaned_data:
                if len(imageform):
                    image = imageform['image']
                    photo = FreeImages(post=post, image=image)
                    photo.save()
                else:
                    pass

            return redirect('freepost_detail', pk=post.pk)
        
        else:
            print(form.errors, formset.errors)

    else:
        form = FreePostForm()
        formset = ImageFormSet(queryset=FreeImages.objects.none())

    return render(request, 'board/freepost_edit.html', {'form': form, 'formset': formset})

@login_required
def reportpost_new(request):

    ImageFormSet = modelformset_factory(ReportImages, form=ReportImagesForm, extra=10, min_num=1)

    if request.method == "POST":
        form = ReportPostForm(request.POST, request.FILES)
        formset = ImageFormSet(request.POST, request.FILES, queryset=ReportImages.objects.none())

        if form.is_valid() and formset.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.author_nickname = request.user.nickname.nickname
            post.save()

            for imageform in formset.cleaned_data:
                if len(imageform):
                    image = imageform['image']
                    photo = ReportImages(post=post, image=image)
                    photo.save()
                
            return redirect('reportpost_detail', pk=post.pk)

        else:
            print(form.errors, formset.errors)

    else:
        form = ReportPostForm()
        formset = ImageFormSet(queryset=ReportImages.objects.none())
        
    return render(request, 'board/reportpost_edit.html', {'form': form, 'formset': formset})

@login_required
def proposalpost_new(request):

    ImageFormSet = modelformset_factory(ProposalImages, form=ProposalImagesForm, extra=10)

    if request.method == "POST":
        form = ProposalPostForm(request.POST, request.FILES)
        formset = ImageFormSet(request.POST, request.FILES, queryset=ProposalImages.objects.none())

        if form.is_valid() and formset.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.author_nickname = request.user.nickname.nickname
            post.save()

            for imageform in formset.cleaned_data:
                if len(imageform):
                    image = imageform['image']
                    photo = ProposalImages(post=post, image=image)
                    photo.save()
                
            return redirect('proposalpost_detail', pk=post.pk)

        else:
            print (form.errors, formset.errors)

    else:
        form = ProposalPostForm()
        formset = ImageFormSet(queryset=ProposalImages.objects.none())
        
    return render(request, 'board/proposalpost_edit.html', {'form': form, 'formset': formset})

@login_required
@staff_member_required
def noticepost_new(request):

    ImageFormSet = modelformset_factory(NoticeImages, form=NoticeImagesForm, extra=10)

    if request.method == "POST":
        form = NoticePostForm(request.POST, request.FILES)
        formset = ImageFormSet(request.POST, request.FILES, queryset=NoticeImages.objects.none())

        if form.is_valid() and formset.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.author_nickname = request.user.nickname.nickname
            post.save()

            for imageform in formset.cleaned_data:
                if len(imageform):
                    image = imageform['image']
                    photo = NoticeImages(post=post, image=image)
                    photo.save()
                
            return redirect('noticepost_detail', pk=post.pk)

        else:
            print (form.errors, formset.errors)

    else:
        form = NoticePostForm()
        formset = ImageFormSet(queryset=NoticeImages.objects.none())
        
    return render(request, 'board/noticepost_edit.html', {'form': form, 'formset': formset})

@login_required
def freepost_edit(request, pk):
    post = get_object_or_404(FreePost, pk=pk)
    ImageFormSet = modelformset_factory(FreeImages, form=FreeImagesForm, extra=9)

    if request.method == "POST":
        form = FreePostForm(request.POST, request.FILES, instance=post)
        formset = ImageFormSet(request.POST, request.FILES, queryset=FreeImages.objects.filter(post=post))

        if form.is_valid() and formset.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.last_edit_date = timezone.now()
            post.number_of_edits += 1
            post.author_nickname = request.user.nickname.nickname
            post.save()

            for imageform in formset.cleaned_data:
                if len(imageform):
                    image = imageform['image']
                    photo = FreeImages(post=post, image=image)
                    photo.save()
                else:
                    pass
                
            return redirect('freepost_detail', pk=post.pk)

        else:
            print (form.errors, formset.errors)

    else:
        if post.author == User.objects.get(username = request.user.get_username()): 
            form = FreePostForm(instance=post)
            formset = ImageFormSet(queryset=FreeImages.objects.filter(post=post))
            return render(request, 'board/freepost_edit.html', {'form': form, 'formset': formset})
        else:
            return HttpResponse('작성자가 아닙니다.')

@login_required
def reportpost_edit(request, pk):
    post = get_object_or_404(ReportPost, pk=pk)
    ImageFormSet = modelformset_factory(ReportImages, form=ReportImagesForm, extra=9)

    if request.method == "POST":
        form = ReportPostForm(request.POST, request.FILES, instance=post)
        formset = ImageFormSet(request.POST, request.FILES, queryset=ReportImages.objects.filter(post=post))

        if form.is_valid() and formset.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.last_edit_date = timezone.now()
            post.number_of_edits += 1
            post.author_nickname = request.user.nickname.nickname
            post.save()

            for imageform in formset.cleaned_data:
                if len(imageform):
                    image = imageform['image']
                    photo = ReportImages(post=post, image=image)
                    photo.save()
                
            return redirect('reportpost_detail', pk=post.pk)

        else:
            print (form.errors, formset.errors)

    else:
        if post.author == User.objects.get(username = request.user.get_username()): 
            form = ReportPostForm(instance=post)
            formset = ImageFormSet(queryset=ReportImages.objects.filter(post=post))
            return render(request, 'board/reportpost_edit.html', {'form': form, 'formset': formset})
        else:
            return HttpResponse('작성자가 아닙니다.')

@login_required
def proposalpost_edit(request, pk):
    post = get_object_or_404(ProposalPost, pk=pk)
    ImageFormSet = modelformset_factory(ProposalImages, form=ProposalImagesForm, extra=9)

    if request.method == "POST":
        form = ProposalPostForm(request.POST, request.FILES, instance=post)
        formset = ImageFormSet(request.POST, request.FILES, queryset=ProposalImages.objects.filter(post=post))

        if form.is_valid() and formset.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.last_edit_date = timezone.now()
            post.number_of_edits += 1
            post.author_nickname = request.user.nickname.nickname
            post.save()

            for imageform in formset.cleaned_data:
                if len(imageform):
                    image = imageform['image']
                    photo = ProposalImages(post=post, image=image)
                    photo.save()
                
            return redirect('proposalpost_detail', pk=post.pk)

        else:
            print (form.errors, formset.errors)

    else:
        if post.author == User.objects.get(username = request.user.get_username()): 
            form = ProposalPostForm(instance=post)
            formset = ImageFormSet(queryset=ProposalImages.objects.filter(post=post))
            return render(request, 'board/proposalpost_edit.html', {'form': form, 'formset': formset})
        else:
            return HttpResponse('작성자가 아닙니다.')

@login_required
@staff_member_required
def noticepost_edit(request, pk):
    post = get_object_or_404(NoticePost, pk=pk)
    ImageFormSet = modelformset_factory(NoticeImages, form=NoticeImagesForm, extra=9)

    if request.method == "POST":
        form = NoticePostForm(request.POST, request.FILES, instance=post)
        formset = ImageFormSet(request.POST, request.FILES, queryset=NoticeImages.objects.filter(post=post))

        if form.is_valid() and formset.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.last_edit_date = timezone.now()
            post.number_of_edits += 1
            post.author_nickname = request.user.nickname.nickname
            post.save()

            for imageform in formset.cleaned_data:
                if len(imageform):
                    image = imageform['image']
                    photo = NoticeImages(post=post, image=image)
                    photo.save()
                
            return redirect('noticepost_detail', pk=post.pk)

        else:
            print (form.errors, formset.errors)

    else:
        if post.author == User.objects.get(username = request.user.get_username()): 
            form = NoticePostForm(instance=post)
            formset = ImageFormSet(queryset=NoticeImages.objects.filter(post=post))
            return render(request, 'board/noticepost_edit.html', {'form': form, 'formset': formset})
        else:
            return HttpResponse('작성자가 아닙니다.')
@login_required
def freepost_remove(request, pk):
    post = get_object_or_404(FreePost, pk=pk)
    if post.author == User.objects.get(username = request.user.get_username()):
        post.delete()
        return redirect('freepost_list')
    else:
        return HttpResponse('작성자가 아닙니다.')

@login_required
def reportpost_remove(request, pk):
    post = get_object_or_404(ReportPost, pk=pk)
    if post.author == User.objects.get(username = request.user.get_username()):
        post.delete()
        return redirect('reportpost_list')
    else:
        return HttpResponse('작성자가 아닙니다.')

@login_required
def proposalpost_remove(request, pk):
    post = get_object_or_404(ProposalPost, pk=pk)
    if post.author == User.objects.get(username = request.user.get_username()):
        post.delete()
        return redirect('proposalpost_list')
    else:
        return HttpResponse('작성자가 아닙니다.')

@login_required
@staff_member_required
def noticepost_remove(request, pk):
    post = get_object_or_404(NoticePost, pk=pk)
    if post.author == User.objects.get(username = request.user.get_username()):
        post.delete()
        return redirect('noticepost_list')
    else:
        return HttpResponse('작성자가 아닙니다.')

# 페이지 이동 없이 댓글 달기. 출처 : https://lhy.kr/
@login_required
def add_freecomment_to_freepost(request, pk):
    if request.method == "POST":
        freepost = get_object_or_404(FreePost, pk=pk)
        content = request.POST.get('freecomment_form')
        
        if not content:
            return HttpResponse('댓글 내용을 입력하세요', status=400)
        else:
            FreeComment.objects.create(
                post = freepost,
                author = request.user,
                content = content
            )
            commenter = request.user
            post_author = freepost.author
            if commenter != post_author:
                Notification.objects.create(
                    actor = commenter,
                    recipient = post_author,
                    verb = "님이 회원님의 게시글에 댓글을 달았습니다.",
                    board = "Free",
                    post_id = freepost.pk,
                    is_read = False,
                )
            return redirect('freepost_detail', pk=freepost.pk)
    else:
        return HttpResponseBadRequest('오류가 발생했습니다. 관리자에게 문의하세요.')

@login_required
def add_reportcomment_to_reportpost(request, pk):
    if request.method == "POST":
        reportpost = get_object_or_404(ReportPost, pk=pk)
        content = request.POST.get('reportcomment_form')
        
        if not content:
            return HttpResponse('댓글 내용을 입력하세요', status=400)
        else:
            ReportComment.objects.create(
                post = reportpost,
                author = request.user,
                content = content
            )
            commenter = request.user
            post_author = reportpost.author
            if commenter != post_author:
                Notification.objects.create(
                    actor = commenter,
                    recipient = post_author,
                    verb = "님이 회원님의 게시글에 댓글을 달았습니다.",
                    board = "Report",
                    post_id = reportpost.pk,
                    is_read = False,
                )
            return redirect('reportpost_detail', pk=reportpost.pk)
    else:
        return HttpResponseBadRequest('오류가 발생했습니다. 관리자에게 문의하세요.')

@login_required
def add_proposalcomment_to_proposalpost(request, pk):
    if request.method == "POST":
        proposalpost = get_object_or_404(ProposalPost, pk=pk)
        content = request.POST.get('proposalcomment_form')
        
        if not content:
            return HttpResponse('댓글 내용을 입력하세요', status=400)
        else:
            ProposalComment.objects.create(
                post = proposalpost,
                author = request.user,
                content = content
            )
            commenter = request.user
            post_author = proposalpost.author
            if commenter != post_author:
                Notification.objects.create(
                    actor = commenter,
                    recipient = post_author,
                    verb = "님이 회원님의 게시글에 댓글을 달았습니다.",
                    board = "Proposal",
                    post_id = proposalpost.pk,
                    is_read = False,
                )
            return redirect('proposalpost_detail', pk=proposalpost.pk)
    else:
        return HttpResponseBadRequest('오류가 발생했습니다. 관리자에게 문의하세요.')

@login_required
def add_noticecomment_to_noticepost(request, pk):
    if request.method == "POST":
        noticepost = get_object_or_404(NoticePost, pk=pk)
        content = request.POST.get('noticecomment_form')
        
        if not content:
            return HttpResponse('댓글 내용을 입력하세요', status=400)
        else:
            NoticeComment.objects.create(
                post = noticepost,
                author = request.user,
                content = content
            )
            commenter = request.user
            post_author = noticepost.author
            if commenter != post_author:
                Notification.objects.create(
                    actor = commenter,
                    recipient = post_author,
                    verb = "님이 회원님의 게시글에 댓글을 달았습니다.",
                    board = "Notice",
                    post_id = noticepost.pk,
                    is_read = False,
                )
            return redirect('noticepost_detail', pk=noticepost.pk)
    else:
        return HttpResponseBadRequest('오류가 발생했습니다. 관리자에게 문의하세요.')

def signup(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        nickname_form = NicknameForm(request.POST)
        new_user_nickname = request.POST.get('nickname')

        if form.is_valid() and nickname_form.is_valid():
            new_user = form.save()
            Nickname.objects.create(
                user = new_user,
                nickname = new_user_nickname
            )
            login(request, new_user)
            return redirect('home')
    else:
        form = SignupForm()
        nickname_form = NicknameForm
    
    return render(request, 'board/signup.html', {'form': form, 'nickname_form': nickname_form})

# 추천/비추천 기능. 출처: 초보몽키의 개발공부로그
@login_required
@require_POST
def freepost_like(request):
    if request.method == 'POST':
        user = request.user
        freepost_id = request.POST.get('pk', None)
        freepost = FreePost.objects.get(pk = freepost_id)
        
        if user == freepost.author:
            message = '자신의 글은 추천 하실 수 없습니다'
        else:
            if freepost.likes.filter(id = user.id).exists():
                freepost.likes.remove(user)
                message = '추천을 취소하셨습니다'
                liker = request.user
                post_author = freepost.author
                Notification.objects.create(
                    actor = user,
                    recipient = freepost.author,
                    verb = "님이 회원님의 게시글 추천을 취소했습니다.",
                    board = "Free",
                    post_id = freepost.pk,
                    is_read = False,
                )
            elif freepost.hates.filter(id = user.id).exists():
                message = '비추천을 취소한 후 추천을 누르실 수 있습니다'
            else:
                freepost.likes.add(user)
                message = '추천을 누르셨습니다'
                liker = request.user
                post_author = freepost.author
                Notification.objects.create(
                    actor = user,
                    recipient = freepost.author,
                    verb = "님이 회원님의 게시글을 추천했습니다.",
                    board = "Free",
                    post_id = freepost.pk,
                    is_read = False,
                )
    
    context = {'likes_count' : freepost.total_likes, 'message' : message}
    return HttpResponse(json.dumps(context), content_type='application/json')

@login_required
@require_POST
def freepost_hate(request):
    if request.method == 'POST':
        user = request.user
        freepost_id = request.POST.get('pk', None)
        freepost = FreePost.objects.get(pk = freepost_id)

        if user == freepost.author:
            message = '자신의 글은 비추천 하실 수 없습니다'
        else:
            if freepost.hates.filter(id = user.id).exists():
                freepost.hates.remove(user)
                message = '비추천을 취소하셨습니다'
                hater = request.user
                post_author = freepost.author
                Notification.objects.create(
                    actor = user,
                    recipient = freepost.author,
                    verb = "님이 회원님의 게시글 비추천을 취소했습니다.",
                    board = "Free",
                    post_id = freepost.pk,
                    is_read = False,
                )
            elif freepost.likes.filter(id = user.id).exists():
                message = '추천을 취소한 후 추천을 누르실 수 있습니다'
            else:
                freepost.hates.add(user)
                message = '비추천을 누르셨습니다'
                hater = request.user
                post_author = freepost.author
                Notification.objects.create(
                    actor = user,
                    recipient = freepost.author,
                    verb = "님이 회원님의 게시글을 비추천했습니다.",
                    board = "Free",
                    post_id = freepost.pk,
                    is_read = False,
                )
    
    context = {'hates_count' : freepost.total_hates, 'message' : message}
    return HttpResponse(json.dumps(context), content_type='application/json')

@login_required
@require_POST
def reportpost_like(request):
    if request.method == 'POST':
        user = request.user
        reportpost_id = request.POST.get('pk', None)
        reportpost = ReportPost.objects.get(pk = reportpost_id)

        if user == reportpost.author:
            message = '자신의 글은 추천 하실 수 없습니다'
        else:
            if reportpost.likes.filter(id = user.id).exists():
                reportpost.likes.remove(user)
                message = '추천을 취소하셨습니다'
                liker = request.user
                post_author = reportpost.author
                Notification.objects.create(
                    actor = user,
                    recipient = reportpost.author,
                    verb = "님이 회원님의 게시글 추천을 취소했습니다.",
                    board = "Report",
                    post_id = reportpost.pk,
                    is_read = False,
                )
            elif reportpost.hates.filter(id = user.id).exists():
                message = '비추천을 취소한 후 추천을 누르실 수 있습니다'
            else:
                reportpost.likes.add(user)
                message = '추천을 누르셨습니다'
                liker = request.user
                post_author = reportpost.author
                Notification.objects.create(
                    actor = user,
                    recipient = reportpost.author,
                    verb = "님이 회원님의 게시글을 추천했습니다.",
                    board = "Report",
                    post_id = reportpost.pk,
                    is_read = False,
                )
    
    context = {'likes_count' : reportpost.total_likes, 'message' : message}
    return HttpResponse(json.dumps(context), content_type='application/json')

@login_required
@require_POST
def reportpost_hate(request):
    if request.method == 'POST':
        user = request.user
        reportpost_id = request.POST.get('pk', None)
        reportpost = ReportPost.objects.get(pk = reportpost_id)

        if user == reportpost.author:
            message = '자신의 글은 비추천 하실 수 없습니다'
        else:
            if reportpost.hates.filter(id = user.id).exists():
                reportpost.hates.remove(user)
                message = '비추천을 취소하셨습니다'
                hater = request.user
                post_author = reportpost.author
                Notification.objects.create(
                    actor = user,
                    recipient = reportpost.author,
                    verb = "님이 회원님의 게시글 비추천을 취소했습니다.",
                    board = "Report",
                    post_id = reportpost.pk,
                    is_read = False,
                )
            elif reportpost.likes.filter(id = user.id).exists():
                message = '추천을 취소한 후 추천을 누르실 수 있습니다'
            else:
                reportpost.hates.add(user)
                message = '비추천을 누르셨습니다'
                hater = request.user
                post_author = reportpost.author
                Notification.objects.create(
                    actor = user,
                    recipient = reportpost.author,
                    verb = "님이 회원님의 게시글을 비추천했습니다.",
                    board = "Report",
                    post_id = reportpost.pk,
                    is_read = False,
                )
    
    context = {'hates_count' : reportpost.total_hates, 'message' : message}
    return HttpResponse(json.dumps(context), content_type='application/json')

@login_required
@require_POST
def proposalpost_like(request):
    if request.method == 'POST':
        user = request.user
        proposalpost_id = request.POST.get('pk', None)
        proposalpost = ProposalPost.objects.get(pk = proposalpost_id)

        if user == proposalpost.author:
            message = '자신의 글은 추천 하실 수 없습니다'
        else:
            if proposalpost.likes.filter(id = user.id).exists():
                proposalpost.likes.remove(user)
                message = '추천을 취소하셨습니다'
                liker = request.user
                post_author = proposalpost.author
                Notification.objects.create(
                    actor = user,
                    recipient = proposalpost.author,
                    verb = "님이 회원님의 게시글 추천을 취소했습니다.",
                    board = "Proposal",
                    post_id = proposalpost.pk,
                    is_read = False,
                )
            elif proposalpost.hates.filter(id = user.id).exists():
                message = '비추천을 취소한 후 추천을 누르실 수 있습니다'
            else:
                proposalpost.likes.add(user)
                message = '추천을 누르셨습니다'
                liker = request.user
                post_author = proposalpost.author
                Notification.objects.create(
                    actor = user,
                    recipient = proposalpost.author,
                    verb = "님이 회원님의 게시글을 추천했습니다.",
                    board = "Proposal",
                    post_id = proposalpost.pk,
                    is_read = False,
                )
    
    context = {'likes_count' : proposalpost.total_likes, 'message' : message}
    return HttpResponse(json.dumps(context), content_type='application/json')

@login_required
@require_POST
def proposalpost_hate(request):
    if request.method == 'POST':
        user = request.user
        proposalpost_id = request.POST.get('pk', None)
        proposalpost = ProposalPost.objects.get(pk = proposalpost_id)

        if user == proposalpost.author:
            message = '자신의 글은 비추천 하실 수 없습니다'
        else:
            if proposalpost.hates.filter(id = user.id).exists():
                proposalpost.hates.remove(user)
                message = '비추천을 취소하셨습니다'
                hater = request.user
                post_author = proposalpost.author
                Notification.objects.create(
                    actor = user,
                    recipient = proposalpost.author,
                    verb = "님이 회원님의 게시글 비추천을 취소했습니다.",
                    board = "Proposal",
                    post_id = proposalpost.pk,
                    is_read = False,
                )
            elif proposalpost.likes.filter(id = user.id).exists():
                message = '추천을 취소한 후 추천을 누르실 수 있습니다'
            else:
                proposalpost.hates.add(user)
                message = '비추천을 누르셨습니다'
                hater = request.user
                post_author = proposalpost.author
                Notification.objects.create(
                    actor = user,
                    recipient = proposalpost.author,
                    verb = "님이 회원님의 게시글을 비추천했습니다.",
                    board = "Proposal",
                    post_id = proposalpost.pk,
                    is_read = False,
                )
    
    context = {'hates_count' : proposalpost.total_hates, 'message' : message}
    return HttpResponse(json.dumps(context), content_type='application/json')

@login_required
@require_POST
def noticepost_like(request):
    if request.method == 'POST':
        user = request.user
        noticepost_id = request.POST.get('pk', None)
        noticepost = NoticePost.objects.get(pk = noticepost_id)

        if user == noticepost.author:
            message = '자신의 글은 추천 하실 수 없습니다'
        else:
            if noticepost.likes.filter(id = user.id).exists():
                noticepost.likes.remove(user)
                message = '추천을 취소하셨습니다'
                liker = request.user
                post_author = noticepost.author
                Notification.objects.create(
                    actor = user,
                    recipient = noticepost.author,
                    verb = "님이 회원님의 게시글 추천을 취소했습니다.",
                    board = "Notice",
                    post_id = noticepost.pk,
                    is_read = False,
                )
            elif noticepost.hates.filter(id = user.id).exists():
                message = '비추천을 취소한 후 추천을 누르실 수 있습니다'
            else:
                noticepost.likes.add(user)
                message = '추천을 누르셨습니다'
                liker = request.user
                post_author = noticepost.author
                Notification.objects.create(
                    actor = user,
                    recipient = noticepost.author,
                    verb = "님이 회원님의 게시글을 추천했습니다.",
                    board = "Notice",
                    post_id = noticepost.pk,
                    is_read = False,
                )
    
    context = {'likes_count' : noticepost.total_likes, 'message' : message}
    return HttpResponse(json.dumps(context), content_type='application/json')

@login_required
@require_POST
def noticepost_hate(request):
    if request.method == 'POST':
        user = request.user
        noticepost_id = request.POST.get('pk', None)
        noticepost = NoticePost.objects.get(pk = noticepost_id)

        if user == noticepost.author:
            message = '자신의 글은 비추천 하실 수 없습니다'
        else:
            if noticepost.hates.filter(id = user.id).exists():
                noticepost.hates.remove(user)
                message = '비추천을 취소하셨습니다'
                hater = request.user
                post_author = noticepost.author
                Notification.objects.create(
                    actor = user,
                    recipient = noticepost.author,
                    verb = "님이 회원님의 게시글 비추천을 취소했습니다.",
                    board = "Notice",
                    post_id = noticepost.pk,
                    is_read = False,
                )
            elif noticepost.likes.filter(id = user.id).exists():
                message = '추천을 취소한 후 추천을 누르실 수 있습니다'
            else:
                noticepost.hates.add(user)
                message = '비추천을 누르셨습니다'
                hater = request.user
                post_author = noticepost.author
                Notification.objects.create(
                    actor = user,
                    recipient = noticepost.author,
                    verb = "님이 회원님의 게시글을 비추천했습니다.",
                    board = "Notice",
                    post_id = noticepost.pk,
                    is_read = False,
                )
    
    context = {'hates_count' : noticepost.total_hates, 'message' : message}
    return HttpResponse(json.dumps(context), content_type='application/json')

@login_required
@require_POST
def freecomment_like(request):
    if request.method == 'POST':
        user = request.user
        freecomment_id = request.POST.get('pk', None)
        freecomment = FreeComment.objects.get(pk = freecomment_id)

        if user == freecomment.author:
            message = '자신의 댓글은 추천 하실 수 없습니다'
        else:
            if freecomment.likes.filter(id = user.id).exists():
                freecomment.likes.remove(user)
                message = '추천을 취소하셨습니다'
                liker = request.user
                comment_author = freecomment.author
                Notification.objects.create(
                    actor = user,
                    recipient = comment_author,
                    verb = "님이 회원님의 댓글 추천을 취소했습니다.",
                    board = "Free",
                    post_id = freecomment.post.pk,
                    is_read = False,
                )
            elif freecomment.hates.filter(id = user.id).exists():
                message = '비추천을 취소한 후 추천을 누르실 수 있습니다'
            else:
                freecomment.likes.add(user)
                message = '추천을 누르셨습니다'
                liker = request.user
                comment_author = freecomment.author
                Notification.objects.create(
                    actor = user,
                    recipient = comment_author,
                    verb = "님이 회원님의 댓글을 추천했습니다.",
                    board = "Free",
                    post_id = freecomment.post.pk,
                    is_read = False,
                )
    
    context = {'likes_count' : freecomment.total_likes, 'message' : message}
    return HttpResponse(json.dumps(context), content_type='application/json')

@login_required
@require_POST
def freecomment_hate(request):
    if request.method == 'POST':
        user = request.user
        freecomment_id = request.POST.get('pk', None)
        freecomment = FreeComment.objects.get(pk = freecomment_id)

        if user == freecomment.author:
            message = '자신의 댓글은 비추천 하실 수 없습니다'
        else:
            if freecomment.hates.filter(id = user.id).exists():
                freecomment.hates.remove(user)
                message = '비추천을 취소하셨습니다'
                hater = request.user
                comment_author = freecomment.author
                Notification.objects.create(
                    actor = user,
                    recipient = comment_author,
                    verb = "님이 회원님의 댓글 비추천을 취소했습니다.",
                    board = "Free",
                    post_id = freecomment.post.pk,
                    is_read = False,
                )
            elif freecomment.likes.filter(id = user.id).exists():
                message = '추천을 취소한 후 추천을 누르실 수 있습니다'
            else:
                freecomment.hates.add(user)
                message = '비추천을 누르셨습니다'
                hater = request.user
                comment_author = freecomment.author
                Notification.objects.create(
                    actor = user,
                    recipient = comment_author,
                    verb = "님이 회원님의 댓글을 비추천했습니다.",
                    board = "Free",
                    post_id = freecomment.post.pk,
                    is_read = False,
                )
    
    context = {'hates_count' : freecomment.total_hates, 'message' : message}
    return HttpResponse(json.dumps(context), content_type='application/json')

@login_required
@require_POST
def reportcomment_like(request):
    if request.method == 'POST':
        user = request.user
        reportcomment_id = request.POST.get('pk', None)
        reportcomment = ReportComment.objects.get(pk = reportcomment_id)

        if user == reportcomment.author:
            message = '자신의 댓글은 추천 하실 수 없습니다'
        else:
            if reportcomment.likes.filter(id = user.id).exists():
                reportcomment.likes.remove(user)
                message = '추천을 취소하셨습니다'
                liker = request.user
                comment_author = reportcomment.author
                Notification.objects.create(
                    actor = user,
                    recipient = comment_author,
                    verb = "님이 회원님의 댓글 추천을 취소했습니다.",
                    board = "Report",
                    post_id = reportcomment.post.pk,
                    is_read = False,
                )
            elif reportcomment.hates.filter(id = user.id).exists():
                message = '비추천을 취소한 후 추천을 누르실 수 있습니다'
            else:
                reportcomment.likes.add(user)
                message = '추천을 누르셨습니다'
                liker = request.user
                comment_author = reportcomment.author
                Notification.objects.create(
                    actor = user,
                    recipient = comment_author,
                    verb = "님이 회원님의 댓글을 추천했습니다.",
                    board = "Report",
                    post_id = reportcomment.post.pk,
                    is_read = False,
                )
    
    context = {'likes_count' : reportcomment.total_likes, 'message' : message}
    return HttpResponse(json.dumps(context), content_type='application/json')

@login_required
@require_POST
def reportcomment_hate(request):
    if request.method == 'POST':
        user = request.user
        reportcomment_id = request.POST.get('pk', None)
        reportcomment = ReportComment.objects.get(pk = reportcomment_id)

        if user == reportcomment.author:
            message = '자신의 댓글은 비추천 하실 수 없습니다'
        else:
            if reportcomment.hates.filter(id = user.id).exists():
                reportcomment.hates.remove(user)
                message = '비추천을 취소하셨습니다'
                hater = request.user
                comment_author = reportcomment.author
                Notification.objects.create(
                    actor = user,
                    recipient = comment_author,
                    verb = "님이 회원님의 댓글 비추천을 취소했습니다.",
                    board = "Report",
                    post_id = reportcomment.post.pk,
                    is_read = False,
                )
            elif reportcomment.likes.filter(id = user.id).exists():
                message = '추천을 취소한 후 추천을 누르실 수 있습니다'
            else:
                reportcomment.hates.add(user)
                message = '비추천을 누르셨습니다'
                hater = request.user
                comment_author = reportcomment.author
                Notification.objects.create(
                    actor = user,
                    recipient = comment_author,
                    verb = "님이 회원님의 댓글을 비추천했습니다.",
                    board = "Report",
                    post_id = reportcomment.post.pk,
                    is_read = False,
                )
    
    context = {'hates_count' : reportcomment.total_hates, 'message' : message}
    return HttpResponse(json.dumps(context), content_type='application/json')

@login_required
@require_POST
def proposalcomment_like(request):
    if request.method == 'POST':
        user = request.user
        proposalcomment_id = request.POST.get('pk', None)
        proposalcomment = ProposalComment.objects.get(pk = proposalcomment_id)

        if user == proposalcomment.author:
            message = '자신의 댓글은 추천 하실 수 없습니다'
        else:
            if proposalcomment.likes.filter(id = user.id).exists():
                proposalcomment.likes.remove(user)
                message = '추천을 취소하셨습니다'
                liker = request.user
                comment_author = proposalcomment.author
                Notification.objects.create(
                    actor = user,
                    recipient = comment_author,
                    verb = "님이 회원님의 댓글 추천을 취소했습니다.",
                    board = "Proposal",
                    post_id = proposalcomment.post.pk,
                    is_read = False,
                )
            elif proposalcomment.hates.filter(id = user.id).exists():
                message = '비추천을 취소한 후 추천을 누르실 수 있습니다'
            else:
                proposalcomment.likes.add(user)
                message = '추천을 누르셨습니다'
                liker = request.user
                comment_author = proposalcomment.author
                Notification.objects.create(
                    actor = user,
                    recipient = comment_author,
                    verb = "님이 회원님의 댓글을 추천했습니다.",
                    board = "Proposal",
                    post_id = proposalcomment.post.pk,
                    is_read = False,
                )
    
    context = {'likes_count' : proposalcomment.total_likes, 'message' : message}
    return HttpResponse(json.dumps(context), content_type='application/json')

@login_required
@require_POST
def proposalcomment_hate(request):
    if request.method == 'POST':
        user = request.user
        proposalcomment_id = request.POST.get('pk', None)
        proposalcomment = ProposalComment.objects.get(pk = proposalcomment_id)

        if user == proposalcomment.author:
            message = '자신의 댓글은 비추천 하실 수 없습니다'
        else:
            if proposalcomment.hates.filter(id = user.id).exists():
                proposalcomment.hates.remove(user)
                message = '비추천을 취소하셨습니다'
                hater = request.user
                comment_author = proposalcomment.author
                Notification.objects.create(
                    actor = user,
                    recipient = comment_author,
                    verb = "님이 회원님의 댓글 비추천을 취소했습니다.",
                    board = "Proposal",
                    post_id = proposalcomment.post.pk,
                    is_read = False,
                )
            elif proposalcomment.likes.filter(id = user.id).exists():
                message = '추천을 취소한 후 추천을 누르실 수 있습니다'
            else:
                proposalcomment.hates.add(user)
                message = '비추천을 누르셨습니다'
                hater = request.user
                comment_author = proposalcomment.author
                Notification.objects.create(
                    actor = user,
                    recipient = comment_author,
                    verb = "님이 회원님의 댓글을 비추천했습니다.",
                    board = "Proposal",
                    post_id = proposalcomment.post.pk,
                    is_read = False,
                )
    
    context = {'hates_count' : proposalcomment.total_hates, 'message' : message}
    return HttpResponse(json.dumps(context), content_type='application/json')

@login_required
@require_POST
def noticecomment_like(request):
    if request.method == 'POST':
        user = request.user
        noticecomment_id = request.POST.get('pk', None)
        noticecomment = NoticeComment.objects.get(pk = noticecomment_id)

        if user == noticecomment.author:
            message = '자신의 댓글은 추천 하실 수 없습니다'
        else:
            if noticecomment.likes.filter(id = user.id).exists():
                noticecomment.likes.remove(user)
                message = '추천을 취소하셨습니다'
                liker = request.user
                comment_author = noticecomment.author
                Notification.objects.create(
                    actor = user,
                    recipient = comment_author,
                    verb = "님이 회원님의 댓글 추천을 취소했습니다.",
                    board = "Notice",
                    post_id = noticecomment.post.pk,
                    is_read = False,
                )
            elif noticecomment.hates.filter(id = user.id).exists():
                message = '비추천을 취소한 후 추천을 누르실 수 있습니다'
            else:
                noticecomment.likes.add(user)
                message = '추천을 누르셨습니다'
                liker = request.user
                comment_author = noticecomment.author
                Notification.objects.create(
                    actor = user,
                    recipient = comment_author,
                    verb = "님이 회원님의 댓글을 추천했습니다.",
                    board = "Notice",
                    post_id = noticecomment.post.pk,
                    is_read = False,
                )
    
    context = {'likes_count' : noticecomment.total_likes, 'message' : message}
    return HttpResponse(json.dumps(context), content_type='application/json')

@login_required
@require_POST
def noticecomment_hate(request):
    if request.method == 'POST':
        user = request.user
        noticecomment_id = request.POST.get('pk', None)
        noticecomment = NoticeComment.objects.get(pk = noticecomment_id)

        if user == noticecomment.author:
            message = '자신의 댓글은 비추천 하실 수 없습니다'
        else:
            if noticecomment.hates.filter(id = user.id).exists():
                noticecomment.hates.remove(user)
                message = '비추천을 취소하셨습니다'
                hater = request.user
                comment_author = noticecomment.author
                Notification.objects.create(
                    actor = user,
                    recipient = comment_author,
                    verb = "님이 회원님의 댓글 비추천을 취소했습니다.",
                    board = "Notice",
                    post_id = noticecomment.post.pk,
                    is_read = False,
                )
            elif noticecomment.likes.filter(id = user.id).exists():
                message = '추천을 취소한 후 추천을 누르실 수 있습니다'
            else:
                noticecomment.hates.add(user)
                message = '비추천을 누르셨습니다'
                hater = request.user
                comment_author = noticecomment.author
                Notification.objects.create(
                    actor = user,
                    recipient = comment_author,
                    verb = "님이 회원님의 댓글을 비추천했습니다.",
                    board = "Notice",
                    post_id = noticecomment.post.pk,
                    is_read = False,
                )
    
    context = {'hates_count' : noticecomment.total_hates, 'message' : message}
    return HttpResponse(json.dumps(context), content_type='application/json')

@login_required
def freecomment_edit(request, pk):
    comment = get_object_or_404(FreeComment, pk=pk)
    if request.method == "POST":
        form = FreeCommentForm(request.POST, instance=comment)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.last_edit_date = timezone.now()
            comment.number_of_edits += 1
            comment.save()
            return redirect('freepost_detail', pk=comment.post.pk)
    else:
        if comment.author == User.objects.get(username = request.user.get_username()): 
            form = FreeCommentForm(instance=comment)
            return render(request, 'board/freecomment_edit.html', {'form': form})
        else:
            return HttpResponse('작성자가 아닙니다.')

@login_required
def reportcomment_edit(request, pk):
    comment = get_object_or_404(ReportComment, pk=pk)
    if request.method == "POST":
        form = ReportCommentForm(request.POST, instance=comment)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.last_edit_date = timezone.now()
            comment.number_of_edits += 1
            comment.save()
            return redirect('reportpost_detail', pk=comment.post.pk)
    else:
        if comment.author == User.objects.get(username = request.user.get_username()): 
            form = ReportCommentForm(instance=comment)
            return render(request, 'board/reportcomment_edit.html', {'form': form})
        else:
            return HttpResponse('작성자가 아닙니다.')

@login_required
def proposalcomment_edit(request, pk):
    comment = get_object_or_404(ProposalComment, pk=pk)
    if request.method == "POST":
        form = ProposalCommentForm(request.POST, instance=comment)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.last_edit_date = timezone.now()
            comment.number_of_edits += 1
            comment.save()
            return redirect('proposalpost_detail', pk=comment.post.pk)
    else:
        if comment.author == User.objects.get(username = request.user.get_username()): 
            form = ProposalCommentForm(instance=comment)
            return render(request, 'board/proposalcomment_edit.html', {'form': form})
        else:
            return HttpResponse('작성자가 아닙니다.')

@login_required
def noticecomment_edit(request, pk):
    comment = get_object_or_404(NoticeComment, pk=pk)
    if request.method == "POST":
        form = NoticeCommentForm(request.POST, instance=comment)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.last_edit_date = timezone.now()
            comment.number_of_edits += 1
            comment.save()
            return redirect('noticepost_detail', pk=comment.post.pk)
    else:
        if comment.author == User.objects.get(username = request.user.get_username()): 
            form = NoticeCommentForm(instance=comment)
            return render(request, 'board/noticecomment_edit.html', {'form': form})
        else:
            return HttpResponse('작성자가 아닙니다.')

@login_required
def freecomment_remove(request, pk):
    comment = get_object_or_404(FreeComment, pk=pk)
    if comment.author == User.objects.get(username = request.user.get_username()):
        comment.delete()
        return redirect('freepost_detail', pk=comment.post.pk)
    else:
        return HttpResponse('작성자가 아닙니다.')

@login_required
def reportcomment_remove(request, pk):
    comment = get_object_or_404(ReportComment, pk=pk)
    if comment.author == User.objects.get(username = request.user.get_username()):
        comment.delete()
        return redirect('reportpost_detail', pk=comment.post.pk)
    else:
        return HttpResponse('작성자가 아닙니다.')

@login_required
def proposalcomment_remove(request, pk):
    comment = get_object_or_404(ProposalComment, pk=pk)
    if comment.author == User.objects.get(username = request.user.get_username()):
        comment.delete()
        return redirect('proposalpost_detail', pk=comment.post.pk)
    else:
        return HttpResponse('작성자가 아닙니다.')

@login_required
def noticecomment_remove(request, pk):
    comment = get_object_or_404(NoticeComment, pk=pk)
    if comment.author == User.objects.get(username = request.user.get_username()):
        comment.delete()
        return redirect('noticepost_detail', pk=comment.post.pk)
    else:
        return HttpResponse('작성자가 아닙니다.')

def top_search_view(request):
    filter_content = request.GET.get('q', '')
    area_for_search = {
        '서울': 'SE', 
        '인천': 'IC', 
        '경기': 'GG', 
        '대전': 'DJ', 
        '세종': 'SJ', 
        '충북': 'CB', 
        '충남': 'CN', 
        '강원': 'GW', 
        '광주': 'GJ', 
        '전북': 'JB', 
        '전남': 'JN', 
        '부산': 'BS', 
        '대구': 'DG', 
        '울산': 'US', 
        '경북': 'GB', 
        '경남': 'GN', 
        '제주': 'JJ'
    }
    
    for q in area_for_search.keys():
        if q == filter_content:
            searchpost_listed = sorted(
                chain(
                    FreePost.objects.filter(title__icontains=filter_content),
                    ReportPost.objects.filter(title__icontains=filter_content),
                    ProposalPost.objects.filter(title__icontains=filter_content),
                    NoticePost.objects.filter(title__icontains=filter_content),
                    FreePost.objects.filter(content__icontains=filter_content),
                    ReportPost.objects.filter(content__icontains=filter_content),
                    ProposalPost.objects.filter(content__icontains=filter_content),
                    NoticePost.objects.filter(content__icontains=filter_content),
                    FreePost.objects.filter(author_nickname__icontains=filter_content),
                    ReportPost.objects.filter(author_nickname__icontains=filter_content),
                    ProposalPost.objects.filter(author_nickname__icontains=filter_content),
                    NoticePost.objects.filter(author_nickname__icontains=filter_content),
                    ReportPost.objects.filter(area__icontains=area_for_search[filter_content]),
                    ReportPost.objects.filter(specific_area__icontains=filter_content),
                ),
                key=lambda post: post.published_date, reverse=True
            )
    else:
        searchpost_listed = sorted(
            chain(
                FreePost.objects.filter(title__icontains=filter_content),
                ReportPost.objects.filter(title__icontains=filter_content),
                ProposalPost.objects.filter(title__icontains=filter_content),
                NoticePost.objects.filter(title__icontains=filter_content),
                FreePost.objects.filter(content__icontains=filter_content),
                ReportPost.objects.filter(content__icontains=filter_content),
                ProposalPost.objects.filter(content__icontains=filter_content),
                NoticePost.objects.filter(content__icontains=filter_content),
                FreePost.objects.filter(author_nickname__icontains=filter_content),
                ReportPost.objects.filter(author_nickname__icontains=filter_content),
                ProposalPost.objects.filter(author_nickname__icontains=filter_content),
                NoticePost.objects.filter(author_nickname__icontains=filter_content),
                ReportPost.objects.filter(specific_area__icontains=filter_content),
            ),
            key=lambda post: post.published_date, reverse=True
        )

    searchpost_listed = sorted(list(set(searchpost_listed)), key=lambda post: post.published_date, reverse=True)
    paginator = Paginator(searchpost_listed, 10)
    page = request.GET.get('page')
    searchposts = paginator.get_page(page)
    return render(request, 'board/searchpost_list.html', {'searchposts': searchposts, 'q': filter_content})

@login_required
@require_POST
def notification_read(request):
    if request.method == 'POST':
        notification_id = request.POST.get('pk', None)
        notification = get_object_or_404(Notification, pk=notification_id)
        notification.is_read = True
        notification.save()
        context = {}
        return HttpResponse(json.dumps(context), content_type='application/json')

@login_required
def notification_read_all(request):
    if request.method == 'POST':
        notification_recipient= request.user
        notifications = Notification.objects.filter(
            recipient = notification_recipient
            ).filter(
                is_read = False,
            )
        for notification in notifications:
            notification.is_read = True
            notification.save()
        context = {}
        return HttpResponse(json.dumps(context), content_type='application/json')

