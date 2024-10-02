DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
    }
}

INSTALLED_APPS = (
    "django.contrib.contenttypes",
    "django.contrib.auth",
    "tests",
)

MIDDLEWARE_CLASSES = []
ROOT_URLCONF = "tests.urls"
EMAIL_BACKEND = "django.core.mail.backends.locmem.EmailBackend"
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
    },
]
