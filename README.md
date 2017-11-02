## ETI Marketing Landing Pages CMS

This is a custom Django Admin CMS for creating marketing landing pages for ETI related projects.

Installing the Package
-----------------

Download the tar file inside the **dist** folder::

```bash
  pip install django-eti-marketing-cms-0.1.tar.gz
```

Quick Start
-----------

1. Add `'marketing'` to **INSTALLED_APPS** in `settings.py`:

```python
  INSTALLED_APPS = [
    ...
    'marketing',
  ]
```

2. Include the `URLconf` in the project _before_ `pages.urls`:

```python
  url(r'^', include('marketing.urls')),
```

3. Run `python manage.py migrate` to generate the models.

4. Start the server `python manage.py runserver`

5. Create a superadmin `python manage.py createsuperuser` then create pages at the admin: `http://localhost:8000/admin`

Notes
------

* **IMAGES & STATIC FILES** This is assuming that you're using the `starthere` project as base that the default static files folder should be `static`, and the CMS pulls the images from `static/images/marketing`

* **TEMPLATES** Obviously the templates are just based stuff. You should always extend those from the actual project `base` template etc...

