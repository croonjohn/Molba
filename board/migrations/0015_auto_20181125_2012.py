# Generated by Django 2.1.3 on 2018-11-25 11:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('board', '0014_auto_20181120_1654'),
    ]

    operations = [
        migrations.AddField(
            model_name='freecomment',
            name='author_nickname',
            field=models.CharField(default='None', max_length=100),
        ),
        migrations.AddField(
            model_name='freepost',
            name='author_nickname',
            field=models.CharField(default='None', max_length=100),
        ),
        migrations.AddField(
            model_name='noticecomment',
            name='author_nickname',
            field=models.CharField(default='None', max_length=100),
        ),
        migrations.AddField(
            model_name='noticepost',
            name='author_nickname',
            field=models.CharField(default='None', max_length=100),
        ),
        migrations.AddField(
            model_name='proposalcomment',
            name='author_nickname',
            field=models.CharField(default='None', max_length=100),
        ),
        migrations.AddField(
            model_name='proposalpost',
            name='author_nickname',
            field=models.CharField(default='None', max_length=100),
        ),
        migrations.AddField(
            model_name='reportcomment',
            name='author_nickname',
            field=models.CharField(default='None', max_length=100),
        ),
        migrations.AddField(
            model_name='reportpost',
            name='author_nickname',
            field=models.CharField(default='None', max_length=100),
        ),
    ]