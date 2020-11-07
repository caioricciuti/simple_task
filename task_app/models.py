from django.contrib import admin
from django.utils import timezone
from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from ckeditor.fields import RichTextField

class Task(models.Model):
    title = models.CharField(max_length=50)
    content = RichTextField(blank=True,null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    due_date = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, default=User)
    responsable = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, related_name="author", default=User)
    STATUS_CHOICES = [('D', 'Done'),('P','Doing'),('N','Not done')]
    Status = models.CharField(max_length=1,choices=STATUS_CHOICES, default='N')
    IMPORTANCE_CHOICES = [('H', 'High'),('M','Medium'),('L','Low')]
    importance = models.CharField(max_length=1,choices=IMPORTANCE_CHOICES, default='M')
    DEPARTAMENT_CHOICES = [('D', 'Dev'),('M','Marketing'),('H','HR'),('L','Legal'),('F','Finances'),('O','Others')]
    departament = models.CharField(max_length=1,choices=DEPARTAMENT_CHOICES, default='M')
    is_public = models.BooleanField(default=False, help_text="If you check this, anyone will be able to see and comment in your task (otherwise, only you and the responsable can see it)")

    def  __str__(self):
        return '%s - %s' % (self.title, self.author)

    def get_absolute_url(self): 
        return reverse("task-detail", kwargs={"pk": self.pk})
    class Meta:
      ordering = ('due_date',)

class Comment(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User,  null=True, on_delete=models.SET_NULL, default=User)
    body = RichTextField(blank=True,null=True)
    #body = models.TextField(help_text='Add a comment')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
      ordering = ('created',)

    def __str__(self):
      return '%s - %s' % (self.task.title, self.author)
    
    def get_absolute_url(self):
      return reverse('task-detail', kwargs={'pk': self.pk})