from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

albumGenres = db.Table('album_genres', db.Model.metadata,
    db.Column('album_id', db.Integer, db.ForeignKey('album.id')),
    db.Column('genre_id', db.Integer, db.ForeignKey('genre.id'))
)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(128), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    ratings = db.relationship('Rating', backref='user', lazy='dynamic')

    def __repr__(self):
        return  '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

class Album(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    artist_id = db.Column(db.Integer, db.ForeignKey('artist.id'))
    name = db.Column(db.String(256), index=True)
    released = db.Column(db.Date)
    rating = db.Column(db.Float, default=0)
    genres = db.relationship('Genre', secondary=albumGenres)
    ratings = db.relationship('Rating', backref='album', lazy='dynamic')

    def __repr__(self):
        return  '<Album {}>'.format(self.name)

class Artist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256), index=True)
    albums = db.relationship('Album', backref='artist', lazy='dynamic')
    def __repr__(self):
        return  '<Artist {}>'.format(self.name)

class Genre(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256), index=True)
    description = db.Column(db.String(1024), index=True)
    albums = db.relationship('Album', secondary=albumGenres, overlaps='overlaps')

    def __repr__(self):
        return  '<Genre {}>'.format(self.name)

class Rating(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    album_id = db.Column(db.Integer, db.ForeignKey('album.id'))
    rating = db.Column(db.Integer, index=True)
    review = db.Column(db.String(5096), index=True)
    likes = db.Column(db.Integer, default=0)

    def __repr__(self):
        return  '<Rating {}>'.format(self.rating)