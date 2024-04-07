from django.urls import reverse, reverse_lazy
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import UpdateView
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib import messages
from .forms import LoginForm, UserRegistrationForm, \
    ProfileEditForm, UserPasswordChangeForm
from .models import Profile
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from ipware import get_client_ip
import requests

#
@login_required
def dashboard(request):
    return render(request,
                  'account/dashboard.html',
                  {'section': 'dashboard'})


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            return render(request, 'account/register_done.html', {'new_user': user})
    else:
        form = UserRegistrationForm()
    return render(request, 'account/register.html', {'form': form})


# @login_required
# def edit(request):
#     if request.method == 'POST':
#         user_form = UserEditForm(instance=request.user,
#                                  data=request.POST)
#         profile_form = ProfileEditForm(
#                                     instance=request.user.profile,
#                                     data=request.POST,
#                                     files=request.FILES)
#         if user_form.is_valid() and profile_form.is_valid():
#             user_form.save()
#             profile_form.save()
#             messages.success(request, 'Profile updated '\
#                                       'successfully')
#         else:
#             messages.error(request, 'Error updating your profile')
#     else:
#         user_form = UserEditForm(instance=request.user)
#         profile_form = ProfileEditForm(
#                                     instance=request.user.profile)
#     return render(request,
#                   'account/edit.html',
#                   {'user_form': user_form,
#                    'profile_form': profile_form})

class LoginUser(LoginView):
    form_class = LoginForm
    template_name = 'account/login.html'
    extra_context = {'title': 'Авторизация'}

    # def get_success_url(self):
    #     return reverse_lazy('dashboard')


@login_required
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('account:login'))


@login_required
def test_redir(request):
    return render(request, 'account/test_redir.html')


class ProfileUser(LoginRequiredMixin, UpdateView):
    model = Profile()
    form_class = ProfileEditForm
    template_name = 'account/profile.html'
    extra_context = {'title': 'Your profile'}

    def get_success_url(self):
        return reverse_lazy('account:profile')

    def get_object(self, queryset=None):
        user = self.request.user
        # Проверяем, существует ли у пользователя профиль
        if hasattr(user, 'profile'):
            return user
        # Если профиль не существует, создаем его
        else:
            profile = Profile.objects.create(user=user)
            return user


class UserPasswordChange(PasswordChangeView):
    form_class = UserPasswordChangeForm
    success_url = reverse_lazy("account:password_change_done")
    template_name = "registration/password_change_form.html"


def my_ip(request):
    # ip, _ = get_client_ip(request)
    external_ip = requests.get('https://api.ipify.org').text
    return render(request,'account/my_ip.html',{'ip':external_ip})
