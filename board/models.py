from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class AbstractPost(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE, default=None, null=True, blank=True)
    published_date = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    content = models.TextField()
    last_edit_date = models.DateTimeField(auto_now=True)
    number_of_edits = models.IntegerField(blank=True, null=False, default=0)
    image = models.ImageField(upload_to='%Y/%m/%d/orig', blank=True, null=True)
    likes = models.ManyToManyField(User, related_name='likes', blank=True, null=True)
    hates = models.ManyToManyField(User, related_name='hates', blank=True, null=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.title
    
    def user_directory_path(instance, filename):
        return 'user_{0}/{1}'.format(instance.user.id, filename)
    
    @property
    def total_likes(self):
        return self.likes.count()
    
    @property
    def total_hates(self):
        return self.hates.count()
    
    @property
    def likes_minus_hates(self):
        return (self.likes.count()-self.hates.count())

    @property
    def published_date_for_board(self):
        today = timezone.now().date()
        if self.published_date.date() == today:
            return self.published_date.strftime('%H:%M')
        else:
            return self.published_date.strftime('%y.%m.%d')
        


class FreePost(AbstractPost):
    likes = models.ManyToManyField(User, related_name='freepost_likes', blank=True, null=True)
    hates = models.ManyToManyField(User, related_name='freepost_hates', blank=True, null=True)
    image = models.ImageField(upload_to='free/%Y/%m/%d/orig', blank=True, null=True)
    board = "Free"

    class Meta:
        abstract = False

class ReportPost(AbstractPost):
    AREA_CHOICES = (
        ('SE','서울'), 
        ('IC','인천'),
        ('GG','경기'),
        ('DJ','대전'),
        ('SJ','세종'),
        ('CB','충북'),
        ('CN','충남'),
        ('GW','강원'),
        ('GJ','광주'),
        ('JB','전북'),
        ('JN','전남'),
        ('BS','부산'),
        ('DG','대구'),
        ('US','울산'),
        ('GB','경북'),
        ('GN','경남'),
        ('JJ','제주'),
    )
    area = models.CharField(
        max_length=2,
        choices = AREA_CHOICES,
    )
    specific_area = models.CharField(max_length=200)
    image = models.ImageField(upload_to='report/%Y/%m/%d/orig', blank=False, null=False)
    likes = models.ManyToManyField(User, related_name='reportpost_likes', blank=True, null=True)
    hates = models.ManyToManyField(User, related_name='reportpost_hates', blank=True, null=True)
    board = "Report"

    class Meta:
        abstract = False
    
    @property
    def show_area(self):
        return self.get_area_display()

class ProposalPost(AbstractPost):
    PR_CHOICES = (
        ('PP', '건의'),
        ('PS', '신고'),
    )
    proposal_type = models.CharField(max_length=2, choices = PR_CHOICES)
    likes = models.ManyToManyField(User, related_name='proposalpost_likes', blank=True, null=True)
    hates = models.ManyToManyField(User, related_name='proposalpost_hates', blank=True, null=True)
    image = models.ImageField(upload_to='proposal/%Y/%m/%d/orig', blank=True, null=True)
    board = "Proposal"

    class Meta:
        abstract = False

    @property
    def show_proposal_type(self):
        return self.get_proposal_type_display()

class NoticePost(AbstractPost):
    NOTICE_CHOICES = (
        (1, '상단고정'),
        (0, '고정하지 않음'),
    )
    notice_type = models.IntegerField(choices=NOTICE_CHOICES)
    likes = models.ManyToManyField(User, related_name='noticepost_likes', blank=True, null=True)
    hates = models.ManyToManyField(User, related_name='noticepost_hates', blank=True, null=True)
    image = models.ImageField(upload_to='notice/%Y/%m/%d/orig', blank=True, null=True)
    board = "Notice"

    class Meta:
        abstract = False

class AbstractComment(AbstractPost):
    title = models.CharField(max_length=200, blank=True, null=True)
    post = models.ForeignKey('board.AbstractPost', on_delete=models.CASCADE, related_name='abstract_comments')

    class Meta:
        abstract = True
    
    def __str__(self):
        return self.content

    @property
    def published_date_for_board(self):
        today = timezone.now().date()
        if self.published_date.date() == today:
            return self.published_date.strftime('%H:%M')
        else:
            return self.published_date.strftime('%y.%m.%d')

class FreeComment(AbstractComment):
    post = models.ForeignKey('board.FreePost', on_delete=models.CASCADE, related_name='freecomments')
    likes = models.ManyToManyField(User, related_name='freecomment_likes', blank=True, null=True)
    hates = models.ManyToManyField(User, related_name='freecomment_hates', blank=True, null=True)

    class Meta:
        abstract = False

class ReportComment(AbstractComment):
    post = models.ForeignKey('board.ReportPost', on_delete=models.CASCADE, related_name='reportcomments')
    likes = models.ManyToManyField(User, related_name='reportcomment_likes', blank=True, null=True)
    hates = models.ManyToManyField(User, related_name='reportcomment_hates', blank=True, null=True)

    class Meta:
        abstract = False

class ProposalComment(AbstractComment):
    post = models.ForeignKey('board.ProposalPost', on_delete=models.CASCADE, related_name='proposalcomments')
    likes = models.ManyToManyField(User, related_name='proposalcomment_likes', blank=True, null=True)
    hates = models.ManyToManyField(User, related_name='proposalcomment_hates', blank=True, null=True)

    class Meta:
        abstract = False

class NoticeComment(AbstractComment):
    post = models.ForeignKey('board.NoticePost', on_delete=models.CASCADE, related_name='noticecomments')
    likes = models.ManyToManyField(User, related_name='noticecomment_likes', blank=True, null=True)
    hates = models.ManyToManyField(User, related_name='noticecomment_hates', blank=True, null=True)

    class Meta:
        abstract = False

