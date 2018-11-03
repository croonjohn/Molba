from django.db import models
from django.utils import timezone

class AbstractPost(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    publisehd_date = models.DateTimeField(auto_now_add=True)
    content = models.TextField()
    last_edit_date = models.DateTimeField(auto_now=True)
    number_of_edits = models.IntegerField(blank=True, null=False, default=0)
    parent = models.CharField(max_length=10, default='Free')
    image = models.ImageField(upload_to='uploads/%Y/%m/%d/orig', blank=True, null=True)

    class Meta:
        abstract = True

    def publish(self):
        self.published_date = timezone.now()
        self.number_of_edits = 0
        self.last_edit_date = published_date
        self.save()
    
    def edit(self, original_published_date):
        self.published_date = original_published_date
        self.last_edit_date = timezone.now()
        self.number_of_edits += 1
        self.save()

    def __str__(self):
        return self.title
    
    def user_directory_path(instance, filename):
        return 'user_{0}/{1}'.format(instance.user.id, filename)

class FreePost(AbstractPost):
    parent = 'Free'
    
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
    parent = 'Report'
    specific_area = models.CharField(max_length=200)
    image = models.ImageField(upload_to='uploads/%Y/%m/%d/orig', blank=False, null=False)

    class Meta:
        abstract = False

class ProposalPost(AbstractPost):
    parent = 'Proposal'
    PR_CHOICES = (
        ('PP', '건의'),
        ('PS', '신고'),
    )
    proposal_type = models.CharField(max_length=2, choices = PR_CHOICES)

    class Meta:
        abstract = False

class NoticePost(AbstractPost):
    parent = 'Notice'
    NOTICE_CHOICES = (
        (1, '상단고정'),
        (0, '고정하지 않음'),
    )
    notice_type = models.IntegerField(choices=NOTICE_CHOICES)

    class Meta:
        abstract = False

'''class Comment(models.Model):
    post = models.ForeignKey('board.FreePost', on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    published_date = models.DateTimeField(blank=True, null=True)
    approved_comment = models.BooleanField(default=False)
    number_of_edits = models.IntegerField(default=0)
    last_edit_date = models.DateTimeField(blank=True, null=True)
    content = models.TextField()

    def approve(self):
        self.published_date = timezone.now()
        self.approved_comment = True
        self.number_of_edits = 0
        self.save()
    
    def edit(self, original_published_date):
        self.published_date = original_published_date
        self.last_edit_date = timezone.now()
        self.number_of_edits += 1
        self.save()

    def __str__(self):
        return self.text
'''
