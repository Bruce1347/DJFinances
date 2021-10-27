import uuid

from django.core.exceptions import ObjectDoesNotExist
from django.db import models


class Entry(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    amount = models.DecimalField(
        null=False,
        max_digits=7,
        decimal_places=2
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
    )
    title = models.CharField(
        max_length=300,
    )
    comment = models.TextField(
        blank=True,
        null=False,
        default="",
    )

    def to_dict(self):
        return {
            "id": str(self.id),
            "title": self.title,
            "comment": self.comment,
            "amount": str(self.amount),
            "created_at": self.created_at.strftime("%s"),
        }

    @classmethod
    def get_entry_by_id(cls, entry_id):
        try:
            entry = cls.objects.get(id=entry_id)
            return entry
        except ObjectDoesNotExist:
            return None
