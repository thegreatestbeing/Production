from django.conf import settings
from django.urls import include, path, re_path, reverse_lazy
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    re_path(r'^email/confirm/(?P<link>[0-9A-Za-z]+)/$', views.EmailActivate.as_view(), name='email-activate'),
    re_path(r'^email/resend/$', views.EmailActivate.as_view(), name='resend-activation'),
    
    re_path(r"^login/$", views.Login, name="login"),
    re_path(r"^logout/$", views.Logout, name="logout"),

    re_path(r'^otp/confirm/$', views.OTPActivate, name='otp-activate'),
    # url(r'^auth/$', views.TwoStepAuth.as_view(), name='Two-step-authentication'),
    # url(r'^otp/resend/$', views.OTPResend.as_view(), name='resend-otp'),
    
    path('password/change/', auth_views.PasswordChangeView.as_view(template_name='password/change.html'), name='password_change'),
    path('password/change/done/', auth_views.PasswordChangeDoneView.as_view(template_name='password/change_done.html'), name='password_change_done'),

    path('password/reset/', auth_views.PasswordResetView.as_view(template_name='password/reset_form.html', email_template_name='email/password_reset_email.html', success_url=reverse_lazy('account:password_reset_done')), name='password_reset'),
    path('password/reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='password/reset_done.html'), name='password_reset_done'),
    path('password/reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='password/reset_confirm.html'), name='password_reset_confirm'),
    path('password/reset/complete/', auth_views.PasswordResetCompleteView.as_view(template_name='password/reset_complete.html'), name='password_reset_complete'),

    re_path(r"^signup/$", views.Signup, name="signup"),
]

app_name = 'account'


