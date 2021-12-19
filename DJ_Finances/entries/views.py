from uuid import UUID
from django.http.response import JsonResponse
from django.views.decorators.http import require_http_methods

from entries.models import Entry, EntrySchema

import json

@require_http_methods(["GET"])
def get_entries(request):
    entries = Entry.objects.filter()
    payload = [entry.to_dict() for entry in entries]
    # Use ``safe`` kwarg to serialize the list through a ``JsonResponse`` object.
    return JsonResponse(payload, safe=False, status=200)

@require_http_methods(["POST"])
def create_entry(request):
    data = json.loads(request.body.decode("utf-8"))
    schema = EntrySchema()
    entry = Entry.objects.create(**schema.load(data))

    d = entry.to_dict()
    return JsonResponse(d, status=200)

@require_http_methods(["GET"])
def get_entry(request, entry_id: UUID):
    entry = Entry.get_entry_by_id(entry_id)
    if entry is None:
        return JsonResponse({"error": "Entry not found"}, status=404)
    return JsonResponse(entry.to_dict(), status=200)

@require_http_methods(["DELETE"])
def delete_entry(request, entry_id: UUID):
    entry = Entry.get_entry_by_id(entry_id)
    if entry is None:
        return JsonResponse({"error": "Entry not found"}, status=404)
    entry.delete()
    return JsonResponse({}, status=200)

def entry_request_dispatcher(request, entry_id: UUID):
    if request.method == "GET":
        return get_entry(request, entry_id)
    elif request.method == "DELETE":
        return delete_entry(request, entry_id)

def entries_request_dispatcher(request):
    if request.method == "POST":
        return create_entry(request)
    elif request.method == "GET":
        return get_entries(request)
