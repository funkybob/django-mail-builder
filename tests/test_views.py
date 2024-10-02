from django.core import mail
from django.test import TestCase


class ViewTestCase(TestCase):
    def test_view(self):
        resp = self.client.get("/")
        self.assertEqual(resp.status_code, 200)

        resp = self.client.post("/", {"name": "test"})
        self.assertEqual(resp.status_code, 302)

        self.assertEqual(len(mail.outbox), 1)
