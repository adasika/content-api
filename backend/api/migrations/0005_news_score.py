# Generated by Django 3.2.13 on 2022-04-25 05:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_alter_news_url'),
    ]

    operations = [
        migrations.AddField(
            model_name='news',
            name='score',
            field=models.CharField(default='', max_length=200),
        ),
    ]
