"""
WSGI config for scholarship_mgmt project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/howto/deployment/wsgi/
"""

import os
import sys
from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "scholarship_mgmt.settings_prod")
sys.path.append("/var/www/html/scholarship_mgmt")
sys.path.append("/var/www/html/var")
application = get_wsgi_application()
