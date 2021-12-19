from django.urls import path
from entries.views import entry_request_dispatcher, entries_request_dispatcher

urlpatterns = [
    path('', entries_request_dispatcher),
    path('<uuid:entry_id>', entry_request_dispatcher),
]