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
import json
import copy
import logging
from django.conf import settings


logger = logging.getLogger(__name__)


class ContactSaver(object):
    """
    Saves a contact record to ActiveCampaign.

    This is a separate class mostly for unit-testing purposes. You should
    probably use the `save_contact` function that is pre-configured with config
    from Django's settings instead.
    """

    def __init__(self, api_url, api_key, list_subscriptions=[]):
        self.__api_url = api_url
        self.__api_key = api_key
        self.__set_api_urls()
        self.__list_subscriptions = list_subscriptions

    def __call__(self, **data):
        payload = copy.deepcopy(data)

        for sub in self.__list_subscriptions:
            payload['status[%s]' % sub] = 1  # This sets their subscription status for list to active.
            payload['p[%s]' % sub] = sub  # This subscribes them to the list.

        if not self.__add_contact_url:
            logger.info("""
                Received ActiveCampaign submission, but API URL and/or key are not
                set up. Here is the data:
                Payload: %s
                """ % payload)
            return

        result = requests.post(self.__add_contact_url, data=payload)
        result_data = json.loads(result.text)

        if result_data['result_code'] != 1 and \
                'does not allow duplicates' in result_data['result_message']:
            # Update contact instead
            existing_contact = result_data['0']
            contact_id = existing_contact['subscriberid']

            payload = copy.deepcopy(payload)
            payload['id'] = contact_id

            result = requests.post(self.__edit_contact_url, data=payload)
            result_data = json.loads(result.text)

        return result_data

    def __set_api_urls(self):
        if self.__api_url and self.__api_key:
            params = (self.__api_url, self.__api_key)
            self.__add_contact_url = '%s/admin/api.php?api_key=%s&api_output=json&api_action=contact_add' % params
            self.__edit_contact_url = '%s/admin/api.php?api_key=%s&api_output=json&api_action=contact_edit&overwrite=0' % params
        else:
            self.__add_contact_url = None
            self.__edit_contact_url = None


save_contact = ContactSaver(
    getattr(settings, 'ACTIVE_CAMPAIGN_API_URL', None),
    getattr(settings, 'ACTIVE_CAMPAIGN_API_KEY', None),
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
