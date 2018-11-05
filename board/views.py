from django.shortcuts import render, get_object_or_404
from .models import FreePost, ReportPost, ProposalPost, NoticePost
from django.utils import timezone

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

