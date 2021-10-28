import factory
from decimal import Decimal
from entries.models import Entry

class EntryFactory(factory.django.DjangoModelFactory):
    amount = factory.Faker(
        'pydecimal',
        min_value=Decimal("-10000"),
        max_value=Decimal("10000"),
    )
    class Meta:
        model = Entry

    