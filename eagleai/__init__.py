from flask import Flask
from flask_pymongo import PyMongo

mongo = PyMongo()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'eagleai_secret_key'
    #Remove this key when going into production
    app.config['MONGO_URI'] = 'mongodb://localhost:27017/eagleai'

    # client = MongoClient('mongodb://localhost:27017/')
    # db = client.user_login_system
    # app.config['MONGO_URL'] = 'mongodb://localhost:27017/eagleai'

    # mongo.init_app(app)

    from eagleai.views import views
    from eagleai.auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    return app



