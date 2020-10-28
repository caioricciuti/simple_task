# Generated by Django 3.1.2 on 2020-10-22 10:59

from django.conf import settings
import django.contrib.auth.models
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('content', models.TextField(blank=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('due_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('Status', models.CharField(choices=[('D', 'Done'), ('P', 'Doing'), ('N', 'Not done')], default='N', max_length=1)),
                ('importance', models.CharField(choices=[('H', 'High'), ('M', 'Medium'), ('L', 'Low')], default='M', max_length=1)),
                ('departament', models.CharField(choices=[('D', 'Dev'), ('M', 'Marketing'), ('H', 'HR'), ('L', 'Legal'), ('F', 'Finances'), ('O', 'Others')], default='M', max_length=1)),
                ('is_public', models.BooleanField(default=False)),
                ('author', models.ForeignKey(default=django.contrib.auth.models.User, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('responsable', models.ForeignKey(default=models.ForeignKey(default=django.contrib.auth.models.User, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL), null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='author', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254)),
                ('body', models.TextField(help_text='Add a comment')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('active', models.BooleanField(default=True)),
                ('name', models.ForeignKey(default=django.contrib.auth.models.User, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('task', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='task_app.task')),
            ],
            options={
                'ordering': ('created',),
            },
        ),
    ]
