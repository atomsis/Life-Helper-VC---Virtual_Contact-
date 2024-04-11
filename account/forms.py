from datetime import datetime
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth import get_user_model
from .models import Profile

#------------------------------- Города -----------------------------
class BaseCityForm(forms.ModelForm):
    city = forms.ChoiceField(choices=[], widget=forms.Select(attrs={'class': 'form-input'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['city'].choices = self.get_city_choices()

    def get_city_choices(self):
        citys =  [
            ('Moscow', 'Москва'),
            ('Saint Petersburg', 'Санкт-Петербург'),
            ('Novosibirsk', 'Новосибирск'),
            ('Yekaterinburg', 'Екатеринбург'),
            ('Nizhny Novgorod', 'Нижний Новгород'),
            ('Kazan', 'Казань'),
            ('Chelyabinsk', 'Челябинск'),
            ('Omsk', 'Омск'),
            ('Samara', 'Самара'),
            ('Rostov-on-Don', 'Ростов-на-Дону'),
            ('Ufa', 'Уфа'),
            ('Krasnoyarsk', 'Красноярск'),
            ('Perm', 'Пермь'),
            ('Voronezh', 'Воронеж'),
            ('Volgograd', 'Волгоград'),
            ('Saratov', 'Саратов'),
            ('Krasnodar', 'Краснодар'),
            ('Tolyatti', 'Тольятти'),
            ('Izhevsk', 'Ижевск'),
            ('Ulyanovsk', 'Ульяновск'),
            ('Barnaul', 'Барнаул'),
            ('Vladivostok', 'Владивосток'),
            ('Yaroslavl', 'Ярославль'),
            ('Irkutsk', 'Иркутск'),
            ('Tyumen', 'Тюмень'),
            ('Khabarovsk', 'Хабаровск'),
            ('Makhachkala', 'Махачкала'),
            ('Orenburg', 'Оренбург'),
            ('Novokuznetsk', 'Новокузнецк'),
            ('Tomsk', 'Томск'),
            ('Kemerovo', 'Кемерово'),
            ('Astrakhan', 'Астрахань'),
            ('Kirov', 'Киров'),
            ('Penza', 'Пенза'),
            ('Lipetsk', 'Липецк'),
            ('Cheboksary', 'Чебоксары'),
            ('Tula', 'Тула'),
            ('Kaliningrad', 'Калининград'),
            ('Balashikha', 'Балашиха'),
            ('Kursk', 'Курск'),
            ('Sevastopol', 'Севастополь'),
            ('Sochi', 'Сочи'),
            ('Arkhangelsk', 'Архангельск'),
            ('Stavropol', 'Ставрополь'),
            ('Smolensk', 'Смоленск'),
            ('Kurgan', 'Курган'),
            ('Surgut', 'Сургут'),
        ]

        return sorted(citys,key=lambda x:x[1])

#----------------------------------- LOGIN AND REGISTTRATION -----------------------
class LoginForm(AuthenticationForm):
    username = forms.CharField(max_length=255, label='Логин', widget=forms.TextInput(attrs={'class': 'form-input'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-input'}), label='Пароль,')


class UserRegistrationForm(BaseCityForm):
    username = forms.CharField(max_length=255, label='Login')
    password = forms.CharField(label='Password',
                               widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat password',
                                widget=forms.PasswordInput)
    email = forms.EmailField(label='E-mail')

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
            profile = Profile.objects.create(
                user=user,
                city=self.cleaned_data['city'],
                date_of_birth=self.cleaned_data['date_of_birth']
            )
            profile.save()
        return user

#------------------------------------ EDIT ------------------------------------------
class UserEditForm(forms.ModelForm):
    email = forms.CharField(disabled=True, label='E-mail', widget=forms.TextInput(attrs={'class': 'form-input'}))
    username = forms.CharField(disabled=True, label='Логин', widget=forms.TextInput(attrs={'class': 'form-input'}))
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email','username']

    def clean_email(self):
        data = self.cleaned_data['email']
        qs = User.objects.exclude(id=self.instance.id) \
            .filter(email=data)
        if qs.exists():
            raise forms.ValidationError('Email already in use.')
        return data


class ProfileEditForm(BaseCityForm):
    current_year = datetime.today().year
    date_of_birth = forms.DateField(
        widget=forms.SelectDateWidget(
            years=range(1900, current_year + 1),
            attrs={'class': 'form-input'}
        )
    )
    class Meta:
        model = Profile
        fields = ['city', 'date_of_birth']
        labels = {
            'date_of_birth': 'Дата рождения',
            'city': 'Город'
        }
        widgets = {
            'photo': forms.FileInput(attrs={'class': 'form-input'}),
        }

#--------------------------------------- Смена пароля ----------------------------------
class UserPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(label='Старый пароль',widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    new_password1 = forms.CharField(label='Новый пароль',widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    new_password2 = forms.CharField(label='Подтверждение нового пароля',widget=forms.PasswordInput(attrs={'class': 'form-input'}))