import os

BASE_DIR=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

POSTGRESSQL = {
    'default':{
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'xx1',
        'USER': 'postgres',
        'PASSWORD' : 'postgres',
        'HOST': 'localhost',
        'PORT': 5432
    }
}