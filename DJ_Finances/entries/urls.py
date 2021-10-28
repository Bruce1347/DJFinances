from django.urls import path
from entries.views import get_entry, get_entries

urlpatterns = [
    path('', get_entries),
    path('<uuid:entry_id>', get_entry),
]