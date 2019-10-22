from unittest import TestCase, mock
import json
import random
from faker import Faker
from eti_marketing import active_campaign as ac

srandom = random.SystemRandom()
fake = Faker()


def _mock_response(data=None):
    mock_response = mock.Mock()

    if data is None:
        data = {'result_code': 1}

    mock_response.text = json.dumps(data)
    mock_response.json.return_value = data
    return mock_response


class SaveContactTests(TestCase):

    def setUp(self):
        super().setUp()
        self.api_url = fake.word()
        self.api_key = fake.word()
        self.client = ac.Client(self.api_url, self.api_key)

    @mock.patch('eti_marketing.active_campaign.requests')
    def test_calls_api_with_the_payload(self, requests):
        payload = {fake.word(): fake.word()}

        requests.request.return_value = _mock_response()

        ac.ContactSaver(self.client)(**payload)

        requests.request.assert_called_once_with(
            'post',
            '%s/admin/api.php' % self.api_url,
            params={'api_key': self.api_key, 'api_output': 'json', 'api_action': 'contact_add'},
            data=payload
        )

    @mock.patch('eti_marketing.active_campaign.requests')
    def test_adds_list_subscriptions(self, requests):
        requests.request.return_value = _mock_response()
        ac.ContactSaver(self.client, ['hello'])()
        __, kwargs = requests.request.call_args
        self.assertEqual(kwargs['data']['p[hello]'], 'hello')
        self.assertEqual(kwargs['data']['status[hello]'], 1)

    @mock.patch('eti_marketing.active_campaign.requests')
    def test_returns_the_unserialized_response(self, requests):
        payload = {fake.word(): fake.word()}
        response = {'hello': 'im_here', 'result_code': 1}

        requests.request.return_value = _mock_response(response)

        result = ac.ContactSaver(self.client)(**payload)
        self.assertEqual(result['hello'], 'im_here')

    @mock.patch('eti_marketing.active_campaign.requests')
    def test_updates_the_contact_if_it_already_exists(self, requests):
        payload = {'first_name': 'New'}
        existing_subscriber_id = srandom.randint(0, 10)

        requests.request.side_effect = [
            _mock_response({
                'result_code': 0,
                '0': {'subscriberid': existing_subscriber_id, 'first_name': 'Test', 'last_name': 'Person'}
            }),
            _mock_response({'updated': True}),
        ]

        result = ac.ContactSaver(self.client)(**payload)

        self.assertTrue(result['updated'])

        self.assertEqual(requests.request.call_count, 2)
        __, kwargs = requests.request.call_args
        self.assertEqual(kwargs['params']['api_action'], 'contact_edit')
        self.assertEqual(kwargs['data']['id'], existing_subscriber_id)
        self.assertEqual(kwargs['data']['first_name'], 'New')

    @mock.patch('eti_marketing.active_campaign.requests')
    def test_returns_if_url_and_key_are_not_set(self, requests):
        self.assertIsNone(ac.save_contact())
        requests.assert_not_called()


class TrackEventTests(TestCase):

    @mock.patch('eti_marketing.active_campaign.requests')
    def test_returns_if_url_and_key_are_not_set(self, requests):
        self.assertIsNone(ac.track_event(fake.email(), fake.word()))
        requests.assert_not_called()

    @mock.patch('eti_marketing.active_campaign.requests')
    def test_calls_api_with_the_payload(self, requests):
        actid = fake.word()
        key = fake.word()
        email = fake.email()
        event = fake.word()
        event_data = fake.word()

        requests.post.return_value = _mock_response()

        ac.EventTracker(actid, key)(email, event, event_data)

        self.assertEqual(json.loads(requests.post.call_args[1]['data']), [{
            'event': event,
            'event_data': event_data,
            'visit': {'email': email},
            'actid': actid,
            'key': key,
        }])

    @mock.patch('eti_marketing.active_campaign.requests')
    def test_returns_the_unserialized_response(self, requests):
        requests.post.return_value = _mock_response({'hello': 'hi'})
        result = ac.EventTracker(fake.word(), fake.word())(fake.email(), fake.word())
        self.assertEqual(result['hello'], 'hi')
