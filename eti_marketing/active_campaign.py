"""
Allows for saving contacts and tracking events to ActiveCampaign.

Configuration options:

    * `ACTIVE_CAMPAIGN_API_URL`: The URL your AC instance resides at.
    * `ACTIVE_CAMPAIGN_API_KEY`: API key
    * `ACTIVE_CAMPAIGN_LIST_SUBSCRIPTIONS`: Additional lists you'd like to
        subscribe all new contacts to.

    * `ACTIVE_CAMPAIGN_EVENT_ACTID`: ActID for the events API
    * `ACTIVE_CAMPAIGN_EVENT_KEY`: Key for the events API
"""

import requests
import copy
import logging
from django.conf import settings

import json
if hasattr(json, 'JSONDecodeError'):
    JSONError = json.JSONDecodeError
else:
    JSONError = ValueError

logger = logging.getLogger(__name__)


class Client(object):
    """
    General use API client for ActiveCampaign API.
    """

    def __init__(self, url, key):
        self._url = url
        self._key = key

    @property
    def is_live(self):
        """
        Whether or not this API client has valid credentials and is configured
        to make actual API calls. This allows the client to be used seamlessly
        in local environments where we don't want to call the API.
        """
        return bool(self._url) and bool(self._key)

    ###########
    # Begin API
    ###########

    ##########
    # Contacts
    ##########

    def get_contact_by_email(self, email):
        try:
            result = self._do_json('contact_view_email', params={'email': email})
        except JSONError:
            return None

        return result if result.get('result_code') == 1 else None

    def add_contact(self, **data):
        return self._do_json('contact_add', 'post', data=data)

    def edit_contact(self, **data):
        return self._do_json('contact_edit', 'post', data=data, params={'overwrite': '0'})

    #########
    # End API
    #########

    def _do_json(self, *args, **kwargs):
        response = self._do_request(*args, **kwargs)

        try:
            return response.json()
        except Exception as e:
            logger.error("""
                error calling api:
                URL: %s
                result: %s
                result status %s
                could not decode result json: %s
            """ % (response.url, response.text, response.status_code, e))

    def _do_request(self, action, method='get', **kwargs):
        params = kwargs.pop('params', {})
        params['api_action'] = action
        params = self._params(**params)
        return requests.request(method, '%s/admin/api.php' % self._url, params=params, **kwargs)

    def _params(self, **params):
        params.setdefault('api_key', self._key)
        params.setdefault('api_output', 'json')
        return params


client = Client(
    getattr(settings, 'ACTIVE_CAMPAIGN_API_URL', None),
    getattr(settings, 'ACTIVE_CAMPAIGN_API_KEY', None),
)


class ContactSaver(object):
    """
    Saves a contact record to ActiveCampaign.

    This is a separate class mostly for unit-testing purposes. You should
    probably use the `save_contact` function that is pre-configured with config
    from Django's settings instead.
    """

    def __init__(self, client, list_subscriptions=[]):
        self._client = client
        self._list_subscriptions = list_subscriptions

    def __call__(self, **data):
        payload = copy.deepcopy(data)

        for sub in self._list_subscriptions:
            payload['status[%s]' % sub] = 1  # This sets their subscription status for list to active.
            payload['p[%s]' % sub] = sub  # This subscribes them to the list.

        if not self._client.is_live:
            logger.info("""
                Received ActiveCampaign submission, but API URL and/or key are not
                set up. Here is the data:
                Payload: %s
                """ % payload)
            return

        result_data = self._client.add_contact(**payload)

        if result_data['result_code'] != 1 and \
                '0' in result_data and \
                'subscriberid' in result_data['0']:
            # Update contact instead
            payload = copy.deepcopy(payload)
            payload['id'] = result_data['0']['subscriberid']

            result_data = self._client.edit_contact(**payload)

        return result_data


save_contact = ContactSaver(
    client,
    getattr(settings, 'ACTIVE_CAMPAIGN_LIST_SUBSCRIPTIONS', []),
)


class EventTracker(object):
    """
    Tracks an event in the ActiveCampaign API.

    This is a separate class mostly for unit-testing purposes. You should
    probably use the `track_event` function that is pre-configured with config
    from Django's settings instead.
    """

    def __init__(self, event_actid, event_key):
        self.__event_actid = event_actid
        self.__event_key = event_key

    def __call__(self, email, event_name, event_data=None):
        payload = {
            'event': event_name,
            'event_data': event_data,
            'visit': {'email': email}
        }

        if not self.__event_actid or not self.__event_key:
            logger.info("""
                Received ActiveCampaign event, but credentials are not set up.
                Here is the data:
                Data: %s
                """ % payload)
            return
        else:
            payload.update(actid=self.__event_actid, key=self.__event_key)

        result = requests.post('https://trackcmp.net/event', data=json.dumps([payload]))
        return json.loads(result.text)


track_event = EventTracker(
    getattr(settings, 'ACTIVE_CAMPAIGN_EVENT_ACTID', None),
    getattr(settings, 'ACTIVE_CAMPAIGN_EVENT_KEY', None),
)
