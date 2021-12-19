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


class EntryCreationTestCase(TestCase):
    def test_create_entry(self):
        payload = {
            'amount': -42.69,
            'title': 'test entry',
            'comment': 'foo\nbar',
        }

        response = self.client.post('/entries/', data=payload, content_type='application/json')

        self.assertEqual(response.status_code, 200)
        data = response.json()

        created = Entry.objects.get(id=data['id'])
        assert created.amount == Decimal('-42.69')
        assert created.title == 'test entry'
        assert created.comment == 'foo\nbar'

class EntryDeletionTestCase(TestCase):
    def setUp(self) -> None:
        self.entry = EntryFactory.create()

    def test_delete_none_entry(self):
        response = self.client.delete('/entries/foobar2000')

        self.assertEqual(response.status_code, 404)

    def test_delete_one_entry(self):
        response = self.client.delete(f'/entries/{self.entry.id}')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(0, Entry.objects.count())
