import os

POSTGRESSQL = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('POSTGRES_DB'),
        'USER': os.getenv('POSTGRES_USER'),
        'PASSWORD': os.getenv('POSTGRES_PASSWORD'),
        'HOST': os.getenv('POSTGRES_HOST', 'reservas_db'),  # o 'db' en Docker
        'PORT': os.getenv('POSTGRES_PORT', 5432),
    }
}