# -----------------------------------------------------------------------------------
# Sample RapidPro settings file, this should allow you to deploy RapidPro locally on
# a PostgreSQL database.
#
# The following are requirements:
#     - a postgreSQL database named 'temba', with a user name 'temba' and
#       password 'temba' (with postgis extensions installed)
#     - a redis instance listening on localhost
# -----------------------------------------------------------------------------------
import os
import copy
import warnings

from django.core.exceptions import ImproperlyConfigured
from .settings_common import *  # noqa

def env(var_name, default=None):
        try:
            if default:
                return os.environ.get(var_name, default)
            return os.environ[var_name]
        except KeyError:
            msg = "missing environment, name %s" % var_name
            raise ImproperlyConfigured(msg)

STORAGE_URL = "http://localhost:8000/media"

# -----------------------------------------------------------------------------------
# Add a custom brand for development
# -----------------------------------------------------------------------------------

custom = copy.deepcopy(BRANDING["rapidpro.io"])
custom["aliases"] = ["custom-brand.org"]
custom["name"] = "Custom Brand"
custom["slug"] = "custom"
custom["org"] = "Custom"
custom["api_link"] = "http://custom-brand.io"
custom["domain"] = "custom-brand.io"
custom["email"] = "join@custom-brand.io"
custom["support_email"] = "support@custom-brand.io"
custom["allow_signups"] = True
BRANDING["custom-brand.io"] = custom

# make another copy as an alternate domain for custom-domain
custom2 = copy.deepcopy(custom)
custom2["aliases"] = ["custom-brand.io"]
custom2["api_link"] = "http://custom-brand.org"
custom2["domain"] = "custom-brand.org"
custom2["email"] = "join@custom-brand.org"
custom2["support_email"] = "support@custom-brand.org"
BRANDING["custom-brand.org"] = custom2

custom3 = copy.deepcopy(BRANDING["rapidpro.io"])
custom3["aliases"] = ["no-topups.org"]
custom3["name"] = "No Topups"
custom3["slug"] = "notopups"
custom3["org"] = "NoTopups"
custom3["api_link"] = "http://no-topups.org"
custom3["domain"] = "no-topups.org"
custom3["email"] = "join@no-topups.org"
custom3["support_email"] = "support@no-topups.org"
custom3["allow_signups"] = True
custom3["welcome_topup"] = 0
custom3["default_plan"] = "trial"
BRANDING["no-topups.org"] = custom3

# set our domain on our brands to our tunnel domain if set
localhost_domain = os.environ.get("LOCALHOST_TUNNEL_DOMAIN")
if localhost_domain is not None:
    for b in BRANDING.values():
        b["domain"] = localhost_domain

# allow all hosts in dev
ALLOWED_HOSTS = ["*"]

# -----------------------------------------------------------------------------------
# Customize database connection
# -----------------------------------------------------------------------------------

DATABASES["default"]["NAME"] = env("POSTGRES_DB", DATABASES["default"]["NAME"])
DATABASES["default"]["USER"] = env("POSTGRES_USER", DATABASES["default"]["USER"])
DATABASES["default"]["PASSWORD"] = env("POSTGRES_PASSWORD", DATABASES["default"]["PASSWORD"])
DATABASES["default"]["HOST"] = env("POSTGRES_HOST", DATABASES["default"]["HOST"])
DATABASES["default"]["PORT"] = env("POSTGRES_PORT", DATABASES["default"]["PORT"])
DATABASES["direct"] = DATABASES["default"]

# -----------------------------------------------------------------------------------
# Redis & Cache Configuration (we expect a Redis instance on localhost)
# -----------------------------------------------------------------------------------
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": env("REDIS_URL"),
        "OPTIONS": {"CLIENT_CLASS": "django_redis.client.DefaultClient"},
    }
}

INTERNAL_IPS = ("127.0.0.1",)

# -----------------------------------------------------------------------------------
# Mailroom - localhost for dev, no auth token
# -----------------------------------------------------------------------------------
MAILROOM_URL = os.environ.get('MAILROOM_URL', 'http://localhost:8090')
MAILROOM_AUTH_TOKEN = None

# -----------------------------------------------------------------------------------
# Load development apps
# -----------------------------------------------------------------------------------
INSTALLED_APPS = INSTALLED_APPS + ("storages",)

# -----------------------------------------------------------------------------------
# In development, add in extra logging for exceptions and the debug toolbar
# -----------------------------------------------------------------------------------
MIDDLEWARE = ("temba.middleware.ExceptionMiddleware",) + MIDDLEWARE

# -----------------------------------------------------------------------------------
# Perform background tasks asynchronously
# -----------------------------------------------------------------------------------
CELERY_ALWAYS_EAGER = False
CELERY_EAGER_PROPAGATES_EXCEPTIONS = False
BROKER_BACKEND = "memory"

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
# set the location of GDAL and GEOS libraries on linux alpine
# -----------------------------------------------------------------------------------
GEOS_LIBRARY_PATH = '/usr/local/lib/libgeos_c.so'
GDAL_LIBRARY_PATH = '/usr/local/lib/libgdal.so'
