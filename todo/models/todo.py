import datetime
from . import db  # Import database instance

class Todo(db.Model):
    __tablename__ = 'todos'  # Table name in the database

    # Define columns (fields)
    id = db.Column(db.Integer, primary_key=True)  # Primary key, auto-increment
    title = db.Column(db.String(80), nullable=False)  # Title, required, max length 80 characters
    description = db.Column(db.String(120), nullable=True)  # Description, optional, max length 120 characters
    completed = db.Column(db.Boolean, nullable=False, default=False)  # Task completion status, default is False
    deadline_at = db.Column(db.DateTime, nullable=True)  # Task deadline, can be null
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)  # Record creation timestamp
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)  # Timestamp updated on record update

    # Helper method to convert the model to a dictionary
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'completed': self.completed,
            'deadline_at': self.deadline_at.isoformat() if self.deadline_at else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
        }

    # String representation for debugging
    def __repr__(self):
        return f'<Todo {self.id} {self.title}>'
