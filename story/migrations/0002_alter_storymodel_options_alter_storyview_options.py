# Generated by Django 5.0.6 on 2024-07-11 11:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('story', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='storymodel',
            options={'ordering': ['-expiry_time'], 'verbose_name': 'Story', 'verbose_name_plural': 'Stories'},
        ),
        migrations.AlterModelOptions(
            name='storyview',
            options={'ordering': ['-id'], 'verbose_name': 'StoryView', 'verbose_name_plural': 'StoryViews'},
        ),
    ]
