from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import PasswordChangeView, PasswordChangeDoneView, PasswordResetView, \
    PasswordResetDoneView
from . import views
from django.urls import reverse_lazy

app_name = 'account'

urlpatterns = [
    # --------------authentication---------------------------------------------------
    path('register/', views.register, name='register'),
    path('login/', views.LoginUser.as_view(), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('password-change/', views.UserPasswordChange.as_view(), name='password_change'),
    path('password-change/done/', PasswordChangeDoneView.as_view(), name='password_change_done'),
    path('password-reset/',
         PasswordResetView.as_view(
             template_name="registration/password_reset_form.html",
             email_template_name="registration/password_reset_email.html",
             success_url=reverse_lazy('account:password_reset_done')
         ),
         name='password_reset'),
    path('password-reset/done/',
         PasswordResetDoneView.as_view(
             template_name="registration/password_reset_done.html"
         ),
         name='password_reset_done'),
    path('password-reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name="registration/password_reset_confirm.html",
             success_url=reverse_lazy('account:password_reset_complete')),
         name='password_reset_confirm'),
    path('password-reset/complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name="registration/password_reset_complete.html"),
         name='password_reset_complete'),
    # --------------------------------------------------------------------------------

    path('', views.dashboard, name='dashboard'),
    path('test_redir/', views.test_redir, name='test_redir'),
    path('profile/', views.edit, name='profile'),
    path('my_ip/',views.my_ip,name='my_ip')

    # path('edit/', views.edit, name='edit'),
]
