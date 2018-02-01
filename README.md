ETI Marketing
=============

This is Django app that provides miscellaneous marketing functionality for ETI
apps.

Installation
------------

* Make sure you have `virtualenv` activated

```bash
  pip install git+https://github.com/cehdeti/marketing.git
```

If using `pipenv`

```
  pipenv install git+https://github.com/cehdeti/marketing.git#egg=eti-marketing
```

Setting up the Package
----------------------

The package is split up into different apps, depending on which functionality
you'd like to include. At minimum, you must include the following in your
Django settings:

```python
  INSTALLED_APPS = [
    ...
    'eti_marketing',
  ]
```

Read on for instructions on setting up each of apps.

### Landing Pages

1. Add app to `INSTALLED_APPS`:

```python
  INSTALLED_APPS = [
    ...
    'eti_marketing',
    'eti_marketing.landing_page',
    'ckeditor',
  ]
```

2. Include the URLs in your main URL conf. Usually, we like to put these URLs
   into some kind of namespace.

```python
  url(r'^p/', include('eti_marketing.landing_page.urls')),
```

3. Run `python manage.py migrate` to run the database migrations.

4. Once you have the django admin going, go to **Sites** and add the site's domain in place of **example.com** so that the **View on Site** buttons in the admin will work correctly.

### News/Blog

1. Add app to `INSTALLED_APPS`:

```python
  INSTALLED_APPS = [
    ...
    'eti_marketing',
    'eti_marketing.news',
    'ckeditor',
  ]
```

2. Include the URLs in your main URL conf. Usually, we like to put these URLs
   into some kind of namespace.

```python
  url(r'^news/', include('eti_marketing.news.urls')),
```

3. Run `python manage.py migrate` to run the database migrations.

4. Once you have the django admin going, go to **Sites** and add the site's domain in place of **example.com** so that the **View on Site** buttons in the admin will work correctly.

### Signup Form

A signup form that talks with Active Campaign is included. To use it, set the
following config in your Django settings at a minimum:

* `ACTIVE_CAMPAIGN_API_URL`: The URL your AC instance resides at.
* `ACTIVE_CAMPAIGN_API_KEY`: API key

Then, add a URL conf for the `eti_marketing.views.SignupView` view:

```python
# urls.py

from django.conf.urls import url
from eti_marketing.views import SignupView

urlpatterns = [
  url(r'^signup/$', SignupView.as_view(), name='signup'),
]
```

You may also optionally specify a `ACTIVE_CAMPAIGN_LIST_SUBSCRIPTIONS` setting, which should be a `list` of mailing list IDs that you'd like all new contacts to be subscribed to.

Feel free to subclass the `SignupForm` class if you need to provide additional
fields or change the mapping of form fields to Active Campaign fields. If you
end up subclassing the form but do not wish to also subclass the `SignupView`,
you can set the `ETI_MARKETING_SIGNUP_FORM_CLASS` Django setting to the
fully-qualified class name of your form and it will be used instead.

### Active Campaign Event Tracking

Additionally, you may also track events with Active Campaign using the
`eti_marketing.active_campaign.track_event` function. To use it, first
configure the following options in your Django settings:

* `ACTIVE_CAMPAIGN_EVENT_URL`: URL to post events to. Defaults to `https://trackcmp.net/event`.
* `ACTIVE_CAMPAIGN_EVENT_ACTID`: ActID for the events API
* `ACTIVE_CAMPAIGN_EVENT_KEY`: Key for the events API

Then call it like so:

```python
from eti_marketing.active_campaign import track_event

track_event('test@example.com', 'my_event_name', ...an optional dict of event
data...)
```

### Signup Form + Event Tracking

You can use the signup form _and_ the event tracking together by first setting
up both components as detailed above, then setting the `ACTIVE_CAMPAIGN_SIGNUP_EVENT` option in your Django settings to the name of the event that should be tracked whenever the contact form is filled out.

Templates
---------

You may configure the base template that the templates in this package extend
from by changing the `ETI_MARKETING_BASE_TEMPLATE` setting:

```python
ETI_MARKETING_BASE_TEMPLATE = 'my_base_template.html'
```

It defaults to `base.html`, so if that exists in your project you should be
fine.

Development
-----------

* `make init`: Installs dependencies and gets you ready to roll.
* `make migrations`: Generates new migrations (for when you change the models)
* `make test`: Runs the test suite
* `make lint`: Runs `flake8`

Check out the `Makefile` for more functionality.
