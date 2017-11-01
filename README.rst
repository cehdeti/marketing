=====
ETI Marketing Landing Pages
=====

This is a custom Django Admin CMS for creating marketing landing pages for ETI related projects.

Quick Start
-----------

1. Add `'marketing'` to `INSTALLED_APPS` in `settings.py`::

	INSTALLED_APPS = [
		...
		'marketing',
	]

2. Include the URLconf in the project::

	url(r'^', include('marketing.urls')),

3. Run `python manage.py migrate` to generate the models.

4. Start the server `python manage.py runserver`

5. Create a superadmin `python manage.py createsuperuser` then create pages at the admin: `http://localhost:8000/admin`


Notes
------

Obviously the templates are just based stuff. You should always extend those from the actualy project `base` template etc...