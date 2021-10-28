from uuid import UUID
from django.http.response import JsonResponse
from django.views.decorators.http import require_http_methods

from entries.models import Entry

@require_http_methods(["GET"])
def get_entries(request):
    entries = Entry.objects.filter()
    payload = [entry.to_dict() for entry in entries]
    # Use ``safe`` kwarg to serialize the list through a ``JsonResponse`` object.
    return JsonResponse(payload, safe=False, status=200)

@require_http_methods(["GET"])
def get_entry(request, entry_id: UUID):
    entry = Entry.get_entry_by_id(entry_id)
    if entry is None:
        return JsonResponse({"error": "Entry not found"}, status=404)
    return JsonResponse(entry.to_dict(), status=200)