"""
WSGI config for WafflePedia project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""

import os, sys

from django.core.wsgi import get_wsgi_application

# add the WafflePedia project path into the sys.path
root_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

project_path = os.path.join(root_path, "WafflePedia")
sys.path.append(project_path)

# add the virtualenv site-packages path to the sys.path
virtualenv_path = os.path.join(root_path, "venv", "lib", "python3.9", "site-packages")
sys.path.append(virtualenv_path)

print(root_path)
print(project_path)
print(virtualenv_path)
print(sys.path)

# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "WafflePedia.settings")
os.environ["DJANGO_SETTINGS_MODULE"] = "WafflePedia.settings"

application = get_wsgi_application()
