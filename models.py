from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)
    
    summaries = db.relationship('Summary', backref='user', lazy=True)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Summary(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original_text = db.Column(db.Text, nullable=False)
    summary_text = db.Column(db.Text, nullable=False)
    summary_length = db.Column(db.Integer, nullable=False)
    original_length = db.Column(db.Integer, nullable=False)
    compression_ratio = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    title = db.Column(db.String(200))
    language = db.Column(db.String(10), default='english')
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'original_text': self.original_text[:100] + '...' if len(self.original_text) > 100 else self.original_text,
            'summary_text': self.summary_text,
            'summary_length': self.summary_length,
            'original_length': self.original_length,
            'compression_ratio': self.compression_ratio,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'language': self.language
        }

