from django import forms

from .models import Mailing, Message, Recipient


class RecipientForm(forms.ModelForm):
    class Meta:
        model = Recipient
        fields = ("full_name", "email", "comment")

    def __init__(self, *args, **kwargs):
        super(RecipientForm, self).__init__(*args, **kwargs)
        fields_placeholders = {
            "full_name": "Введите Ф.И.О.",
            "email": "Введите адрес эл. почты",
            "comment": "Можете добавить комментарий",
        }
        for field, placeholder in fields_placeholders.items():
            self.fields[field].widget.attrs.update({"class": "form-control", "placeholder": placeholder})


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = (
            "subject",
            "body",
        )

    def __init__(self, *args, **kwargs):
        super(MessageForm, self).__init__(*args, **kwargs)
        fields_placeholders = {
            "subject": "Укажите тему письма",
            "body": "Введите текст письма",
        }
        for field, placeholder in fields_placeholders.items():
            self.fields[field].widget.attrs.update({"class": "form-control", "placeholder": placeholder})


class MailingForm(forms.ModelForm):
    class Meta:
        model = Mailing
        fields = (
            "message",
            "recipients",
        )

    def __init__(self, *args, **kwargs):
        super(MailingForm, self).__init__(*args, **kwargs)

        for field in self.Meta.fields:
            self.fields[field].widget.attrs.update({"class": "form-control"})
