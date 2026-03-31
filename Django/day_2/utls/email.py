from django.core.mail import send_mail
from django.conf import settings

def send_verify_email(message,user_email):
    title = "이메일 인증"
    message = f"해당 링크로 접속을 해주세요 {message}"
    from_email = settings.EMAIL_HOST_USER
    to_email = (user_email,)
    return send_mail(title,message,from_email,to_email)