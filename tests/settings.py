SECRET_KEY = 'NOTASECRET'


INSTALLED_APPS = [
    'eti_marketing_cms',
    'ckeditor',
]


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}


ROOT_URLCONF = 'eti_marketing_cms.urls'
