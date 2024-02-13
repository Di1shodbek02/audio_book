
import os

from django.core.wsgi import get_wsgi_application

settings_module = 'AudioBook.deployment' if 'WEBSITE_HOSTNAME' in os.environ else 'AudioBook.settings'
os.environ.setdefault('DJANGO_SETTINGS_MODULE', settings_module)

application = get_wsgi_application()
