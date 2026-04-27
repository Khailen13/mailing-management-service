from datetime import datetime

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, DeleteView, DetailView, ListView, TemplateView, UpdateView

from config.settings import EMAIL_HOST_USER
from mailing.forms import MailingForm, MessageForm, RecipientForm
from mailing.models import Mailing, MailingAttempt, Message, Recipient
from mailing.services import get_data_from_cache


# Главная страница
class MainViews(TemplateView):
    template_name = "mailing/main.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["mailing_attempts_count"] = MailingAttempt.objects.all().count
        context["mailing_launched_count"] = Mailing.objects.filter(status="launched").count
        context["recipients_count"] = Recipient.objects.all().count
        return context


# CRUD для Получателей рассылки
class RecipientListView(LoginRequiredMixin, ListView):
    model = Recipient
    template_name = "mailing/object_list.html"

    def get_queryset(self):
        user = self.request.user
        return get_data_from_cache(self.model, user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["view_name"] = "Получатели рассылки"
        context["add_button_url"] = "mailing:recipient_create"
        context["obj_for_list"] = "mailing/recipient_for_list.html"
        context["obj_update_url"] = "mailing:recipient_update"
        context["obj_delete_url"] = "mailing:recipient_delete"
        return context


class RecipientDetailView(LoginRequiredMixin, DetailView):
    model = Recipient
    template_name = "mailing/object_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["view_name"] = "Детали получателя рассылки"
        context["obj_for_detail"] = "mailing/recipient_for_detail.html"
        context["obj_list_url"] = "mailing:recipient_list"
        context["obj_update_url"] = "mailing:recipient_update"
        context["obj_delete_url"] = "mailing:recipient_delete"
        return context


class RecipientCreateView(LoginRequiredMixin, CreateView):
    model = Recipient
    form_class = RecipientForm
    template_name = "mailing/object_form.html"
    success_url = reverse_lazy("mailing:recipient_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["view_name"] = "Добавление получателя рассылки"
        context["obj_list_url"] = "mailing:recipient_list"
        return context

    def form_valid(self, form):
        recipient = form.save()
        user = self.request.user
        recipient.owner = user
        recipient.save()
        return super().form_valid(form)


class RecipientUpdateView(LoginRequiredMixin, UpdateView):
    model = Recipient
    form_class = RecipientForm
    template_name = "mailing/object_form.html"
    success_url = reverse_lazy("mailing:recipient_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["view_name"] = "Изменение данных получателя рассылки"
        context["obj_list_url"] = "mailing:recipient_list"
        return context


class RecipientDeleteView(LoginRequiredMixin, DeleteView):
    model = Recipient
    template_name = "mailing/object_confirm_delete.html"
    success_url = reverse_lazy("mailing:recipient_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        recipient_id = self.kwargs.get("pk")
        recipient_subject = Recipient.objects.get(id=recipient_id).full_name
        context["view_name"] = "Удаление получателя рассылки"
        context["obj_prefix"] = "получателя рассылки"
        context["obj_name"] = recipient_subject
        context["obj_list_url"] = "mailing:recipient_list"

        return context


# CRUD для Сообщений
class MessageListView(LoginRequiredMixin, ListView):
    model = Message
    template_name = "mailing/object_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["view_name"] = "Сообщения"
        context["obj_for_list"] = "mailing/message_for_list.html"
        context["add_button_url"] = "mailing:message_create"
        context["obj_update_url"] = "mailing:message_update"
        context["obj_delete_url"] = "mailing:message_delete"
        return context

    def get_queryset(self):
        user = self.request.user
        return get_data_from_cache(self.model, user)


class MessageDetailView(LoginRequiredMixin, DetailView):
    model = Message
    template_name = "mailing/object_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["obj_for_detail"] = "mailing/message_for_detail.html"
        context["view_name"] = "Детали сообщения"
        context["obj_list_url"] = "mailing:message_list"
        context["obj_update_url"] = "mailing:message_update"
        context["obj_delete_url"] = "mailing:message_delete"
        return context


class MessageCreateView(LoginRequiredMixin, CreateView):
    model = Message
    form_class = MessageForm
    template_name = "mailing/object_form.html"
    success_url = reverse_lazy("mailing:message_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["view_name"] = "Добавление сообщения"
        context["obj_list_url"] = "mailing:message_list"
        return context

    def form_valid(self, form):
        message = form.save()
        user = self.request.user
        message.owner = user
        message.save()
        return super().form_valid(form)


class MessageUpdateView(LoginRequiredMixin, UpdateView):
    model = Message
    form_class = MessageForm
    template_name = "mailing/object_form.html"
    success_url = reverse_lazy("mailing:message_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["view_name"] = "Изменение сообщения"
        context["obj_list_url"] = "mailing:message_list"
        return context


class MessageDeleteView(LoginRequiredMixin, DeleteView):
    model = Message
    template_name = "mailing/object_confirm_delete.html"
    success_url = reverse_lazy("mailing:message_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        message_id = self.kwargs.get("pk")
        message_subject = Message.objects.get(id=message_id).subject
        context["view_name"] = "Удаление сообщения"
        context["obj_prefix"] = "сообщение"
        context["obj_name"] = message_subject
        context["obj_list_url"] = "mailing:message_list"

        return context


# CRUD для Рассылок
class MailingListView(LoginRequiredMixin, ListView):
    model = Mailing
    template_name = "mailing/object_list.html"

    def get_queryset(self):
        user = self.request.user
        return get_data_from_cache(self.model, user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["view_name"] = "Рассылки"
        context["obj_for_list"] = "mailing/mailing_for_list.html"
        context["add_button_url"] = "mailing:mailing_create"
        context["obj_update_url"] = "mailing:mailing_update"
        context["obj_delete_url"] = "mailing:mailing_delete"
        return context

    def post(self, request, *args, **kwargs):
        mailing_id = request.POST.get("run mailing")
        self.mailing(mailing_id)
        return redirect("mailing:mailing_list")

    def mailing(self, mailing_id):
        mailing = Mailing.objects.get(id=mailing_id)
        message_subject = mailing.message.subject
        message_body = mailing.message.body
        recipient_obj_list = mailing.recipients.all()

        mailing.start_datetime = datetime.now()
        mailing.status = "launched"
        mailing.save()

        for recipient in recipient_obj_list:
            try:
                send_mail(
                    subject=message_subject,
                    message=message_body,
                    from_email=EMAIL_HOST_USER,
                    recipient_list=[
                        recipient.email,
                    ],
                )
                status = "successfully"
                server_response = None
            except Exception as error:
                status = "unsuccessfully"
                server_response = str(error)
            finally:
                MailingAttempt.objects.create(
                    status=status,
                    server_response=server_response,
                    mailing=mailing,
                    recipient=recipient,
                )
        mailing.end_datetime = datetime.now()
        mailing.status = "completed"
        mailing.save()


class MailingDetailView(LoginRequiredMixin, DetailView):
    model = Mailing
    template_name = "mailing/object_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        mailing_id = self.kwargs.get("pk")
        mailing_recipients = Mailing.objects.get(id=mailing_id).recipients.all()
        context["obj_for_detail"] = "mailing/mailing_for_detail.html"
        context["view_name"] = "Детали рассылки"
        context["obj_list_url"] = "mailing:mailing_list"
        context["obj_update_url"] = "mailing:mailing_update"
        context["obj_delete_url"] = "mailing:mailing_delete"
        context["recipients"] = ", ".join([str(recipient) for recipient in mailing_recipients])
        return context


class MailingCreateView(LoginRequiredMixin, CreateView):
    model = Mailing
    form_class = MailingForm
    template_name = "mailing/object_form.html"
    success_url = reverse_lazy("mailing:mailing_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["view_name"] = "Добавление рассылки"
        context["obj_list_url"] = "mailing:mailing_list"
        return context

    def form_valid(self, form):
        mailing = form.save()
        user = self.request.user
        mailing.owner = user
        mailing.save()
        return super().form_valid(form)


class MailingUpdateView(LoginRequiredMixin, UpdateView):
    model = Mailing
    form_class = MailingForm
    template_name = "mailing/object_form.html"
    success_url = reverse_lazy("mailing:mailing_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["view_name"] = "Изменение рассылки"
        context["obj_list_url"] = "mailing:mailing_list"
        return context


class MailingDeleteView(LoginRequiredMixin, DeleteView):
    model = Mailing
    template_name = "mailing/object_confirm_delete.html"
    success_url = reverse_lazy("mailing:mailing_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        mailing_id = self.kwargs.get("pk")
        context["view_name"] = "Удаление рассылки"
        context["obj_prefix"] = "рассылку"
        context["obj_name"] = mailing_id
        context["obj_list_url"] = "mailing:mailing_list"

        return context


# Список Попыток рассылок
class MailingAttemptListView(LoginRequiredMixin, ListView):
    model = MailingAttempt
    template_name = "mailing/object_list.html"

    def get_queryset(self):
        user = self.request.user
        return get_data_from_cache(self.model, user)

    def get_context_data(self, **kwargs):
        mailing_attempt_list = self.get_queryset()
        successful_mailing_attempt_list = [
            object for object in mailing_attempt_list if object.status == "successfully"
        ]
        total_attempts_count = len(mailing_attempt_list)
        successful_attempts_count = len(successful_mailing_attempt_list)
        context = super().get_context_data(**kwargs)
        context["view_name"] = (
            f"Попытки рассылок | Успешно отправлены: {successful_attempts_count}/{total_attempts_count}"
        )
        context["obj_for_list"] = "mailing/mailing_attempt_for_list.html"

        return context


#  Переключение статуса рассылок
class ChangeMailingActivityView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        mailing_id = kwargs.get("pk")
        mailing = get_object_or_404(Mailing, id=mailing_id)
        if not request.user.has_perm("mailing.change_mailing_activity"):
            raise PermissionDenied
        mailing.is_active = not mailing.is_active
        mailing.save()
        return redirect("mailing:mailing_list")
