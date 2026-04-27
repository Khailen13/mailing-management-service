from datetime import datetime

from django.core.mail import send_mail
from django.core.management import BaseCommand
from termcolor import colored

from config.settings import EMAIL_HOST_USER
from mailing.models import Mailing, MailingAttempt


class Command(BaseCommand):
    """
    Команда отправляет рассылки из базы данных.
    Для отправки всех рассылок из базы данных команда вводится без аргументов: 'python manage.py mailing'.
    Для отправки конкретных рассылок следует указать id рассылок ч/з пробел: 'python manage.py mailing id1 id2 ...'.
    """

    help = '"mailing id1 id2 ..." / "mailing" - отправляет рассылки из БД по их id или все рассылки (без аргумента)'
    successful_sending_count = 0
    unsuccessful_sending_count = 0

    def handle(self, *args, **options):
        if not args:
            print(colored("Попытка отправки всех рассылок", "yellow"))
            mailing_id_list = [mailing_object.id for mailing_object in Mailing.objects.all()]
        else:
            print(colored(f"Попытка отправки рассылок c id={args}", "yellow"))
            mailing_id_list = list()
            for arg in args:
                try:
                    Mailing.objects.get(id=arg)
                    mailing_id_list.append(arg)
                except Exception:
                    print(colored(f"Рассылка с id={arg} не найдена в базе данных", "red"))

        for mailing_id in mailing_id_list:
            self.custom_send_mail(mailing_id)
        print(colored("Рассылка завершена", "yellow"))
        print(
            colored(
                f"Всего попыток отправки: {self.successful_sending_count + self.unsuccessful_sending_count}", "yellow"
            )
        )
        print(
            colored(
                f"Успешных:{self.successful_sending_count} | Неуспешных:{self.unsuccessful_sending_count} ", "yellow"
            )
        )

    def add_arguments(self, parser):
        parser.add_argument(nargs="*", type=int, dest="args", help="Список")

    def custom_send_mail(self, mailing_id):
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
                print(
                    colored(
                        f"Письмо (id={mailing.message.id}) расcылки (id={mailing_id}) отправлено успешно.", "green"
                    )
                )
                self.successful_sending_count += 1
            except Exception as error:
                status = "unsuccessfully"
                server_response = str(error)
                print(
                    colored(
                        f"Возникла ошибка при отправке письма (id={mailing.message.id}) расcылки (id={mailing_id})",
                        "red",
                    )
                )
                print(colored(f"Ответ сервера: {error}", "red"))
                self.unsuccessful_sending_count += 1

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
