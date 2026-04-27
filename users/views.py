import secrets

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, UpdateView

from config.settings import EMAIL_HOST_USER
from mailing.models import Mailing, Recipient

from .forms import UserRegisterForm, UserUpdateForm
from .models import User


class UserListView(LoginRequiredMixin, ListView):
    model = User

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        users = User.objects.all()
        users_recipients_count = dict()
        users_mailing_count = dict()
        users_running_mailing_count = dict()
        for user in users:
            users_recipients_count[user.pk] = Recipient.objects.filter(owner=user).count()
            users_mailing_count[user.pk] = Mailing.objects.filter(owner=user).count()
            users_running_mailing_count[user.pk] = Mailing.objects.filter(owner=user, status="launched").count()

        context["recipients_count"] = users_recipients_count
        context["mailing_count"] = users_mailing_count
        context["running_mailing_count"] = users_running_mailing_count
        return context


class UserCreateView(CreateView):
    model = User
    form_class = UserRegisterForm
    success_url = reverse_lazy("users:login")

    def form_valid(self, form):
        user = form.save()
        user.is_active = False
        token = secrets.token_hex(16)
        user.token = token
        user.save()
        host = self.request.get_host()
        url = f"http://{host}/users/email_confirm/{token}/"
        send_mail(
            subject="Подтверждение почты",
            message=f"Для подтверждения почты перейдите по ссылке: {url}",
            from_email=EMAIL_HOST_USER,
            recipient_list=[
                user.email,
            ],
        )
        return super().form_valid(form)


def email_verification(request, token):
    user = get_object_or_404(User, token=token)
    user.is_active = True
    user.save()
    return redirect(reverse("users:login"))


class UserDetailView(LoginRequiredMixin, DetailView):
    model = User


class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserUpdateForm
    success_url = reverse_lazy("mailing:main")


class ChangeUserActivityView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        user_id = kwargs.get("pk")
        user = get_object_or_404(User, id=user_id)
        if not request.user.has_perm("users.change_user_activity"):
            raise PermissionDenied
        user.is_active = not user.is_active
        user.save()
        return redirect("users:user_list")
