
# -----------------------------------------------------------------------------------
# Sample RapidPro settings file, this should allow you to deploy RapidPro locally on
# a PostgreSQL database.
#
# The following are requirements:
#     - a postgreSQL database named 'temba', with a user name 'temba' and
#       password 'temba' (with postgis extensions installed)
#     - a redis instance listening on localhost
# -----------------------------------------------------------------------------------

import copy
import warnings
from django.utils.translation import gettext_lazy as _
from .settings_common import *  # noqa


ADMINS = ((os.environ.get('ADMIN_USERNAME', "RapidPro"), os.environ.get('ADMIN_EMAIL', "code@yourdomain.io")),)
MANAGERS = ADMINS


STORAGE_URL = "http://localhost:8000/media"

USER_TIME_ZONE = os.environ.get("TZ", USER_TIME_ZONE)

# -----------------------------------------------------------------------------------
# Add a custom brand for development
# -----------------------------------------------------------------------------------
BRANDS.append(
{
        "slug": "localhost",
        "name": "RapidPro",
        "hosts": ["localhost.io"],
        "org": "My Org",
        "domain": "app.localhost.io",
        "colors": dict(primary="#0c6596"),
        "styles": ["brands/rapidpro/font/style.css"],
        "email": "join@localhost.io",
        "support_email": "support@localhost.io",
        "link": "https://app.localhost.io",
        "docs_link": "http://docs.localhost.io",
        "ticket_domain": "tickets.localhost.io",
        "favico": "brands/rapidpro/rapidpro.ico",
        "splash": "brands/rapidpro/splash.jpg",
        "logo": "images/logo-dark.svg",
        "allow_signups": True,
        "title": _("Visually build nationally scalable mobile applications"),
    }
)

# set our domain on our brands to our tunnel domain if set
localhost_domain = os.environ.get("LOCALHOST_TUNNEL_DOMAIN")
if localhost_domain is not None:
    for b in BRANDS:
        b["domain"] = localhost_domain

# allow all hosts in dev
ALLOWED_HOSTS = ["*"]

# CSRF allow localhost
CSRF_TRUSTED_ORIGINS = ["https://localhost",
                        "http://localhost",
                        "https://kiboko.net",
                        "http://kiboko.net",
                        ]

# -----------------------------------------------------------------------------------
# Redis & Cache Configuration (we expect a Redis instance on localhost)
# -----------------------------------------------------------------------------------
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": os.environ.get('REDIS_URL', CACHES["default"]["LOCATION"]),
        "OPTIONS": {"CLIENT_CLASS": "django_redis.client.DefaultClient"},
    }
}

# -----------------------------------------------------------------------------------
# Expand internal ip range
# -----------------------------------------------------------------------------------
INTERNAL_IPS = iptools.IpRangeList("127.0.0.1/24", "192.168.0.10",
                                   "192.168.0.0/24", "172.16.0.0/12",
                                   "10.0.0.0/8", "0.0.0.0")  # network block


# -----------------------------------------------------------------------------------
# Mailroom - localhost for dev, no auth token
# -----------------------------------------------------------------------------------
MAILROOM_URL = os.environ.get('MAILROOM_URL', 'http://localhost:8090')
MAILROOM_AUTH_TOKEN = os.environ.get('MAILROOM_AUTH_TOKEN')

# -----------------------------------------------------------------------------------
# Load development apps
# -----------------------------------------------------------------------------------
INSTALLED_APPS = INSTALLED_APPS + ("storages",)

# -----------------------------------------------------------------------------------
# In development, add in extra logging for exceptions and the debug toolbar
# -----------------------------------------------------------------------------------
MIDDLEWARE = ("temba.middleware.ExceptionMiddleware",) + MIDDLEWARE

# -----------------------------------------------------------------------------------
# In development, perform background tasks in the web thread (synchronously)
# -----------------------------------------------------------------------------------
CELERY_TASK_ALWAYS_EAGER = True
CELERY_TASK_EAGER_PROPAGATES = True
CELERY_RESULT_BACKEND = None
CELERY_BROKER_URL = os.environ.get('REDIS_URL', CELERY_BROKER_URL)

# -----------------------------------------------------------------------------------
# This setting throws an exception if a naive datetime is used anywhere. (they should
# always contain a timezone)
# -----------------------------------------------------------------------------------
warnings.filterwarnings(
    "error", r"DateTimeField .* received a naive datetime", RuntimeWarning, r"django\.db\.models\.fields"
)

# -----------------------------------------------------------------------------------
# Make our sitestatic URL be our static URL on development
# -----------------------------------------------------------------------------------
STATIC_URL = "/sitestatic/"

# -----------------------------------------------------------------------------------
# Configure database connection
# -----------------------------------------------------------------------------------
from urllib.parse import urlsplit
params = urlsplit(os.environ.get('DATABASE_URL',
                             "postgresql://temba:temba@localhost:5432/temba"))

user_passwd, host_port = params.netloc.split('@')
default_database_config = {
    "ENGINE": "django.contrib.gis.db.backends.postgis",
    "NAME": params.path.replace('/','', 1),
    "USER": user_passwd.split(':')[0],
    "PASSWORD": user_passwd.split(':')[1],
    "HOST": host_port.split(':')[0],
    "PORT": host_port.split(':')[1],
    "ATOMIC_REQUESTS": True,
    "CONN_MAX_AGE": 60,
    "OPTIONS": {},
    "DISABLE_SERVER_SIDE_CURSORS": True,
}

DATABASES = {"default": default_database_config, "readonly": default_database_config.copy()}

