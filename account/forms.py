from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth import get_user_model
from .models import Profile


class LoginForm(AuthenticationForm):
    username = forms.CharField(max_length=255, label='Логин', widget=forms.TextInput(attrs={'class': 'form-input'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-input'}), label='Пароль,')


class UserRegistrationForm(forms.ModelForm):
    username = forms.CharField(max_length=255, label='Login')
    password = forms.CharField(label='Password',
                               widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat password',
                                widget=forms.PasswordInput)
    email = forms.EmailField(label='E-mail')
    city = forms.CharField(max_length=255)

    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'city', 'password', 'password2']
        labels = {
            'email': 'E-mail',

        }

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords don\'t match.')
        return cd['password2']

    def clean_email(self):
        data = self.cleaned_data['email']
        if User.objects.filter(email=data).exists():
            raise forms.ValidationError('Email already in use.')
        return data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
            profile = Profile.objects.create(user=user, city=self.cleaned_data['city'])
            profile.save()
        return user


# class UserEditForm(forms.ModelForm):
#     class Meta:
#         model = User
#         fields = ['first_name', 'last_name', 'email']
#
#     def clean_email(self):
#         data = self.cleaned_data['email']
#         qs = User.objects.exclude(id=self.instance.id) \
#             .filter(email=data)
#         if qs.exists():
#             raise forms.ValidationError('Email already in use.')
#         return data


class ProfileEditForm(forms.ModelForm):
    username = forms.CharField(disabled=True, label='Логин', widget=forms.TextInput(attrs={'class': 'form-input'}))
    email = forms.CharField(disabled=True, label='E-mail', widget=forms.TextInput(attrs={'class': 'form-input'}))
    date_of_birth = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-input', 'type': 'date'}))

    class Meta:
        model = Profile
        fields = ['username','email','city','date_of_birth']
        labels = {
            'date_of_birth': 'Дата рождения',
            'city': 'Город'
        }
        widgets = {
            'city': forms.TextInput(attrs={'class': 'form-input'}),
        }


class UserPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(label='Старый пароль',widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    new_password1 = forms.CharField(label='Новый пароль',widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    new_password2 = forms.CharField(label='Подтверждение нового пароля',widget=forms.PasswordInput(attrs={'class': 'form-input'}))