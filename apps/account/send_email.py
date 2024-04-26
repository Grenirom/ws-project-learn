from decouple import config
from django.core.mail import send_mail

HOST = config('SEND_EMAIL_HOST')


def send_confirmation_email(user, code):
    print(code, 'code from send mail')
    link = f'http://{HOST}/account/activate/{code}'
    send_mail(
        subject='Здравствуйте! Активируйте ваш аккаунт.',
        message=f'Чтобы активировать аккаунт, вам необходимо перейти по ссылке ниже!'
        f'\n{link}'
        f'\nСсылка действительна 1 раз!',
        from_email='nikitagrebnev402@gmail.com',
        recipient_list=[user],
        fail_silently=False,
    )

