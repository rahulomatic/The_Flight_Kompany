from flask import Flask
from config import Config
import os
from extensions import db, login_manager



def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    login_manager.init_app(app)
    
    from models.user import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))


    from models.user import User

    from routes.main import main_bp
    from routes.auth import auth_bp
    from routes.flights import flights_bp
    from routes.bookings import bookings_bp
    from routes.admin import admin_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(flights_bp)
    app.register_blueprint(bookings_bp)
    app.register_blueprint(admin_bp)

    with app.app_context():
        os.makedirs("database", exist_ok=True)
        db.create_all()

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True)

