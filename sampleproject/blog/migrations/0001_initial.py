# Generated by Django 3.2 on 2021-07-08 15:34

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BlogPost',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=256, verbose_name='タイトル')),
                ('content', models.TextField(verbose_name='本文')),
                ('postged_at', models.DateTimeField(auto_now_add=True, verbose_name='投稿日時')),
                ('category', models.CharField(choices=[('Book', '読書'), ('Game', 'ゲーム'), ('Music', '音楽')], max_length=50, verbose_name='カテゴリ')),
            ],
        ),
    ]
