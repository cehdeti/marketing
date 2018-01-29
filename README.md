ETI Marketing Landing Pages CMS
===============================

This is a custom Django Admin CMS for creating marketing landing pages for ETI related projects.

The goal of this CMS is consistency so the Marketing staff can easily add new marketing landing pages based on project's styleguide, and without coding. The templates should be extended per project since it's just a barebone to get you started.

INSTALLATION
------------

* Make sure you have `virtualenv` activated

```bash
  pip install git+https://github.com/cehdeti/eti-django-marketing-cms.git
```

If using `pipenv`

```
  pipenv install git+https://github.com/cehdeti/eti-django-marketing-cms.git#egg=django-eti-marketing-cms
```

SETTING UP THE PACKAGE
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

### TEMPLATES

You may configure the base template that the `landing.html` template extends
from by changing the `ETI_MARKETING_CMS_BASE_TEMPLATE` setting:

```python
ETI_MARKETING_CMS_BASE_TEMPLATE = 'my_base_template.html'
```

It defaults to `base.html`, so if that exists in your project you should be
fine.

DEVELOPMENT
-----------

* `make init`: Installs dependencies and gets you ready to roll.
* `make migrations`: Generates new migrations (for when you change the models)
* `make test`: Runs the test suite
* `make lint`: Runs `flake8`

Check out the `Makefile` for more functionality.
