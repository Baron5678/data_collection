from flask import Flask
from hello_app_flask.routers import user_data, index
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from werkzeug.wrappers import Response


# Using blueprints to organize the application into components
app = Flask(__name__)
app.wsgi_app = DispatcherMiddleware(
    Response("Not Found", status=404),
    {
        "/flask": app.wsgi_app
    }
)
app.register_blueprint(index.index_page)
app.register_blueprint(user_data.user_data_page)

if __name__ == '__main__':
    app.run()
