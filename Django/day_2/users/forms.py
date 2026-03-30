from django import forms
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

User = get_user_model()

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
        fields = ('email','username')
        labels = {
            'email': '이메일',
            'username': '이름',
        }
        widgets = {
            'email' : forms.EmailInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'exmaple@example.com',
                }
            ),
            'username' : forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder' : '이름을 입력하세요'
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

    def clean(self):
        cleaned_data = super().clean()
        return cleaned_data
