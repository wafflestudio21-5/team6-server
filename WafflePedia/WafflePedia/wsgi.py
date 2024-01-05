"""
WSGI config for WafflePedia project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""

import os, sys

from django.core.wsgi import get_wsgi_application

# add the WafflePedia project path into the sys.path
project_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_path)

# add the virtualenv site-packages path to the sys.path
virtualenv_path = os.path.join(
    project_path, "venv", "lib", "python3.9", "site-packages"
)
sys.path.append(virtualenv_path)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "WafflePedia.settings")

application = get_wsgi_application()
