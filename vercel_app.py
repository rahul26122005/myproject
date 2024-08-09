from django.core.wsgi import get_wsgi_application
from django.core.handlers.wsgi import WSGIHandler

# Initialize Django WSGI application
application = get_wsgi_application()

def handler(environ, start_response):
    # Call Django's WSGI application
    return application(environ, start_response)
