from unittest import TestCase, mock
from eti_marketing_cms.forms import SignupForm

from faker import Faker
fake = Faker()


class SignupFormTests(TestCase):

    def setUp(self):
        super().setUp()
        self.__data = {
            'first_name': fake.first_name(),
            'last_name': fake.last_name(),
            'organization': fake.company(),
            'title': fake.job(),
            'email': fake.email(),
            'phone': fake.msisdn(),
        }
        self.__subject = SignupForm(data=self.__data)

    def test_validation(self):
        self.assertTrue(self.__subject.is_valid())

    @mock.patch('eti_marketing_cms.forms.active_campaign')
    def test_creates_active_campaign_contact(self, ac):
        api_result = fake.word()
        ac.save_contact.return_value = api_result

        self.__subject.is_valid()
        result = self.__subject.save()

        self.assertEqual(result, api_result)

        attrs = {
            'first_name': self.__data['first_name'],
            'last_name': self.__data['last_name'],
            'orgname': self.__data['organization'],
            'field[%TITLE%,0]': self.__data['title'],
            'email': self.__data['email'],
            'phone': self.__data['phone'],
        }
        ac.save_contact.assert_called_once_with(**attrs)

    @mock.patch('eti_marketing_cms.forms.active_campaign')
    @mock.patch('eti_marketing_cms.forms.settings')
    def test_tracks_a_signup_event_if_one_is_set(self, settings, ac):
        event = fake.word()
        settings.ACTIVE_CAMPAIGN_SIGNUP_EVENT = event
        self.__subject.is_valid()
        self.__subject.save()
        ac.track_event.assert_called_once_with(self.__data['email'], event)
