import environ

from mystore.settings.base import *

env = environ.Env(
    DEBUG=(bool, False),
    SECURE_SSL_REDIRECT=(bool, True),
    ACCESS_TOKEN_EXPIRATION=(float, 2),
    REFRESH_TOKEN_EXPIRATION=(float, 6),
    CORS_ALLOWED_ORIGINS=(list, []),
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

GRAPHQL_AUTH = {
    'REGISTER_MUTATION_FIELDS': ['username', 'email', 'first_name', 'last_name'],
    'ALLOW_LOGIN_NOT_VERIFIED': True,
    'SEND_ACTIVATION_EMAIL': False,
}
