from decouple import config

from mystore.settings.base import *

DEBUG = True

SECRET_KEY = '+h2l4baub7m(--@vfuxbi5^*-#_^z9c=8(!y4tb@^0o06az4vy'

ALLOWED_HOSTS = ['0.0.0.0', 'localhost']

CORS_ORIGIN_ALLOW_ALL = True

CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            'hosts': [
                (config('REDIS_URL')),
            ],
        },
    },
}

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('DB_NAME'),
        'USER': config('DB_USER'),
        'PASSWORD': config('DB_PASS'),
        'HOST': config('DB_HOST'),
        'PORT': config('DB_PORT'),
    }
}

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = config('EMAIL_HOST')
EMAIL_PORT = config('EMAIL_PORT')
EMAIL_HOST_USER = config('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False

STRIPE_SECRET_KEY = config('STRIPE_SECRET_KEY')
STRIPE_PUBLIC_KEY = config('STRIPE_PUBLIC_KEY')

GRAPHQL_JWT = {
    'JWT_VERIFY_EXPIRATION': True,
    'JWT_LONG_RUNNING_REFRESH_TOKEN': True,
    'JWT_EXPIRATION_DELTA': timedelta(hours=config('ACCESS_TOKEN_EXPIRATION', cast=float)),
    'JWT_REFRESH_EXPIRATION_DELTA': timedelta(hours=config('REFRESH_TOKEN_EXPIRATION', cast=float)),
    'JWT_AUTH_HEADER_PREFIX': 'Bearer',
    'JWT_ALLOW_ANY_CLASSES': [
        'graphql_auth.mutations.Register',
        'graphql_auth.mutations.VerifyAccount',
        'graphql_auth.mutations.ResendActivationEmail',
        'graphql_auth.mutations.SendPasswordResetEmail',
        'graphql_auth.mutations.PasswordReset',
        'graphql_auth.mutations.ObtainJSONWebToken',
        'graphql_auth.mutations.VerifyToken',
        'graphql_auth.mutations.RefreshToken',
        'graphql_auth.mutations.RevokeToken',
    ],
}
