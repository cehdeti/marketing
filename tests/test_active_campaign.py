from unittest import TestCase, mock
import json
import random
from eti_marketing import active_campaign as ac

from faker import Faker
fake = Faker()


def _mock_response(data=None):
    mock_response = mock.Mock()

    if data is None:
        data = {'result_code': 1}

    mock_response.text = json.dumps(data)
    return mock_response


class SaveContactTests(TestCase):

    @mock.patch('eti_marketing.active_campaign.requests')
    def test_calls_api_with_the_payload(self, requests):
        api_url = fake.word()
        api_key = fake.word()
        payload = {fake.word(): fake.word()}

        requests.post.return_value = _mock_response()

        ac.ContactSaver(api_url, api_key)(**payload)

        requests.post.assert_called_once_with(
            '%s/admin/api.php?api_key=%s&api_output=json&api_action=contact_add' % (
                api_url, api_key
            ),
            data=payload
        )

    @mock.patch('eti_marketing.active_campaign.requests')
    def test_adds_list_subscriptions(self, requests):
        requests.post.return_value = _mock_response()
        ac.ContactSaver(fake.word(), fake.word(), ['hello'])()
        args, kwargs = requests.post.call_args
        self.assertEqual(kwargs['data']['p[hello]'], 'hello')
        self.assertEqual(kwargs['data']['status[hello]'], 1)

    @mock.patch('eti_marketing.active_campaign.requests')
    def test_returns_the_unserialized_response(self, requests):
        api_url = fake.word()
        api_key = fake.word()
        payload = {fake.word(): fake.word()}
        response = {'hello': 'im_here', 'result_code': 1}

        requests.post.return_value = _mock_response(response)

        result = ac.ContactSaver(api_url, api_key)(**payload)
        self.assertEqual(result['hello'], 'im_here')

    @mock.patch('eti_marketing.active_campaign.requests')
    def test_updates_the_contact_if_it_already_exists(self, requests):
        api_url = fake.word()
        api_key = fake.word()
        payload = {'first_name': 'New'}
        existing_subscriber_id = random.randint(0, 10)

        requests.post.side_effect = [
            _mock_response({
                'result_message': 'does not allow duplicates',
                'result_code': 0,
                '0': {'subscriberid': existing_subscriber_id, 'first_name': 'Test', 'last_name': 'Person'}
            }),
            _mock_response({'updated': True}),
        ]

        result = ac.ContactSaver(api_url, api_key)(**payload)

        self.assertTrue(result['updated'])

        self.assertEqual(requests.post.call_count, 2)
        args, kwargs = requests.post.call_args
        self.assertEqual(
            args[0],
            '%s/admin/api.php?api_key=%s&api_output=json&api_action=contact_edit&overwrite=0' % (api_url, api_key)
        )
        self.assertEqual(kwargs['data']['id'], existing_subscriber_id)
        self.assertEqual(kwargs['data']['first_name'], 'New')

    @mock.patch('builtins.print')
    @mock.patch('eti_marketing.active_campaign.requests')
    def test_prints_and_returns_if_url_and_key_are_not_set(self, requests, mock_print):
        self.assertIsNone(ac.save_contact())
        mock_print.assert_called_once()
        requests.assert_not_called()


class TrackEventTests(TestCase):

    @mock.patch('builtins.print')
    @mock.patch('eti_marketing.active_campaign.requests')
    def test_prints_and_returns_if_url_and_key_are_not_set(self, requests, mock_print):
        self.assertIsNone(ac.track_event(fake.email(), fake.word()))
        mock_print.assert_called_once()
        requests.assert_not_called()

    @mock.patch('eti_marketing.active_campaign.requests')
    def test_calls_api_with_the_payload(self, requests):
        url = fake.word()
        actid = fake.word()
        key = fake.word()
        email = fake.email()
        event = fake.word()
        event_data = fake.word()

        requests.post.return_value = _mock_response()

        ac.EventTracker(url, actid, key)(email, event, event_data)

        requests.post.assert_called_once_with(
            url, data=json.dumps([{
                'event': event,
                'event_data': event_data,
                'visit': {'email': email},
                'actid': actid,
                'key': key,
            }])
        )

    @mock.patch('eti_marketing.active_campaign.requests')
    def test_returns_the_unserialized_response(self, requests):
        requests.post.return_value = _mock_response({'hello': 'hi'})
        result = ac.EventTracker(fake.word(), fake.word(), fake.word())(fake.email(), fake.word())
        self.assertEqual(result['hello'], 'hi')
