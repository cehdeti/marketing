from unittest import TestCase, mock
from eti_marketing.templatetags import marketing as tags

from faker import Faker
fake = Faker()


class GoogleAnalyticsTests(TestCase):

    @mock.patch('eti_marketing.templatetags.marketing.settings')
    def test_returns_a_script_if_the_id_is_set(self, settings):
        ga_id = fake.word()
        settings.GOOGLE_ANALYTICS_ID = ga_id

        result = tags.google_analytics()
        self.assertIn('Google Analytics', result)
        self.assertIn('id=%s' % ga_id, result)
        self.assertIn('gtag(\'config\', \'%s\')' % ga_id, result)

    @mock.patch('eti_marketing.templatetags.marketing.settings')
    def test_returns_nothing_if_not(self, settings):
        settings.GOOGLE_ANALYTICS_ID = None
        self.assertIsNone(tags.google_analytics())


class GoogleTagManagerTests(TestCase):

    @mock.patch('eti_marketing.templatetags.marketing.settings')
    def test_returns_a_script_if_the_id_is_set(self, settings):
        gtm_id = fake.word()
        settings.GOOGLE_TAGMANAGER_ID = gtm_id

        result = tags.google_tagmanager()
        self.assertIn('Google Tag Manager', result)
        self.assertIn('(window,document,\'script\',\'dataLayer\',\'%s\')' % gtm_id, result)

    @mock.patch('eti_marketing.templatetags.marketing.settings')
    def test_returns_nothing_if_not(self, settings):
        settings.GOOGLE_TAGMANAGER_ID = None
        self.assertIsNone(tags.google_tagmanager())


class GoogleTagManagerNoscriptTests(TestCase):

    @mock.patch('eti_marketing.templatetags.marketing.settings')
    def test_returns_a_script_if_the_id_is_set(self, settings):
        gtm_id = fake.word()
        settings.GOOGLE_TAGMANAGER_ID = gtm_id

        result = tags.google_tagmanager_noscript()
        self.assertIn('Google Tag Manager (noscript)', result)
        self.assertIn('<noscript>', result)
        self.assertIn('id=%s' % gtm_id, result)

    @mock.patch('eti_marketing.templatetags.marketing.settings')
    def test_returns_nothing_if_not(self, settings):
        settings.GOOGLE_TAGMANAGER_ID = None
        self.assertIsNone(tags.google_tagmanager_noscript())


class ActiveCampaignEventTrackerTests(TestCase):

    @mock.patch('eti_marketing.templatetags.marketing.settings')
    def test_returns_a_script_if_the_id_is_set(self, settings):
        ac_id = fake.word()
        settings.ACTIVE_CAMPAIGN_EVENT_ACTID = ac_id

        result = tags.active_campaign_event_tracker()
        self.assertIn('//trackcmp.net/visit?actid=%s' % ac_id, result)

    @mock.patch('eti_marketing.templatetags.marketing.settings')
    def test_returns_nothing_if_not(self, settings):
        settings.ACTIVE_CAMPAIGN_EVENT_ACTID = None
        self.assertIsNone(tags.active_campaign_event_tracker())
