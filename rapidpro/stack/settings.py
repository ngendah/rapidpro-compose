
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

from .settings_common import *  # noqa
from django.utils.translation import gettext_lazy as _

STORAGE_URL = "http://localhost:8000/media"

# -----------------------------------------------------------------------------------
# Add a custom brand for development
# -----------------------------------------------------------------------------------
# the name of our topup plan
TOPUP_PLAN = "topups"
WORKSPACE_PLAN = "workspace"

# Default plan for new orgs
DEFAULT_PLAN = TOPUP_PLAN
BRANDING = {
    "rapidpro.io": {
        "slug": "localhost",
        "name": "RapidPro",
        "org": "My Org",
        "colors": dict(primary="#0c6596"),
        "styles": ["brands/rapidpro/font/style.css"],
        "default_plan": TOPUP_PLAN,
        "welcome_topup": 1000,
        "email": "join@rapidpro.io",
        "support_email": "support@rapidpro.io",
        "link": "https://app.rapidpro.io",
        "api_link": "https://api.rapidpro.io",
        "docs_link": "http://docs.rapidpro.io",
        "domain": "app.rapidpro.io",
        "ticket_domain": "tickets.rapidpro.io",
        "favico": "brands/rapidpro/rapidpro.ico",
        "splash": "brands/rapidpro/splash.jpg",
        "logo": "brands/rapidpro/logo.png",
        "allow_signups": True,
        "flow_types": ["M", "V", "B", "S"],  # see Flow.FLOW_TYPES
        "location_support": True,
        "tiers": dict(multi_user=0, multi_org=0),
        "bundles": [],
        "welcome_packs": [dict(size=5000, name="Demo Account"), dict(size=100000, name="UNICEF Account")],
        "title": _("Visually build nationally scalable mobile applications"),
        "description": _("Visually build nationally scalable mobile applications from anywhere in the world."),
        "credits": "Copyright &copy; 2012-2022 UNICEF, Nyaruka. All Rights Reserved.",
        "support_widget": False,
    }
}
DEFAULT_BRAND = os.environ.get("DEFAULT_BRAND", "rapidpro.io")

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
CELERY_RESULT_BACKEND = None
CELERY_BROKER_URL = os.environ.get('REDIS_URL',
                             "redis://%s:%d/%d" % (REDIS_HOST, REDIS_PORT, REDIS_DB))
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

