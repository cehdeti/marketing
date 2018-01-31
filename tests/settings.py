SECRET_KEY = 'NOTASECRET'


INSTALLED_APPS = [
    'eti_marketing_cms',
    'eti_marketing_cms.landing_page',
    'ckeditor',
]


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}


ROOT_URLCONF = 'tests.urls'
