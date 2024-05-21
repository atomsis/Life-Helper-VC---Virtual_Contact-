from django.urls import reverse, reverse_lazy
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseBadRequest
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import UpdateView
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.forms import AuthenticationForm
from django.db import IntegrityError
from django.contrib import messages
from .forms import UserRegistrationForm, \
    ProfileEditForm, UserPasswordChangeForm, UserEditForm
from django.contrib.auth.models import User
from .models import Profile,Friendship
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
import requests


#
@login_required
def dashboard(request):
    return render(request,
                  'account/dashboard.html',
                  {'section': 'dashboard'})


def register(request):
    if request.user.is_authenticated:
        return redirect('account:profile')
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])
            try:
                user.save()
                if not Profile.objects.filter(user=user).exists():
                    Profile.objects.create(user=user)
                return render(request, 'account/register_done.html', {'new_user': user})
            except IntegrityError:
                Profile.objects.create(user=user)
                return render(request, 'account/register_done.html', {'new_user': user})
    else:
        form = UserRegistrationForm()
    return render(request, 'account/register.html', {'form': form})


@login_required
def edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user,
                                 data=request.POST)
        profile_form = ProfileEditForm(
            instance=request.user.profile,
            data=request.POST,
            files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_instance = profile_form.save(commit=False)
            if 'photo' in request.FILES:
                profile_instance.photo = request.FILES['photo']
                profile_instance.save()
                messages.success(request, 'Profile updated ' \
                                          'successfully')
                # profile_form.save()
                return redirect('account:profile')
        else:
            messages.error(request, 'Error updating your profile')
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(
            instance=request.user.profile)
    return render(request,
                  'account/profile.html',
                  {'user_form': user_form,
                   'profile_form': profile_form,
                   'section': 'profile'})


### ---------------------- LOGIN v1 ----------------------------------------
# class LoginUser(LoginView):
#     form_class = LoginForm
#     template_name = 'account/login.html'
#     extra_context = {'title': 'Авторизация'}
### -------------------------------------------------------------------------

### ------------------- LOGIN v2 --------------------------------------------
# def user_login(request):
#     if request.method == 'POST':
#         form = UserLoginForm(request.POST)
#         if form.is_valid():
#             username = form.cleaned_data['username']
#             password = form.cleaned_data['password']
#             user = authenticate(username=username, password=password)
#             if user is not None:
#                 login(request, user)
#                 return redirect('account:profile')  # Redirect to profile page after successful login
#     else:
#         form = UserLoginForm()
#     return render(request, 'account/login.html', {'form': form})
### ---------------------------------------------------------------------

### ------------------- LOGIN v3 --------------------------------------------
def login_view(request):
    if request.user.is_authenticated:
        return redirect('account:profile')
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('account:profile')
    else:
        form = AuthenticationForm()
    return render(request, 'account/login.html', {'form': form})


### ---------------------------------------------------------------------

@login_required
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('account:login'))


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
        return self.request.user.profile


class UserPasswordChange(PasswordChangeView):
    form_class = UserPasswordChangeForm
    success_url = reverse_lazy("account:password_change_done")
    template_name = "registration/password_change_form.html"


def my_ip(request):
    # ip, _ = get_client_ip(request)
    external_ip = requests.get('https://api.ipify.org').text
    return render(request, 'account/my_ip.html', {'ip': external_ip})


@login_required
def all_users(request):
    users = User.objects.exclude(pk=request.user.pk)

    friends = set(request.user.profile.get_friends())
    friend_status = {user.id: (user in friends) for user in users}

    # friend_status = {}

    # for user in users:
    #     is_friend = user in request.user.profile.get_friends()
    #     friend_status[user.id] = is_friend

    # for user in users:
    #     is_friend = Friendship.objects.filter(
    #         from_user=request.user, to_user=user
    #     ).exists() or Friendship.objects.filter(
    #         from_user=user, to_user=request.user
    #     ).exists()
    #     friend_status[user.id] = is_friend
    #
    # for k,v in friend_status.items():
    #     print(f'{k}=>{v}')

    return render(request, 'friends/all_users.html', {'users': users, 'friend_status': friend_status})


@login_required
def my_friends(request):
    user = request.user
    friends = user.profile.get_friends()
    return render(request, 'friends/friend_list.html', {'friends': friends})


@login_required
def add_friend(request):
    if request.method == 'POST':
        friend_id = request.POST.get('friend_id')
        # print(friend_id)
        try:
            friend_profile = Profile.objects.get(pk=friend_id)
            request.user.profile.add_friend(friend_profile)
            messages.success(request, 'Вы добавили нового друга')
            return redirect('account:all_users')
        except Profile.DoesNotExist:
            messages.error(request, 'Неверный ID друга')
            return HttpResponseBadRequest('Неверный ID друга')
    else:
        messages.error(request, 'Неверный метод запроса')
        return HttpResponseBadRequest('Неверный метод запроса')


@login_required
def remove_friend(request):
    if request.method == 'POST':
        friend_id = request.POST.get('friend_id')
        try:
            friend_profile = Profile.objects.get(pk=friend_id)
            request.user.profile.remove_friend(friend_profile)
            messages.success(request, 'Вы удалили друга из списка')
            return redirect('account:all_users')
        except Profile.DoesNotExist:
            messages.error(request, 'Неверный ID друга')
            return HttpResponseBadRequest('Неверный ID друга')
    else:
        messages.error(request, 'Неверный метод запроса')
        return HttpResponseBadRequest('Неверный метод запроса')