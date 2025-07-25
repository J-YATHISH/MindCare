from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def init_db():
    from models.user import User
    from models.therapist import Therapist
    from models.journal import Journal
    from models.streaks import Streak
    db.create_all()
