from . import db

class Staff(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)  # Real or display name
    username = db.Column(db.String(100), unique=True, nullable=False)  # Minecraft username
    notes = db.Column(db.Text, nullable=True)  # Extra details
    last_login = db.Column(db.DateTime, nullable=True)  # Last login timestamp
    total_time_online = db.Column(db.Float, default=0)  # Time spent online in hours

    def __repr__(self):
        return f"<Staff {self.name} ({self.username})>"
