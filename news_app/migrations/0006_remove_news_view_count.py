# Generated by Django 4.2.5 on 2023-09-19 06:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('news_app', '0005_news_view_count'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='news',
            name='view_count',
        ),
    ]
