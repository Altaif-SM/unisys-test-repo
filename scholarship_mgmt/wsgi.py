"""
WSGI config for scholarship_mgmt project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/howto/deployment/wsgi/
"""
import time
import traceback
import signal
import os
import sys
from django.core.wsgi import get_wsgi_application

sys.path.append('/var/www/html/scholarship_mgmt')
sys.path.append('/var/www/html/var/lib/python3.5/site-packages')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "scholarship_mgmt.settings_prod")

try:
    application = get_wsgi_application()
except Exception:
    # Error loading applications
    if 'mod_wsgi' in sys.modules:
        traceback.print_exc()
        os.kill(os.getpid(), signal.SIGINT)
        time.sleep(2.5)
