from flask import Flask
from hello_app_flask.routers import user_data, index

# Using blueprints to organize the application into components
app = Flask(__name__)
app.register_blueprint(index.index_page)
app.register_blueprint(user_data.user_data_page)

if __name__ == '__main__':
    app.run()
