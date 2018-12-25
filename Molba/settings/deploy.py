from .base import *

DEBUG = False

ALLOWED_HOSTS = [
    '.molba.net', 
    'localhost', 
    '.ap-northeast-2.compute.amazonaws.com',
]

#Security settings
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = False
SECURE_HSTS_SECONDS = 60
SECURE_REDIRECT_EXEMPT = []
SECURE_SSL_HOST = None
SECURE_SSL_REDIRECT = False
