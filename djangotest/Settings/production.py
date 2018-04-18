from djangotest.Settings.base import *

DATABASES['default']=dj_database_url.config()