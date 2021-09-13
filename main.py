from flask import Flask, render_template, redirect, url_for, flash, request, jsonify
from flask_bootstrap import Bootstrap
from sqlalchemy import column
from sqlalchemy.orm import relationship
from web_bots import *
from flask_sqlalchemy import SQLAlchemy
# from flask_ckeditor import CKEditor
# from datetime import date
# from functools import wraps
# from flask import abort
# from werkzeug.security import generate_password_hash, check_password_hash
# from sqlalchemy.orm import relationship
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user
# from forms import CreatePostForm, RegisterForm, LoginForm, CommentForm
# from flask_gravatar import Gravatar
# from datetime import datetime
# import os





############################### API DESCRIPTION ###################################
# Get all information about local shows from one site with the local gig api
# Employing web scraping to get show information from local sites to provide
# up to date info on local shows



app = Flask(__name__)

#db
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///dadrockkc.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)


# database for all venues
class Venue(db.Model):
    __tablename__ = 'venue'
    id = db.Column(db.Integer, primary_key=True)
    venue_name = db.Column(db.String(20), nullable=False)

    #reviews relationship
    reviews = relationship('VenueReview', back_populates='parent_post')


# A database for reviews of Shows
class ShowReview(db.Model):
    __tablename__ = 'show_review'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), nullable=False)
    date = db.Column(db.String(250), nullable=False)
    genre = db.Column(db.String(15), nullable=False)
    price = db.Column(db.Float(20), nullable=False)
    time = db.Column(db.String(10), nullable=True)
    rating = db.Column(db.String(10), nullable=False)
    review = db.Column(db.String(2000), nullable=False)

    #User relationship
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = relationship('User', back_populates='show_reviews')

    # Children
    comments = relationship('ShowComment', back_populates='show_parent')

    def to_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}

class VenueReview(db.Model):
    __tablename__ = 'venue_review'
    id = db.Column(db.Integer, primary_key=True)
    venue_name = db.Column(db.String(20), nullable=False)
    review = db.Column(db.String(2000), nullable=False)



    #User relationship
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = relationship('User', back_populates='venue_reviews')

    #venue relationship
    parent_post = relationship('Venue', back_populates='reviews')

    # Children
    comments = relationship('VenueComment', back_populates='venue_parent')

    def to_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}



class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(1000))
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))

    #Relationships
    show_reviews = relationship('ShowReview', back_populates='user')
    venue_reviews = relationship('VenueReview', back_populates='user')
    show_comments = relationship('ShowComment', back_populates='comment_author')
    venue_comments = relationship('VenueComment')

    def to_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}



class ShowComment(db.Model):
    __tablename__ = 'show_comment'
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(250))

    #user relationship
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    comment_author = relationship('User', back_populates='comments')

    # Parent
    show_id = db.Column(db.Integer, db.ForeignKey('show_review.id'))
    show_parent = relationship('ShowReview', back_populates='comments')
    parent_post = relationship('', back_populates='comments')

class VenueComment(db.Model):
    __tablename__ = 'venue_comment'
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(250))

    #user relationship
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    comment_author = relationship('User', back_populates='venue_comments')

    # Parent
    venue_id = db.Column(db.Integer, db.ForeignKey('venue_review.id'))
    venue_parent = relationship('VenueReview', back_populates='comments')

@app.route('/')
def home():
    return render_template('index.html')


# Knuckleheads scraper
@app.route('/all-kunckleheads')
def knuckleheads_data():
    knucklehead_scraper = KnuckleHeadScraper()
    knucklehead_scraper.get_shows()
    return jsonify(knucklehead_schedule=knucklehead_scraper.show_info)


# Riot Room scraper
@app.route('/all-riotroom')
def riotroom_data():
    riotroom_scraper = RiotRoomScraper()
    riotroom_scraper.get_shows()
    return jsonify(riotroom_schedule=riotroom_scraper.show_info)


@app.route('/edit-event')
def edit_event():
    pass


if __name__ == '__main__':
    app.run(debug=True)