from datetime import datetime
from decimal import Decimal

from django.test import TestCase
from entries.factories import EntryFactory
from entries.models import Entry
from status_codes import StatusCode


class EntriesRetrievalTestCase(TestCase):
    def setUp(self):
        self.entry_1: Entry = EntryFactory.create(
            created_at=datetime(2021, 10, 29, 13, 37, 42)
        )
        self.entry_2: Entry = EntryFactory.create(
            created_at=datetime(2021, 10, 29, 14, 42, 42)
        )
        self.entry_3: Entry = EntryFactory.create(
            created_at=datetime(2020, 10, 29, 13, 37, 42)
        )

    def test_retrieve_one_entry(self):
        url = f"/entries/{str(self.entry_1.id)}"
        response = self.client.get(url)

        assert response.status_code == StatusCode.OK.value
        recieved = response.json()
        self.assertAlmostEqual(
            Decimal(recieved['amount']), Decimal(self.entry_1.amount)
        )
        self.assertEqual(
            {
                'comment': recieved['comment'],
                'title': recieved['title'],
            },
            {
                'comment': '',
                'title': '',
            }
        )

    def test_retrieve_all_entries(self):
        response = self.client.get("/entries/")

        assert response.status_code == StatusCode.OK.value
        recieved = response.json()
        self.assertEqual(
            [str(entry.get('id')) for entry in recieved],
            [
                str(self.entry_1.id),
                str(self.entry_2.id),
                str(self.entry_3.id),
            ],
        )
