# Generated by Django 4.2.10 on 2024-04-14 01:10

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='HistoryList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('thread_title', models.CharField(max_length=255, verbose_name='スレッドタイトル')),
                ('url', models.CharField(max_length=255, verbose_name='url')),
            ],
        ),
    ]
