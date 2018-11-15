from django.shortcuts import render, get_object_or_404, redirect
from .models import (
    FreePost, ReportPost, ProposalPost, NoticePost, FreeComment, ReportComment, ProposalComment, NoticeComment
    )
from django.utils import timezone
from .forms import (
    FreePostForm, ReportPostForm, ProposalPostForm, NoticePostForm, FreeCommentForm, ReportCommentForm, ProposalCommentForm, NoticeCommentForm, UserForm, UserChangeForm
)
from django.contrib.auth.models import User
from django.contrib.auth import login

from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponse, HttpResponseBadRequest
from django.views.decorators.http import require_POST
try:
    from django.utils import simplejson as json
except ImportError:
    import json
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from hitcount.models import HitCount
from hitcount.views import HitCountMixin
from itertools import chain


def freepost_list(request):
    freepost_listing = FreePost.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
    notice_tops = NoticePost.objects.filter(notice_type=1, published_date__lte=timezone.now()).order_by('-published_date')
    paginator = Paginator(freepost_listing, 10)
    page = request.GET.get('page')
    freeposts = paginator.get_page(page)
    return render(request,'board/freepost_list.html', {'freeposts': freeposts, 'notice_tops': notice_tops})

def reportpost_list(request):
    reportpost_listing = ReportPost.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
    notice_tops = NoticePost.objects.filter(notice_type=1, published_date__lte=timezone.now()).order_by('-published_date')
    paginator = Paginator(reportpost_listing, 10)
    page = request.GET.get('page')
    reportposts = paginator.get_page(page)
    return render(request, 'board/reportpost_list.html', {'reportposts': reportposts, 'notice_tops': notice_tops})

def proposalpost_list(request):
    proposalpost_listing = ProposalPost.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
    notice_tops = NoticePost.objects.filter(notice_type=1, published_date__lte=timezone.now()).order_by('-published_date')
    paginator = Paginator(proposalpost_listing, 10)
    page = request.GET.get('page')
    proposalposts = paginator.get_page(page)
    return render(request, 'board/proposalpost_list.html', {'proposalposts': proposalposts, 'notice_tops': notice_tops})

def noticepost_list(request):
    noticepost_listing = NoticePost.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
    paginator = Paginator(noticepost_listing, 10)
    page = request.GET.get('page')
    noticeposts = paginator.get_page(page)
    return render(request, 'board/noticepost_list.html', {'noticeposts': noticeposts})

@login_required
def memberpost_list(request):
    member = request.user
    memberpost_listed = sorted(
        chain(FreePost.objects.filter(author=member),
        ReportPost.objects.filter(author=member),
        ProposalPost.objects.filter(author=member),
        NoticePost.objects.filter(author=member)),
        key=lambda post: post.published_date, reverse=True)
    paginator = Paginator(memberpost_listed, 10)
    page = request.GET.get('page')
    memberposts = paginator.get_page(page)
    return render(request, 'board/memberpost_list.html', {'memberposts': memberposts})

@login_required
def membercomment_list(request):
    member = request.user
    membercomment_listed = sorted(
        chain(FreeComment.objects.filter(author=member),
        ReportComment.objects.filter(author=member),
        ProposalComment.objects.filter(author=member),
        NoticeComment.objects.filter(author=member)),
        key=lambda comment: comment.published_date, reverse=True)
    paginator = Paginator(membercomment_listed, 20)
    page = request.GET.get('page')
    membercomments = paginator.get_page(page)
    return render(request, 'board/membercomment_list.html', {'membercomments': membercomments})

@login_required
def member_info(request):
    member = request.user
    return render(request, 'board/member_info.html', {'member': member})

login_required
def member_info_change(request):
    member = request.user
    if request.method == "POST":
        form = UserChangeForm(request.POST, instance=member)
        if form.is_valid():
            member = form.save(commit=False)
            member.save()
            message = "회원정보가 변경되었습니다."
            return redirect('member_info')
    else:
        form = UserChangeForm(instance=member)
        return render(request, 'board/member_info_change.html', {'form': form})

def home(request):
    return render(request, 'board/home.html')

def freepost_detail(request, pk):
    freepost = get_object_or_404(FreePost, pk=pk)
    hit_count = HitCount.objects.get_for_object(freepost)
    hit_count_response = HitCountMixin.hit_count(request, hit_count)
    return render(request, 'board/freepost_detail.html', {'freepost': freepost})
    
def reportpost_detail(request, pk):
    reportpost = get_object_or_404(ReportPost, pk=pk)
    hit_count = HitCount.objects.get_for_object(reportpost)
    hit_count_response = HitCountMixin.hit_count(request, hit_count)
    return render(request, 'board/reportpost_detail.html', {'reportpost': reportpost})

def proposalpost_detail(request, pk):
    proposalpost = get_object_or_404(ProposalPost, pk=pk)
    hit_count = HitCount.objects.get_for_object(proposalpost)
    hit_count_response = HitCountMixin.hit_count(request, hit_count)
    return render(request, 'board/proposalpost_detail.html', {'proposalpost': proposalpost})

def noticepost_detail(request, pk):
    noticepost = get_object_or_404(NoticePost, pk=pk)
    hit_count = HitCount.objects.get_for_object(noticepost)
    hit_count_response = HitCountMixin.hit_count(request, hit_count)
    return render(request, 'board/noticepost_detail.html', {'noticepost': noticepost})

@login_required
def freepost_new(request):
    if request.method == "POST":
        form = FreePostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('freepost_detail', pk=post.pk)
    else:
        form = FreePostForm()
    return render(request, 'board/freepost_edit.html', {'form': form})

@login_required
def reportpost_new(request):
    if request.method == "POST":
        form = ReportPostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('reportpost_detail', pk=post.pk)
    else:
        form = ReportPostForm()
    return render(request, 'board/reportpost_edit.html', {'form': form})

@login_required
def proposalpost_new(request):
    if request.method == "POST":
        form = ProposalPostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=Falses)
            post.author = request.user
            post.save()
            return redirect('proposalpost_detail', pk=post.pk)
    else:
        form = ProposalPostForm()
    return render(request, 'board/proposalpost_edit.html', {'form': form})

@login_required
@staff_member_required
def noticepost_new(request):
    if request.method == "POST":
        form = NoticePostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('noticepost_detail', pk=post.pk)
    else:
        form = NoticePostForm()
    return render(request, 'board/noticepost_edit.html', {'form': form})

@login_required
def freepost_edit(request, pk):
    post = get_object_or_404(FreePost, pk=pk)
    if request.method == "POST":
        form = FreePostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.last_edit_date = timezone.now()
            post.number_of_edits += 1
            post.save()
            return redirect('freepost_detail', pk=post.pk)
    else:
        if post.author == User.objects.get(username = request.user.get_username()): 
            form = FreePostForm(instance=post)
            return render(request, 'board/freepost_edit.html', {'form': form})
        else:
            return HttpResponse('작성자가 아닙니다.')

@login_required
def reportpost_edit(request, pk):
    post = get_object_or_404(ReportPost, pk=pk)
    if request.method == "POST":
        form = ReportPostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.last_edit_date = timezone.now()
            post.number_of_edits += 1
            post.save()
            return redirect('reportpost_detail', pk=post.pk)
    else:
        if post.author == User.objects.get(username = request.user.get_username()): 
            form = ReportPostForm(instance=post)
            return render(request, 'board/reportpost_edit.html', {'form': form})
        else:
            return HttpResponse('작성자가 아닙니다.')

@login_required
def proposalpost_edit(request, pk):
    post = get_object_or_404(ProposalPost, pk=pk)
    if request.method == "POST":
        form = ProposalPostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.last_edit_date = timezone.now()
            post.number_of_edits += 1
            post.save()
            return redirect('proposalpost_detail', pk=post.pk)
    else:
        if post.author == User.objects.get(username = request.user.get_username()): 
            form = ProposalPostForm(instance=post)
            return render(request, 'board/proposalpost_edit.html', {'form': form})
        else:
            return HttpResponse('작성자가 아닙니다.')

@login_required
@staff_member_required
def noticepost_edit(request, pk):
    post = get_object_or_404(NoticePost, pk=pk)
    if request.method == "POST":
        form = NoticePostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.last_edit_date = timezone.now()
            post.number_of_edits += 1
            post.save()
            return redirect('noticepost_detail', pk=post.pk)
    else:
        if post.author == User.objects.get(username = request.user.get_username()): 
            form = NoticePostForm(instance=post)
            return render(request, 'board/noticepost_edit.html', {'form': form})
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
            return redirect('noticepost_detail', pk=noticepost.pk)
    else:
        return HttpResponseBadRequest('오류가 발생했습니다. 관리자에게 문의하세요.')

def signup(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            new_user = User.objects.create_user(**form.cleaned_data)
            login(request, new_user)
            return redirect('home')
        else:
            return HttpResponse('이미 존재하는 아이디입니다')
    else:
        form = UserForm()
        return render(request, 'board/signup.html', {'form': form})

# 좋아요/싫어요 기능. 출처: 초보몽키의 개발공부로그
@login_required
@require_POST
def freepost_like(request):
    if request.method == 'POST':
        user = request.user
        freepost_id = request.POST.get('pk', None)
        freepost = FreePost.objects.get(pk = freepost_id)
        
        if user == freepost.author:
            message = '자신의 글은 좋아요 하실 수 없습니다'
        else:
            if freepost.likes.filter(id = user.id).exists():
                freepost.likes.remove(user)
                message = '좋아요를 취소하셨습니다'
            elif freepost.hates.filter(id = user.id).exists():
                message = '싫어요를 취소한 후 좋아요를 누르실 수 있습니다'
            else:
                freepost.likes.add(user)
                message = '좋아요를 누르셨습니다'
    
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
            message = '자신의 글은 싫어요 하실 수 없습니다'
        else:
            if freepost.hates.filter(id = user.id).exists():
                freepost.hates.remove(user)
                message = '싫어요를 취소하셨습니다'
            elif freepost.likes.filter(id = user.id).exists():
                message = '좋아요를 취소한 후 좋아요를 누르실 수 있습니다'
            else:
                freepost.hates.add(user)
                message = '싫어요를 누르셨습니다'
    
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
            message = '자신의 글은 좋아요 하실 수 없습니다'
        else:
            if reportpost.likes.filter(id = user.id).exists():
                reportpost.likes.remove(user)
                message = '좋아요를 취소하셨습니다'
            elif reportpost.hates.filter(id = user.id).exists():
                message = '싫어요를 취소한 후 좋아요를 누르실 수 있습니다'
            else:
                reportpost.likes.add(user)
                message = '좋아요를 누르셨습니다'
    
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
            message = '자신의 글은 싫어요 하실 수 없습니다'
        else:
            if reportpost.hates.filter(id = user.id).exists():
                reportpost.hates.remove(user)
                message = '싫어요를 취소하셨습니다'
            elif reportpost.likes.filter(id = user.id).exists():
                message = '좋아요를 취소한 후 좋아요를 누르실 수 있습니다'
            else:
                reportpost.hates.add(user)
                message = '싫어요를 누르셨습니다'
    
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
            message = '자신의 글은 좋아요 하실 수 없습니다'
        else:
            if proposalpost.likes.filter(id = user.id).exists():
                proposalpost.likes.remove(user)
                message = '좋아요를 취소하셨습니다'
            elif proposalpost.hates.filter(id = user.id).exists():
                message = '싫어요를 취소한 후 좋아요를 누르실 수 있습니다'
            else:
                proposalpost.likes.add(user)
                message = '좋아요를 누르셨습니다'
    
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
            message = '자신의 글은 싫어요 하실 수 없습니다'
        else:
            if proposalpost.hates.filter(id = user.id).exists():
                proposalpost.hates.remove(user)
                message = '싫어요를 취소하셨습니다'
            elif proposalpost.likes.filter(id = user.id).exists():
                message = '좋아요를 취소한 후 좋아요를 누르실 수 있습니다'
            else:
                proposalpost.hates.add(user)
                message = '싫어요를 누르셨습니다'
    
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
            message = '자신의 글은 좋아요 하실 수 없습니다'
        else:
            if noticepost.likes.filter(id = user.id).exists():
                noticepost.likes.remove(user)
                message = '좋아요를 취소하셨습니다'
            elif noticepost.hates.filter(id = user.id).exists():
                message = '싫어요를 취소한 후 좋아요를 누르실 수 있습니다'
            else:
                noticepost.likes.add(user)
                message = '좋아요를 누르셨습니다'
    
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
            message = '자신의 글은 싫어요 하실 수 없습니다'
        else:
            if noticepost.hates.filter(id = user.id).exists():
                noticepost.hates.remove(user)
                message = '싫어요를 취소하셨습니다'
            elif noticepost.likes.filter(id = user.id).exists():
                message = '좋아요를 취소한 후 좋아요를 누르실 수 있습니다'
            else:
                noticepost.hates.add(user)
                message = '싫어요를 누르셨습니다'
    
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
            message = '자신의 댓글은 좋아요 하실 수 없습니다'
        else:
            if freecomment.likes.filter(id = user.id).exists():
                freecomment.likes.remove(user)
                message = '좋아요를 취소하셨습니다'
            elif freecomment.hates.filter(id = user.id).exists():
                message = '싫어요를 취소한 후 좋아요를 누르실 수 있습니다'
            else:
                freecomment.likes.add(user)
                message = '좋아요를 누르셨습니다'
    
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
            message = '자신의 댓글은 싫어요 하실 수 없습니다'
        else:
            if freecomment.hates.filter(id = user.id).exists():
                freecomment.hates.remove(user)
                message = '싫어요를 취소하셨습니다'
            elif freecomment.likes.filter(id = user.id).exists():
                message = '좋아요를 취소한 후 좋아요를 누르실 수 있습니다'
            else:
                freecomment.hates.add(user)
                message = '싫어요를 누르셨습니다'
    
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
            message = '자신의 댓글은 좋아요 하실 수 없습니다'
        else:
            if reportcomment.likes.filter(id = user.id).exists():
                reportcomment.likes.remove(user)
                message = '좋아요를 취소하셨습니다'
            elif reportcomment.hates.filter(id = user.id).exists():
                message = '싫어요를 취소한 후 좋아요를 누르실 수 있습니다'
            else:
                reportcomment.likes.add(user)
                message = '좋아요를 누르셨습니다'
    
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
            message = '자신의 댓글은 싫어요 하실 수 없습니다'
        else:
            if reportcomment.hates.filter(id = user.id).exists():
                reportcomment.hates.remove(user)
                message = '싫어요를 취소하셨습니다'
            elif reportcomment.likes.filter(id = user.id).exists():
                message = '좋아요를 취소한 후 좋아요를 누르실 수 있습니다'
            else:
                reportcomment.hates.add(user)
                message = '싫어요를 누르셨습니다'
    
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
            message = '자신의 댓글은 좋아요 하실 수 없습니다'
        else:
            if proposalcomment.likes.filter(id = user.id).exists():
                proposalcomment.likes.remove(user)
                message = '좋아요를 취소하셨습니다'
            elif proposalcomment.hates.filter(id = user.id).exists():
                message = '싫어요를 취소한 후 좋아요를 누르실 수 있습니다'
            else:
                proposalcomment.likes.add(user)
                message = '좋아요를 누르셨습니다'
    
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
            message = '자신의 댓글은 싫어요 하실 수 없습니다'
        else:
            if proposalcomment.hates.filter(id = user.id).exists():
                proposalcomment.hates.remove(user)
                message = '싫어요를 취소하셨습니다'
            elif proposalcomment.likes.filter(id = user.id).exists():
                message = '좋아요를 취소한 후 좋아요를 누르실 수 있습니다'
            else:
                proposalcomment.hates.add(user)
                message = '싫어요를 누르셨습니다'
    
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
            message = '자신의 댓글은 좋아요 하실 수 없습니다'
        else:
            if noticecomment.likes.filter(id = user.id).exists():
                noticecomment.likes.remove(user)
                message = '좋아요를 취소하셨습니다'
            elif noticecomment.hates.filter(id = user.id).exists():
                message = '싫어요를 취소한 후 좋아요를 누르실 수 있습니다'
            else:
                noticecomment.likes.add(user)
                message = '좋아요를 누르셨습니다'
    
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
            message = '자신의 댓글은 싫어요 하실 수 없습니다'
        else:
            if noticecomment.hates.filter(id = user.id).exists():
                noticecomment.hates.remove(user)
                message = '싫어요를 취소하셨습니다'
            elif noticecomment.likes.filter(id = user.id).exists():
                message = '좋아요를 취소한 후 좋아요를 누르실 수 있습니다'
            else:
                noticecomment.hates.add(user)
                message = '싫어요를 누르셨습니다'
    
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

