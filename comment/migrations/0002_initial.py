# Generated by Django 5.0.6 on 2024-07-05 10:23

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('comment', '0001_initial'),
        ('post', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='commentlikemodel',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='commnentmodel',
            name='parent',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='comment.commnentmodel'),
        ),
        migrations.AddField(
            model_name='commnentmodel',
            name='post',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='post.postusermodel'),
        ),
        migrations.AddField(
            model_name='commnentmodel',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='commentlikemodel',
            name='comment',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='comment.commnentmodel'),
        ),
    ]
