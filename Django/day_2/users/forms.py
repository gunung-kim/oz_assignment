from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from todo.models import User


class SignUpForm(UserCreationForm):

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        new_update_field = ('password1','password2')
        for field in new_update_field:
            self.fields[field].widget.attrs['class'] = 'form-control'
            if field == 'password1':
                self.fields[field].label = '비밀번호'
                self.fields[field].widget.attrs['placeholder'] = '비밀번호를 입력해주세요'
            else :
                self.fields[field].label = '비밀번호 확인'
                self.fields[field].widget.attrs['placeholder'] = '비밀번호 한번 더 입력해주세요'

    # def save(self, commit=True):
    #     user = super().save(commit=False)
    #     user.set_password(self.cleaned_data['password1'])
    #     if commit:
    #         user.save()
    #     return user

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('email',)
        labels = {
            'email': '이메일',
        }
        widgets = {
            'email' : forms.EmailInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'exmaple@example.com',
                }
            )
        }

class LoginForm(AuthenticationForm):

    username = forms.EmailField(
        label='이메일',
        widget = forms.EmailInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'example@example.com',
            }
        )
    )
    password = forms.CharField(
        label='비밀번호',
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': '비밀번호를 입력해주세요',
            }
        )
    )
    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.user = None

    def clean(self):
        # cleaned_data = super().clean()
        email = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        self.user = authenticate(self.request, email=email, password=password)
        if not self.user:
            raise forms.ValidationError('존재하지 않는 유저 입니다')
        if not self.user.is_active:
            raise forms.ValidationError('인증되지 않은 유저 입니다')
        self.user_cache = self.user
        return self.cleaned_data
