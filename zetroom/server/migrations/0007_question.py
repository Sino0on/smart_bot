# Generated by Django 4.0.6 on 2022-07-29 11:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('server', '0006_course_image_meeting_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('answer', models.TextField()),
                ('datetime', models.DateTimeField(auto_now_add=True)),
                ('Course', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='server.course')),
            ],
            options={
                'verbose_name': 'Вопрос',
                'verbose_name_plural': 'Вопросы',
                'ordering': ['-datetime'],
            },
        ),
    ]
