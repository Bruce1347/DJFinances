import uuid

from django.core.exceptions import ObjectDoesNotExist
from django.db import models

from marshmallow import Schema, fields, validate


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

    class Meta:
        # Ensure that entries are always sorted chronologically in querysets.
        ordering = ['created_at']

    def to_dict(self):
        return {
            "id": str(self.id),
            "title": self.title,
            "comment": self.comment,
            "amount": float(self.amount),
            "created_at": self.created_at.strftime("%s"),
        }

    @classmethod
    def get_entry_by_id(cls, entry_id):
        try:
            entry = cls.objects.get(id=entry_id)
            return entry
        except ObjectDoesNotExist:
            return None

class EntrySchema(Schema):
    amount = fields.Decimal(
        2,
        validate=validate.Range(min=-10_000, max=10_000)
    )
    title = fields.Str(validate=validate.Length(max=300))
    comment = fields.Str()
    id = fields.UUID(read_only=True)
    created_at = fields.DateTime(read_only=True)
