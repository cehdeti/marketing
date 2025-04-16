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
Don't forget to add this to `requirements.txt` if you are _not_ using `pipenv` or run `pip freeze > requirements.txt`:

```bash
  -e git+https://github.com/cehdeti/marketing.git#egg=eti_marketing
```

If using `pipenv`

```
  pipenv install git+https://github.com/cehdeti/marketing.git#egg=eti_marketing
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

### Google Analytics/GTM/Active Campaign/Twitter Trackers

This package contains template tags you can use to output GA, GTM, and AC
tracking, Twitter Pixel scripts. First, configure the following settings in your `settings.py` (you don't need all
of them if they don't apply):

* `GOOGLE_ANALYTICS_ID`: The ID of your Google Analytics account (G-xxxxxxxxxx).
* `GOOGLE_TAGMANAGER_ID`: The ID of your GTM account (GTM-xxxxxx).
* `ACTIVE_CAMPAIGN_EVENT_ACTID`: The ID for your AC events (numeric)
* `TWITTER_PIXEL_ID`: The Twitter Pixel ID

Then in your template, do this:

```
{% load marketing %}

<html>
<head>
  ...
  {% google_analytics %}
  {% google_tagmanager %}
  {% active_campaign_event_tracker %}
  {% twitter_pixel_tracker %}
  ...
</head>
<body>
  {% google_tagmanager_noscript %}
</body>
</html>
```

No conditional logic should be necessary to include the tags; if the settings above are not
configured, the template tags will simply not print the scripts.

### Landing Pages

The `landing_page` app provides targeted Landing Pages that can be tailored to
specific audiences.

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
  path('p/', include('eti_marketing.landing_page.urls')),
```

3. Run `python manage.py migrate` to run the database migrations.

4. Once you have the django admin going, go to **Sites** and add the site's domain in place of **example.com** so that the **View on Site** buttons in the admin will work correctly.

### Preview

The `preview` app provides a simple slideshow for users to preview the app. It also contains a nice drag and drop UI to sort the slides using [`django-admin-sortable2`](http://django-admin-sortable2.readthedocs.io/en/latest/installation.html)

1. Add app to `INSTALLED_APPS`:

```python
  INSTALLED_APPS = [
    ...
    'eti_marketing',
    'eti_marketing.preview',
    'ckeditor',
    'adminsortable2',
  ]
```

2. Tie the view to a specific URL:

```python
  path('preview/', include('eti_marketing.preview.urls')),
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

from django.urls import path
from eti_marketing.views import SignupView

urlpatterns = [
  path('signup/', SignupView.as_view(), name='signup'),
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
