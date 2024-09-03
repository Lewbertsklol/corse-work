# Generated by Django 5.1 on 2024-09-03 08:17

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Создан')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Обновлен')),
                ('title', models.CharField(max_length=255, verbose_name='Заголовок')),
                ('text', models.TextField(verbose_name='Текст')),
                ('image', models.ImageField(blank=True, null=True, upload_to='posts', verbose_name='Изображение')),
                ('views_count', models.PositiveIntegerField(default=0, verbose_name='Количество просмотров')),
            ],
            options={
                'verbose_name': 'Пост',
                'verbose_name_plural': 'Посты',
                'ordering': ['-created_at'],
            },
        ),
    ]
