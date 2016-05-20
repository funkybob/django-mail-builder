
from django.test import TestCase


from mail_builder import build_message


class BuilderTestCase(TestCase):

    def test_empty(self):
        msg = build_message('empty.email')
        self.assertEqual(msg.to, [])

    def test_defaults(self):
        msg = build_message('empty.email', from_email='test@test.com')
        self.assertEqual(msg.to, [])
        self.assertEqual(msg.from_email, 'test@test.com')

    def test_subject(self):
        msg = build_message('subject.email')
        self.assertEqual(msg.subject, 'Test Subject')

    def test_to(self):
        msg = build_message('to.email')
        self.assertEqual(msg.to, ['test@test.com'])

    def test_html(self):
        msg = build_message('html.email')
        alts = [alt for alt, mtype in msg.alternatives if mtype == 'text/html']
        self.assertEqual(len(alts), 1)
        self.assertHTMLEqual(alts[0], '<h1> Welcome! </h1>')

    def test_handle_template_exception(self):
        msg = build_message('exception.email')
