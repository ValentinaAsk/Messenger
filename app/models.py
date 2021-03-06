from flask_bcrypt import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from app import db

association = db.Table('association_chats_users', db.Model.metadata,
    db.Column('user_id', db.Integer, db.ForeignKey('users.id')),
    db.Column('chat_id', db.Integer, db.ForeignKey('chats.id'))
)


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(50), nullable=True)
    password = db.Column(db.String(255), nullable=False)
    messages = db.relationship('Message', backref='user', lazy=True)
    chats = db.relationship('Chat', secondary=association, back_populates="users")
    token = db.Column(db.String(255), nullable=True)

    def hash_password(self):
        self.password = generate_password_hash(self.password).decode('utf8')

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self):
        return f'<User {self.name}>'


class Chat(db.Model):
    __tablename__ = 'chats'
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(255))
    messages = db.relationship('Message', backref='chat', lazy=True)
    last_message = db.Column(db.String(255))
    last_message_time = db.Column(db.DateTime())
    sender_id = db.Column(db.Integer(), db.ForeignKey('users.id'))
    users = db.relationship("User", secondary=association, back_populates="chats")

    def __repr__(self):
        return f'<Chat {self.title}>'


class Message(db.Model):
    __tablename__ = 'messages'
    id = db.Column(db.Integer(), primary_key=True)
    sender_id = db.Column(db.Integer(), db.ForeignKey('users.id'))
    chat_id = db.Column(db.Integer(), db.ForeignKey('chats.id'))
    time = db.Column(db.DateTime(), default=datetime.utcnow)
    content = db.Column(db.String(255))

    def __repr__(self):
        return f'<Message {self.content}>'
