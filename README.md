ETI Marketing Landing Pages CMS
===============================

This is a custom Django Admin CMS for creating marketing landing pages for ETI related projects.

INSTALLATION
------------------------

* Make sure you have `virtualenv` activated

```bash
  pip install git+https://github.com/cehdeti/eti-django-marketing-cms.git
```

To uninstall:

```bash
  pip uninstall django-eti-marketing-cms
```

SETTING UP THE PACKAGE
------------------------

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

6. Go to the **Sites** section in the admin, and change the url to `http://localhost:8000` in order for the "View the site" button to work properly.

## IMAGES & STATIC FILES

This is assuming that your project is serving static files with the `static` folder, and this little CMS pulls the images from `static/images/marketing` folder.

### TEMPLATES

To override the default cms templates, these are the files used for it and you should able to override them by creating a `marketing` folder under your project's `templates` folder:

* [base.html](marketing/templates/base.html) - Probably should just extends from the project.
* [landing.html](marketing/templates/landing.html)
* [/includes/header.html](marketing/templates/includes/header.html)
* [/includes/footer.html](marketing/templates/includes/footer.html)

