SECRET_KEY = 'NOTASECRET'  # noqa: S105


INSTALLED_APPS = [
    'eti_marketing',
    'eti_marketing.landing_page',
    'eti_marketing.preview',
    'ckeditor',
]


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}


ROOT_URLCONF = 'tests.urls'


DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'
