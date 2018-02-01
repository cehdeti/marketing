from unittest import TestCase, mock

from eti_marketing.utils import PublishedQuerysetMixin, BaseTemplateMixin

from faker import Faker
fake = Faker()


class _PublishedViewParent(object):

    def __init__(self):
        self.__mock_queryset = mock.Mock()
        self.__mock_queryset.filtered = False

        def published(*args, **kwargs):
            self.__mock_queryset.filtered = True
            return self.__mock_queryset

        self.__mock_queryset.published.side_effect = published

    def get_queryset(self):
        return self.__mock_queryset


class _PublishedView(PublishedQuerysetMixin, _PublishedViewParent):

    def __init__(self, is_superuser=False):
        super().__init__()
        self.request = mock.Mock()
        self.request.user = mock.Mock()
        self.request.user.is_superuser = is_superuser


class PublishedQuerysetMixinTests(TestCase):

    def test_limits_the_queryset_to_published_items(self):
        queryset = _PublishedView().get_queryset()
        self.assertTrue(queryset.filtered)

    def test_bypasses_the_limit_for_superadmins(self):
        queryset = _PublishedView(True).get_queryset()
        self.assertFalse(queryset.filtered)


class _BaseTemplateViewParent(object):

    def get_context_data(self, **kwargs):
        return {}


class _BaseTemplateView(BaseTemplateMixin, _BaseTemplateViewParent):
    pass


class BaseTemplateMixinTests(TestCase):

    def setUp(self):
        super().setUp()
        self.__subject = _BaseTemplateView()

    @mock.patch('eti_marketing.utils.settings')
    def test_adds_the_configured_base_template_to_the_context(self, settings):
        template = fake.word()
        settings.ETI_MARKETING_BASE_TEMPLATE = template

        context = self.__subject.get_context_data()

        self.assertEqual(template, context['base_template'])

    def test_defaults_to_something_reasonable(self):
        context = self.__subject.get_context_data()
        self.assertEqual('base.html', context['base_template'])
