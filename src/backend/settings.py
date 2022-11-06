import os

import environ
from configurations import Configuration
import structlog

env = environ.Env()


class Base(Configuration):

    # Build paths inside the project like this: os.path.join(BASE_DIR, ...)
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    # SECURITY WARNING: keep the secret key used in production secret!
    SECRET_KEY = env.str("SECRET_KEY")

    # SECURITY WARNING: don't run with debug turned on in production!
    DEBUG = env.bool("DEBUG", False)

    ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", default="*")

    # Application definition

    INSTALLED_APPS = [
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
        "djangoql",

        'django_extensions',
        'rest_framework',
        'health_check',
        'health_check.db',
        'health_check.cache',
        'django_celery_results',

        "api",
        "dictionary",
    ]

    MIDDLEWARE = [
        'django.middleware.security.SecurityMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
        'django_structlog.middlewares.RequestMiddleware',
    ]

    ROOT_URLCONF = 'backend.urls'

    TEMPLATES = [
        {
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'DIRS': [os.path.join(BASE_DIR, "templates")],
            'APP_DIRS': True,
            'OPTIONS': {
                'context_processors': [
                    'django.template.context_processors.debug',
                    'django.template.context_processors.request',
                    'django.contrib.auth.context_processors.auth',
                    'django.contrib.messages.context_processors.messages',
                ],
            },
        },
    ]

    WSGI_APPLICATION = 'backend.wsgi.application'

    # Database
    # https://docs.djangoproject.com/en/3.0/ref/settings/#databases

    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "PORT": env.int("DB_PORT", default=5432),
            "HOST": env.str("DB_HOST", default="db"),
            "NAME": env.str("DB_NAME", default="demodb"),
            "USER": env.str("DB_USER", default="demouser"),
            "PASSWORD": env.str("DB_PASSWORD"),
            "CHARSET": "utf8mb4",
        }
    }

    DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

    REDIS_URL = f"redis://{env.str('REDIS_HOST')}:{env.str('REDIS_PORT')}/{env.str('REDIS_CACHE_DB', default='0')}"

    CACHES = {
        "default": {
            "BACKEND": "django_redis.cache.RedisCache",
            "LOCATION": REDIS_URL,
            "OPTIONS": {
                "CLIENT_CLASS": "django_redis.client.DefaultClient",
            },
        }
    }

    AUTH_PASSWORD_VALIDATORS = [
        {
            'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
        },
        {
            'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        },
        {
            'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
        },
        {
            'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
        },
    ]

    # Internationalization
    # https://docs.djangoproject.com/en/3.0/topics/i18n/

    LANGUAGE_CODE = 'en-us'

    TIME_ZONE = 'UTC'

    USE_I18N = True

    USE_L10N = True

    USE_TZ = True

    # Static files (CSS, JavaScript, Images)
    # https://docs.djangoproject.com/en/3.0/howto/static-files/

    STATIC_URL = '/static/'
    STATICFILES_DIRS = [
        os.path.join(BASE_DIR, "statics"),
    ]

    REST_FRAMEWORK = {
        'DEFAULT_RENDERER_CLASSES': [
            'rest_framework.renderers.JSONRenderer',
            'rest_framework.renderers.BrowsableAPIRenderer',
        ],
        'DEFAULT_PARSER_CLASSES': [
            'rest_framework.parsers.JSONParser',
        ]
    }

    CELERY_BROKER_URL = REDIS_URL
    CELERY_RESULT_BACKEND = 'django-db'
    CELERY_ACCEPT_CONTENT = ["application/json"]
    CELERY_TASK_SERIALIZER = "json"
    CELERY_RESULT_SERIALIZER = "json"

    LOGGING = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "verbose": {
                "format": "{levelname} {asctime} {module} {process:d} {thread:d} {message}",
                "style": "{",
            },
            "json": {
                "()": structlog.stdlib.ProcessorFormatter,
                "processor": structlog.processors.JSONRenderer(),
            },
            "plain_console": {
                "()": structlog.stdlib.ProcessorFormatter,
                "processor": structlog.dev.ConsoleRenderer(),
            },
            "key_value": {
                "()": structlog.stdlib.ProcessorFormatter,
                "processor": structlog.processors.KeyValueRenderer(key_order=['timestamp', 'level', 'event', 'logger']),
            },
        },
        "handlers": {
            "console": {"class": "logging.StreamHandler", "formatter": 'verbose'},
            "console_structlog_plain": {"class": "logging.StreamHandler", "formatter": "plain_console"},
            "console_structlog_json": {"class": "logging.StreamHandler", "formatter": "json"},
            "console_structlog_key_value": {"class": "logging.StreamHandler", "formatter": "key_value"},
        },
        "loggers": {
            "django": {
                "handlers": ["console_structlog_plain"],
                "level": os.getenv("DJANGO_LOG_LEVEL", "INFO"),
                "propagate": True,
            },
            "dictionary": {
                "handlers": ["console_structlog_plain"],
                "level": os.getenv("DJANGO_LOG_LEVEL", "INFO"),
                "propagate": True,
            },
            "api": {
                "handlers": ["console_structlog_plain"],
                "level": os.getenv("DJANGO_LOG_LEVEL", "INFO"),
                "propagate": True,
            },
            "celery": {
                "handlers": ["console_structlog_plain"],
                "level": os.getenv("DJANGO_LOG_LEVEL", "INFO"),
                "propagate": True,
            },
            "": {
                "handlers": ["console_structlog_plain"],
                "level": os.getenv("DJANGO_LOG_LEVEL", "INFO"),
                "propagate": True,
            },
        }
    }

    structlog.configure(
        processors=[
            structlog.stdlib.filter_by_level,
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.stdlib.add_logger_name,
            structlog.stdlib.add_log_level,
            structlog.stdlib.PositionalArgumentsFormatter(),
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            structlog.processors.UnicodeDecoder(),
            structlog.processors.ExceptionPrettyPrinter(),
            structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
        ],
        context_class=structlog.threadlocal.wrap_dict(dict),
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )


def show_debug_toolbar(request):
    """Hack to display debug toolbar when running in Docker."""
    if "PYTEST_CURRENT_TEST" in env:
        return False
    return True


class Dev(Base):
    INTERNAL_IPS = ["127.0.0.1"]

    DEBUG_TOOLBAR_CONFIG = {"SHOW_TOOLBAR_CALLBACK": show_debug_toolbar}

    @classmethod
    def setup(cls):
        super(Dev, cls).setup()
        cls.INSTALLED_APPS += [
            "debug_toolbar",
        ]

        cls.MIDDLEWARE.insert(0, "debug_toolbar.middleware.DebugToolbarMiddleware")
        cls.LOGGING["loggers"][""]["level"] = "DEBUG"


class Prod(Base):
    DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
    STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
    AWS_ACCESS_KEY_ID = env.str("AWS_ACCESS_KEY_ID", default="")
    AWS_SECRET_ACCESS_KEY = env.str("AWS_SECRET_ACCESS_KEY", default="")
    AWS_STORAGE_BUCKET_NAME = env.str("AWS_STATICS_STORAGE_BUCKET_NAME", default="")
    AWS_DEFAULT_ACL = "public-read"
    AWS_QUERYSTRING_AUTH = False
    AWS_IS_GZIPPED = True
    # set to "*" to help with container/server ips and allow load balancer to
    # sample the service
    ALLOWED_HOSTS = ["*"]

    @classmethod
    def setup(cls):
        super(Prod, cls).setup()
        cls.LOGGING["loggers"]["django"]["handlers"] = ["console_structlog_json"]
        cls.LOGGING["loggers"]["dictionary"]["handlers"] = ["console_structlog_json"]
        cls.LOGGING["loggers"]["api"]["handlers"] = ["console_structlog_json"]
