from asgiref.wsgi import WsgiToAsgi
from hello_app_flask.app import app
# Wrapping the Flask WSGI application with WsgiToAsgi to make it compatible with ASGI servers
asgi_app = WsgiToAsgi(app)