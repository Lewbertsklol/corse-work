from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.core.mail import send_mail
from django.http import HttpRequest
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views import generic

import random
from string import ascii_letters, digits

from .forms import ResetPasswordForm, UserCreationForm


class UserListView(generic.ListView):
    model = get_user_model()


def toggle_active(request, pk):
    user = get_user_model().objects.get(pk=pk)
    user.is_active = not user.is_active
    user.save()
    return redirect('users:list')


class RegisterView(generic.CreateView):
    model = get_user_model()
    form_class = UserCreationForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        """ Send email for verification """
        email = form.cleaned_data.get('email')
        encoded_email = urlsafe_base64_encode(bytes(email, 'utf-8'))
        url = reverse('users:email-verification', kwargs={'email': encoded_email})
        full_url = f'{self.request.scheme}://{self.request.get_host()}{url}'
        send_mail(
            'Подтверждение электронной почты',
            f'Для подтверждения адреса электронной почты перейдите по ссылке: {full_url}',
            None,
            recipient_list=[email],
        )
        return super().form_valid(form)


def email_verification(request: HttpRequest, email):
    email = urlsafe_base64_decode(email).decode('utf-8')
    user = get_user_model().objects.get(email=email)
    if not user.is_email_verified:
        user.is_email_verified = True
        user.save()
    return redirect('users:login')


class ResetPasswordView(generic.FormView):
    template_name = 'users/reset-password.html'
    form_class = ResetPasswordForm
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        email = form.cleaned_data.get('email')
        new_password = "".join(random.sample(digits + ascii_letters, 8))
        user = get_user_model().objects.get(email=email)
        user.password = make_password(new_password)
        user.save()
        send_mail(
            'Восстановление пароля',
            f'Ваш пароль был сброшен. Ваш новый пароль {new_password}',
            None,
            recipient_list=[email],
        )
        return super().form_valid(form)
