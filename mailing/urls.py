from django.urls import path
from django.views.decorators.cache import cache_page

from mailing.apps import MailingConfig
from mailing.views import (ChangeMailingActivityView, MailingAttemptListView, MailingCreateView, MailingDeleteView,
                           MailingDetailView, MailingListView, MailingUpdateView, MainViews, MessageCreateView,
                           MessageDeleteView, MessageDetailView, MessageListView, MessageUpdateView,
                           RecipientCreateView, RecipientDeleteView, RecipientDetailView, RecipientListView,
                           RecipientUpdateView)

app_name = MailingConfig.name

urlpatterns = [
    path("", MainViews.as_view(), name="main"),
    path("recipients/", RecipientListView.as_view(), name="recipient_list"),
    path("recipients/create/", RecipientCreateView.as_view(), name="recipient_create"),
    path("recipients/<int:pk>/", cache_page(60)(RecipientDetailView.as_view()), name="recipient_detail"),
    path("recipients/<int:pk>/update/", RecipientUpdateView.as_view(), name="recipient_update"),
    path("recipients/<int:pk>/delete/", RecipientDeleteView.as_view(), name="recipient_delete"),
    path("messages/", MessageListView.as_view(), name="message_list"),
    path("messages/create/", MessageCreateView.as_view(), name="message_create"),
    path("messages/<int:pk>/", cache_page(60)(MessageDetailView.as_view()), name="message_detail"),
    path("messages/<int:pk>/update/", MessageUpdateView.as_view(), name="message_update"),
    path("messages/<int:pk>/delete/", MessageDeleteView.as_view(), name="message_delete"),
    path("mailing/", MailingListView.as_view(), name="mailing_list"),
    path("mailing/create/", MailingCreateView.as_view(), name="mailing_create"),
    path("mailing/<int:pk>/", cache_page(60)(MailingDetailView.as_view()), name="mailing_detail"),
    path("mailing/<int:pk>/update/", MailingUpdateView.as_view(), name="mailing_update"),
    path("mailing/<int:pk>/delete/", MailingDeleteView.as_view(), name="mailing_delete"),
    path("mailing/<int:pk>/change_activity/", ChangeMailingActivityView.as_view(), name="mailing_activity"),
    path("mailing_attempt/", MailingAttemptListView.as_view(), name="mailing_attempt_list"),
]
