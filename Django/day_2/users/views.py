from django.contrib.auth.forms import AuthenticationForm,UserCreationForm
from django.core import signing
from django.core.exceptions import PermissionDenied
from django.core.signing import TimestampSigner, SignatureExpired
from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.contrib.auth import login as django_login
from  django.contrib.auth import logout as django_logout
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, FormView
from users.forms import SignUpForm, LoginForm
from users.models import User
from utls.email import send_verify_email


class SignUpView(CreateView):
    form_class = SignUpForm
    template_name = 'registration/signup.html'
    success_url = reverse_lazy('login')

    def form_valid(self,form):
        user = form.save()
        signer = TimestampSigner()
        signed_user_email = signer.sign(user.email)
        dumps_user_email = signing.dumps(signed_user_email)
        url = f"{self.request.scheme}://{self.request.META['HTTP_HOST']}/accounts/verify/?code={dumps_user_email}"
        send_verify_email(url,user.email)
        return render(self.request,'auth/signup_pending.html',{'email':user.email})

def verify_email(request):
    code = request.GET.get('code')
    signer = TimestampSigner()
    try:
        signed_user_email = signing.loads(code)
        email = signer.unsign(signed_user_email,max_age=60 * 30)
    except (signing.BadSignature,TypeError, SignatureExpired):
        return render(request,'auth/signup_fail.html')
    user = get_object_or_404(User,email=email)
    user.is_active=True
    user.save()
    return render(request,'auth/signup_done.html',{'user':user})

class LoginView(FormView):
    form_class = LoginForm
    template_name = 'registration/login.html'
    success_url = reverse_lazy('todo_list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request']=self.request
        return kwargs

    def form_valid(self,form):
        user = form.get_user()
        django_login(self.request,user)
        return redirect(reverse_lazy('todo_list'))

class LogoutView(View):
    def get(self, request):
        django_logout(request)
        return redirect(reverse_lazy('login'))

# def sign_up(request):
#     form = UserCreationForm(request.POST)
#     if form.is_valid():
#         form.save()
#         return redirect(settings.LOGIN_URL)
#     context = {'form': form}
#     return render(request,'registration/signup.html', context)

# def login(request):
#     form = AuthenticationForm(request,data=request.POST)
#     if form.is_valid():
#         django_login(request, form.get_user())
#         return redirect(settings.LOGIN_REDIRECT_URL)
#     context = {'form': form}
#     return render(request,'registration/login.html', context)

# def logout(request):
#     django_logout(request)
#     return redirect(settings.LOGOUT_REDIRECT_URL)