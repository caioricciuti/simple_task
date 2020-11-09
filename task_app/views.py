from django.shortcuts import render, redirect, reverse
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Task, Comment
from django.contrib.auth.models import User
from django.db.models import Q
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.utils import timezone
import datetime
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from bootstrap_datepicker_plus import DateTimePickerInput
from django.core.mail import EmailMessage
from django.http import HttpResponse
from django.template.loader import render_to_string
def index_app(request):
    if request.user.is_authenticated:
        return redirect('task/')
    else:
        return render(request, 'task_app/index.html')
       
class DashboardTaskAppView(LoginRequiredMixin, ListView):
    model = Task
    template_name = "task_app/task_dashboard.html"
    context_object_name = 'tasks'
    today = datetime.date.today()

    def queryset(self):
        ordering = ['-due_date']
        usr = self.request.user
        return Task.objects.filter(Q(responsable=usr))

class DashboardTaskAppViewPublic(LoginRequiredMixin, ListView):
    model = Task
    template_name = "task_app/task_dashboard_public.html"
    context_object_name = 'tasks'
    today = datetime.date.today()

    def queryset(self):
        return Task.objects.filter(Q(is_public=True))

class TaskDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Task

    def test_func(self):
        task = self.get_object()
        if self.request.user == task.author or self.request.user == task.responsable or task.is_public == True:
            return True 
        else:
            return False

class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    fields = ['title','content','due_date','responsable','importance','departament','is_public']

    def get_form(self):
        form = super().get_form()
        form.fields['due_date'].widget = DateTimePickerInput()
        return form

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.date_created = timezone.now()
        form.instance.Status = "N"
        current_site = ('https://simpletask.caioricciuti.com/task')
        title = form.cleaned_data.get('title')
        responsable = form.cleaned_data.get('responsable')
        mail_subject = f'{title} | Simple Task.'
        message = render_to_string('task_app/task_create_email.html', {
                'user': responsable,
                'title': title,
                'author': form.instance.author,
                'domain': current_site,                
            })
        to_email = responsable.email
        email = EmailMessage(
                mail_subject, message, to=[to_email]
            )
        email.send()
        messages.success(self.request, f'Nice, {title} created! In this page you can update, comment and delete your task, have fun!')
        return super().form_valid(form)

class TaskUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):

    model = Task
    fields = ['title','content','due_date','responsable','importance','departament','Status','is_public']
    def get_form(self):
        form = super().get_form()
        form.fields['due_date'].widget = DateTimePickerInput()
        return form
    def form_valid(self, form):
        if form.is_valid:
            form.instance.author = self.request.user
            form.instance.date_created = timezone.now()
            title = form.cleaned_data.get('title')
            messages.info(self.request, f'You just updated: {title}!')
            return super().form_valid(form)
        else: 
            pass

    def test_func(self):
        task = self.get_object()
        if self.request.user == task.author:
            return True
        else:
            return False

class TaskDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Task

    def test_func(self):
        task = self.get_object()
        if self.request.user == task.author:
            return True
        else:
            return False

    def get_success_url(self, *args, **kwargs):
        success_url = ('/task')
        messages.warning(self.request, 'Task DELETED!')
        return success_url


class TaskSearchView(LoginRequiredMixin, ListView):
    template_name = 'task_app/task_search.html'
    model = Task

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            object_list = self.model.objects.filter(title__icontains=query)
            #object_list = self.model.objects.filter(title__icontains=query)
        else:
            object_list = self.model.objects.none()
        return object_list

class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    fields = ['body']
    
    def form_valid(self, form):
        form.instance.task_id = self.kwargs['pk']
        form.instance.author = self.request.user
        form.instance.created = timezone.now()
        form.save()
        messages.success(self.request, 'Comment created!')
        return super().form_valid(form)

    def get_success_url(self):
        task_number = Task.objects.get(pk=self.kwargs.get('pk'))
        return task_number.get_absolute_url()


class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Comment
    fields = ['body']

    def form_valid(self, form):
        messages.info(self.request, 'Comment updated!')
        return super().form_valid(form)

    def test_func(self):
        comment = self.get_object()
        if self.request.user == comment.author:
            return True
        else:
            return False
            
    def get_success_url(self):
        return reverse('task-detail', kwargs={'pk': self.get_object().task.pk})

class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment

    def test_func(self):
        task = self.get_object()
        if self.request.user == task.author:
            return True
        else:
            return False
    
    def get_success_url(self):
        messages.warning(self.request, 'Comment DELETED!')
        return reverse('task-detail', kwargs={'pk': self.get_object().task.pk})
    

def doc_taskapp(request):
    return render(request, 'task_app/task_docs.html')

def handler404(request, exception):
    return render(request, '404.html', status=404)

def handler500(request):
    return render(request, '500.html', status=500)
    
def handler403(request, exception):
    return render(request, '403.html', status=403)