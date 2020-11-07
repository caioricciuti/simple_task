from django.urls import path, include
from . import views
from .views import (DashboardTaskAppView, 
                    TaskDetailView,
                    TaskCreateView, 
                    TaskUpdateView, 
                    DashboardTaskAppViewPublic,
                    TaskDeleteView,
                    CommentCreateView,
                    CommentUpdateView,
                    CommentDeleteView,
                    TaskSearchView
                    )

urlpatterns = [
    path('', views.index_app, name="home-app"),
    path('task/', DashboardTaskAppView.as_view(), name="task-home"),
    path('task/public', DashboardTaskAppViewPublic.as_view(), name="task-home-public"),
    path('task/new_task/', TaskCreateView.as_view(), name='task-create'),
    path('task/<int:pk>/', TaskDetailView.as_view(), name='task-detail'),
    path('task/<int:pk>/update', TaskUpdateView.as_view(), name='task-update'),
    path('task/<int:pk>/delete', TaskDeleteView.as_view(), name='task-delete'),
    path('task/<int:pk>/comment', CommentCreateView.as_view(), name='task-comment'),
    path('task/comment/<int:pk>/update', CommentUpdateView.as_view(), name='task-comment-update'),
    path('task/comment/<int:pk>/delete', CommentDeleteView.as_view(), name='task-comment-delete'),
    path('docs/', views.doc_taskapp, name="task-doc"),
    path('task/results', TaskSearchView.as_view(), name="task-search"),
]