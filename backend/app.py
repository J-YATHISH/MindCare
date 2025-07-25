from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Config for SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../database/mindcare.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize DB
db = SQLAlchemy(app)

# Import models after db is initialized
#from models.models import User, JournalEntry, TherapistProfile, Rating

# Register blueprints
from routes.auth import auth_bp
# from routes.journal import journal_bp
# from routes.therapists import therapist_bp
# from routes.sentiment import sentiment_bp
# from routes.points import points_bp

app.register_blueprint(auth_bp, url_prefix="/api/auth")
# app.register_blueprint(journal_bp, url_prefix="/api/journal")
# app.register_blueprint(therapist_bp, url_prefix="/api/therapists")
# app.register_blueprint(sentiment_bp, url_prefix="/api/sentiment")
# app.register_blueprint(points_bp, url_prefix="/api/points")

# Run the app
if __name__ == "__main__":
    app.run(debug=True)

