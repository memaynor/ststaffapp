from . import db
import requests

class Staff(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)  # Real or display name
    username = db.Column(db.String(100), unique=True, nullable=False)  # Minecraft username
    notes = db.Column(db.Text, nullable=True)  # Extra details
    last_login = db.Column(db.DateTime, nullable=True)  # Last login timestamp
    total_time_online = db.Column(db.Float, default=0)  # Time spent online in hours
    total_weekly_time = db.Column(db.Float, default=0)  # Resets every Sunday
    minecraft_uuid = db.Column(db.String(36), unique=True, nullable=True)  # Minecraft UUID

    @property
    def skin_url(self):
        """Dynamically generates the Crafatar body render URL from the UUID"""
        if self.minecraft_uuid:
            return f"https://crafatar.com/renders/body/{self.minecraft_uuid}?overlay"
        return None  # No skin if no UUID


    def __repr__(self):
        return f"<Staff {self.name} ({self.username}) - {self.minecraft_uuid}>"
    
    def fetch_minecraft_uuid(self):
        try:
            url = f"https://api.mojang.com/users/profiles/minecraft/{self.username}"
            response = requests.get(url)
            if response.status_code == 200:
                uuid = response.json().get("id")
                self.minecraft_uuid = uuid
            else:
                self.minecraft_uuid = None  # Username might be invalid
        except Exception as e:
            print(f"Error fetching Minecraft UUID: {e}")
            self.minecraft_uuid = None
        