from django.shortcuts import render, get_object_or_404, redirect
from .models import (
    FreePost, ReportPost, ProposalPost, NoticePost, FreeComment, ReportComment, ProposalComment, NoticeComment
    )
from django.utils import timezone
from .forms import (
    FreePostForm, ReportPostForm, ProposalPostForm, NoticePostForm, FreeCommentForm, ReportCommentForm, ProposalCommentForm, NoticeCommentForm
)

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseBadRequest

def freepost_list(request):
    freeposts = FreePost.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
    return render(request,'board/freepost_list.html', {'freeposts': freeposts})

def reportpost_list(request):
    reportposts = ReportPost.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
    return render(request, 'board/reportpost_list.html', {'reportposts': reportposts})

def proposalpost_list(request):
    proposalposts = ProposalPost.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
    return render(request, 'board/proposalpost_list.html', {'proposalposts': proposalposts})

def noticepost_list(request):
    noticeposts = NoticePost.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
    return render(request, 'board/noticepost_list.html', {'noticeposts': noticeposts})

def home(request):
    return render(request, 'board/home.html')

def freepost_detail(request, pk):
    freepost = get_object_or_404(FreePost, pk=pk)
    return render(request, 'board/freepost_detail.html', {'freepost': freepost})
    
def reportpost_detail(request, pk):
    reportpost = get_object_or_404(ReportPost, pk=pk)
    return render(request, 'board/reportpost_detail.html', {'reportpost': reportpost})

def proposalpost_detail(request, pk):
    proposalpost = get_object_or_404(ProposalPost, pk=pk)
    return render(request, 'board/proposalpost_detail.html', {'proposalpost': proposalpost})

def noticepost_detail(request, pk):
    noticepost = get_object_or_404(NoticePost, pk=pk)
    return render(request, 'board/noticepost_detail.html', {'noticepost': noticepost})

@login_required
def freepost_new(request):
    if request.method == "POST":
        form = FreePostForm(request.POST)
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
        form = ReportPostForm(request.POST)
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
        form = ProposalPostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=Falses)
            post.author = request.user
            post.save()
            return redirect('proposalpost_detail', pk=post.pk)
    else:
        form = ProposalPostForm()
    return render(request, 'board/proposalpost_edit.html', {'form': form})

@login_required
def noticepost_new(request):
    if request.method == "POST":
        form = NoticePostForm(request.POST)
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
        form = FreePostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.last_edit_date = timezone.now()
            post.number_of_edits += 1
            post.save()
            return redirect('freepost_detail', pk=post.pk)
    else:
        form = FreePostForm(instance=post)
    return render(request, 'board/freepost_edit.html', {'form': form})

@login_required
def reportpost_edit(request, pk):
    post = get_object_or_404(ReportPost, pk=pk)
    if request.method == "POST":
        form = ReportPostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.last_edit_date = timezone.now()
            post.number_of_edits += 1
            post.save()
            return redirect('reportpost_detail', pk=post.pk)
    else:
        form = ReportPostForm(instance=post)
    return render(request, 'board/reportpost_edit.html', {'form': form})

@login_required
def proposalpost_edit(request, pk):
    post = get_object_or_404(ProposalPost, pk=pk)
    if request.method == "POST":
        form = ProposalPostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.last_edit_date = timezone.now()
            post.number_of_edits += 1
            post.save()
            return redirect('proposalpost_detail', pk=post.pk)
    else:
        form = ProposalPostForm(instance=post)
    return render(request, 'board/proposalpost_edit.html', {'form': form})

@login_required
def noticepost_edit(request, pk):
    post = get_object_or_404(NoticePost, pk=pk)
    if request.method == "POST":
        form = NoticePostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.last_edit_date = timezone.now()
            post.number_of_edits += 1
            post.save()
            return redirect('noticepost_detail', pk=post.pk)
    else:
        form = NoticePostForm(instance=post)
    return render(request, 'board/noticepost_edit.html', {'form': form})

@login_required
def freepost_remove(request, pk):
    post = get_object_or_404(FreePost, pk=pk)
    post.delete()
    return redirect('freepost_list')

@login_required
def reportpost_remove(request, pk):
    post = get_object_or_404(ReportPost, pk=pk)
    post.delete()
    return redirect('reportpost_list')

@login_required
def proposalpost_remove(request, pk):
    post = get_object_or_404(ProposalPost, pk=pk)
    post.delete()
    return redirect('proposalpost_list')

@login_required
def noticepost_remove(request, pk):
    post = get_object_or_404(NoticePost, pk=pk)
    post.delete()
    return redirect('noticepost_list')

@login_required
def add_freecomment_to_freepost(request, pk):
    freepost = get_object_or_404(FreePost, pk=pk)
    if request.method == "POST":
        form = FreeCommentForm(request.POST)
        if form.is_valid():
            freecomment = form.save(commit=False)
            freecomment.post = freepost
            freecomment.author = request.author
            freecomment.save()
            return redirect('freepost_detail', pk=freepost.pk)
    else:
        form = FreeCommentForm()
    return render(request, 'add_freecomment_to_freepost.html', {'form': form})

@login_required
def add_reportcomment_to_reportpost(request, pk):
    reportpost = get_object_or_404(ReportPost, pk=pk)
    if request.method == "POST":
        form = ReportCommentForm(request.POST)
        if form.is_valid():
            reportcomment = form.save(commit=False)
            reportcomment.post = reportpost
            reportcomment.author = request.author
            reportcomment.save()
            return HttpResponse("댓글이 등록되었습니다.")
    else:
        form = ReportCommentForm()
        return HttpResponseBadRequest()

@login_required
def add_proposalcomment_to_proposalpost(request, pk):
    proposalpost = get_object_or_404(ProposalPost, pk=pk)
    if request.method == "POST":
        form = ProposalCommentForm(request.POST)
        if form.is_valid():
            proposalcomment = form.save(commit=False)
            proposalcomment.post = proposalpost
            proposalcomment.author = request.author
            proposalcomment.save()
            return HttpResponse("댓글이 등록되었습니다.")
    else:
        form = ProposalCommentForm()
        return HttpResponseBadRequest()

@login_required
def add_noticecomment_to_noticepost(request, pk):
    noticepost = get_object_or_404(NoticePost, pk=pk)
    if request.method == "POST":
        form = NoticeCommentForm(request.POST)
        if form.is_valid():
            noticecomment = form.save(commit=False)
            noticecomment.post = noticepost
            noticecomment.author = request.author
            noticecomment.save()
            return HttpResponse("댓글이 등록되었습니다.")
    else:
        form = NoticeCommentForm()
        return HttpResponseBadRequest()
        

