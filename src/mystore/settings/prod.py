import environ

from mystore.settings.base import *

env = environ.Env(
    DEBUG=(bool, False),
    SECURE_SSL_REDIRECT=(bool, True),
    ACCESS_TOKEN_EXPIRATION=(float, 2),
    REFRESH_TOKEN_EXPIRATION=(float, 6)
)

DEBUG = env('DEBUG')

SECRET_KEY = env('SECRET_KEY')

ALLOWED_HOSTS = env.list('ALLOWED_HOSTS')

CORS_ALLOWED_ORIGINS = env.list('CORS_ALLOWED_ORIGINS')

SECURE_SSL_REDIRECT = env('SECURE_SSL_REDIRECT')

CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            'hosts': [
                (env('REDIS_URL')),
            ],
        },
    },
}

DATABASES = {
    'default': env.db(),
}

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = env('MAILGUN_SMTP_SERVER')
EMAIL_PORT = env('MAILGUN_SMTP_PORT')
EMAIL_HOST_USER = env('MAILGUN_SMTP_LOGIN')
EMAIL_HOST_PASSWORD = env('MAILGUN_SMTP_PASSWORD')
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False

STRIPE_SECRET_KEY = env('STRIPE_SECRET_KEY')
STRIPE_PUBLIC_KEY = env('STRIPE_PUBLIC_KEY')

GRAPHQL_JWT = {
    'JWT_VERIFY_EXPIRATION': True,
    'JWT_LONG_RUNNING_REFRESH_TOKEN': True,
    'JWT_EXPIRATION_DELTA': timedelta(hours=env('ACCESS_TOKEN_EXPIRATION')),
    'JWT_REFRESH_EXPIRATION_DELTA': timedelta(hours=env('REFRESH_TOKEN_EXPIRATION')),
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
