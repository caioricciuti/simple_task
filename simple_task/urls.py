
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.urls import path, include
from users import views as user_views

urlpatterns = [
    path('', include('task_app.urls')),
    path('super/', admin.site.urls),
    path('register/', user_views.register, name="register"),
    path('profile/', user_views.profile, name='profile'),
    path('profile/update/', user_views.profileupdate, name='profileupdate'),
    path('profile/delete/', user_views.account_delete, name='account_delete'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name="login"),
    path('logout/', auth_views.LogoutView.as_view(), name="logout"),
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='users/password_reset.html'), name="password_reset"),
    path('password_reset/done', auth_views.PasswordResetDoneView.as_view(template_name='users/password_reset_done.html'), name="password_reset_done"),
    path('password_reset_confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='users/password_reset_confirm.html'), name="password_reset_confirm"),
    path('password_reset_complete/', auth_views.PasswordResetCompleteView.as_view(template_name='users/password_reset_complete.html'), name="password_reset_complete"),
    path('activate/<uidb64>/<token>/', user_views.activate, name="activate"),    
]

handler404 = 'task_app.views.handler404'
handler403 = 'task_app.views.handler403'
handler500 = 'task_app.views.handler500'


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)