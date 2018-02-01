from django.conf import settings


def get_base_template():
    """
    Returns the configured base template.
    """
    return getattr(settings, 'ETI_MARKETING_BASE_TEMPLATE', 'base.html')


class PublishedQuerysetMixin(object):
    """
    Mixin for views that need to be limited to "published" items.
    """

    def get_queryset(self):
        queryset = super().get_queryset()

        if not self.request.user.is_superuser:
            queryset = queryset.published()

        return queryset


class BaseTemplateMixin(object):
    """
    Mixin for views that need to include the `base_template` variable.
    """

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['base_template'] = get_base_template()
        return context
