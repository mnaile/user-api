from flask import Flask
from extensions.extensions import db,ma




def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"]="postgres://postgres:Test12345@localhost:5432/userdb"
    db.init_app(app)
    ma.init_app(app)
    ctx = app.app_context()
    ctx.push()

    db.create_all()
    # db.drop_all()
    return app