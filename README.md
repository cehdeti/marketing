ETI Marketing CMS
===============================

This is Django app that provides miscellaneous marketing functionality for ETI
apps.

Currently, it does the following:

* Provides a `LandingPage` model so the Marketing staff can easily add new marketing landing pages based on project's styleguide, and without coding.
* Provides a simple, extensible signup form that talks to Active Campaign.
* Centralizes communications with the Active Campaign API

Installation
------------

* Make sure you have `virtualenv` activated

```bash
  pip install git+https://github.com/cehdeti/eti-django-marketing-cms.git
```

If using `pipenv`

```
  pipenv install git+https://github.com/cehdeti/eti-django-marketing-cms.git#egg=django-eti-marketing-cms
```

Setting up the Package
----------------------

1. Add the following to `settings.py`:

```python
  INSTALLED_APPS = [
    ...
    'eti_marketing_cms',
    'ckeditor',
  ]
```

2. Include the `URLconf` in the project _before_ `pages.urls`:

```python
  url(r'^', include('eti_marketing_cms.urls')),
```

3. `python manage.py migrate` to migrate the models

4. Once you have the django admin going, go to **Sites** and add the site's domain in place of **example.com** - That because if you don't do that. The **View on Site** button will not work correctly.


### Templates

You may configure the base template that the templates in this package extend
from by changing the `ETI_MARKETING_CMS_BASE_TEMPLATE` setting:

```python
ETI_MARKETING_CMS_BASE_TEMPLATE = 'my_base_template.html'
```

It defaults to `base.html`, so if that exists in your project you should be
fine.

### Signup Form

A signup form that talks with Active Campaign is included. To use it, set the
following config in your Django settings at a minimum:

* `ACTIVE_CAMPAIGN_API_URL`: The URL your AC instance resides at.
* `ACTIVE_CAMPAIGN_API_KEY`: API key

Then, add a URL conf for the `eti_marketing_cms.views.SignupView` view:

```python
# urls.py

from django.conf.urls import url
from eti_marketing_cms.views import SignupView

urlpatterns = [
  url(r'^signup/$', SignupView.as_view(), name='signup'),
]
```

You may also optionally specify a `ACTIVE_CAMPAIGN_LIST_SUBSCRIPTIONS` setting, which should be a `list` of mailing list IDs that you'd like all new contacts to be subscribed to.

Feel free to subclass the `SignupForm` class if you need to provide additional
fields or change the mapping of form fields to Active Campaign fields. If you
end up subclassing the form but do not wish to also subclass the `SignupView`,
you can set the `ETI_MARKETING_CMS_SIGNUP_FORM_CLASS` Django setting to the
fully-qualified class name of your form and it will be used instead.

### Active Campaign Event Tracking

Additionally, you may also track events with Active Campaign using the
`eti_marketing_cms.active_campaign.track_event` function. To use it, first
configure the following options in your Django settings:

* `ACTIVE_CAMPAIGN_EVENT_URL`: URL to post events to. Defaults to `https://trackcmp.net/event`.
* `ACTIVE_CAMPAIGN_EVENT_ACTID`: ActID for the events API
* `ACTIVE_CAMPAIGN_EVENT_KEY`: Key for the events API

Then call it like so:

```python
from eti_marketing_cms.active_campaign import track_event

track_event('test@example.com', 'my_event_name', ...an optional dict of event
data...)
```

### Signup Form + Event Tracking

You can use the signup form _and_ the event tracking together by first setting
up both components as detailed above, then setting the `ACTIVE_CAMPAIGN_SIGNUP_EVENT` option in your Django settings to the name of the event that should be tracked whenever the contact form is filled out.

Development
-----------

* `make init`: Installs dependencies and gets you ready to roll.
* `make migrations`: Generates new migrations (for when you change the models)
* `make test`: Runs the test suite
* `make lint`: Runs `flake8`

Check out the `Makefile` for more functionality.
