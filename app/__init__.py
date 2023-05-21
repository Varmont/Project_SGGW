from flask import Flask
from .extensions import db, login_manager
from .user_management.user import User


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///blog.db"
app.config["SECRET_KEY"] = "DSFDSFGHSHFFSG"
app.static_folder = 'static'

db.init_app(app)
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.filter_by(id=user_id).first()

from .main.routes import main
app.register_blueprint(main)

from .user_management.routes import user_management
app.register_blueprint(user_management)

from .trips.routes import trips
app.register_blueprint(trips)

if __name__ == "__main__":
    app.run(debug=True, port=5000)
