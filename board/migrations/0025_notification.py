# Generated by Django 2.1.3 on 2018-12-20 09:09

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('board', '0024_auto_20181204_2137'),
    ]

    operations = [
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('verb', models.CharField(max_length=100)),
                ('board', models.CharField(max_length=20)),
                ('post_id', models.IntegerField(default=0)),
                ('is_read', models.BooleanField(default=False)),
                ('actor', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='notification_actor', to=settings.AUTH_USER_MODEL)),
                ('recipient', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='notification_recipient', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
