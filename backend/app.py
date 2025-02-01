from flask import Flask # web framework
from flask_sqlalchemy import SQLAlchemy # connect to database
from flask_cors import CORS # frontend<>backend
from flask_migrate import Migrate
import os

app = Flask(__name__) #new flask
CORS(app)  # frontend<>backend

# Database Configuration
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///staff.db" # create database
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False # disables a warning

from backend.models import db  # ✅ Import db from backend.models
db.init_app(app)  # ✅ Initialize database
migrate = Migrate(app, db)  # ✅ Enable database migrations

# Import models and routes
from backend.models.staff import Staff  # ✅ Use absolute import
from backend.routes.staff_routes import staff_bp  # ✅ Use absolute import

app.register_blueprint(staff_bp, url_prefix="/api/staff") # all stff api stuff in one place

with app.app_context():  # Ensure Flask is running in the right context
    db.create_all()  # Create tables if they don’t exist


if __name__ == "__main__":
    app.run(debug=True)
