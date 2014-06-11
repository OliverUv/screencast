
#  |  Settings template
#  |
#  |  Copy this file to local_settings.py in the same directory,
#  |  and change the settings so that they agree with your setup.

# ip or url to the idacast-server host that the user should connect
# to from their idacast-client
IDACAST_HOST = '127.0.0.1'
# do the same for port
IDACAST_PORT = '8888'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',     # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': '/home/oliver/.screencast-sq3.db',  # Or path to database file if using sqlite3.
        # The following settings are not used with sqlite3:
        'USER': '',
        'PASSWORD': '',
        'HOST': '',                                 # Empty for localhost through domain sockets or '127.0.0.1' for localhost through TCP.
        'PORT': '',                                 # Set to empty string for default.
    }
}

STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    '/home/oliver/Projects/screencast/static',
)

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    '/home/oliver/Projects/screencast/templates',
)
