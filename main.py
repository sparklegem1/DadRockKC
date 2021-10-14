from functools import wraps

from flask import Flask, render_template, redirect, url_for, flash, request, jsonify
from flask_bootstrap import Bootstrap
from sqlalchemy import column
from sqlalchemy.orm import relationship
from werkzeug.exceptions import abort
from werkzeug.security import generate_password_hash, check_password_hash
from web_bots import *
from flask_sqlalchemy import SQLAlchemy
from flask_ckeditor import CKEditor
# from datetime import date
# from functools import wraps
# from flask import abort
# from werkzeug.security import generate_password_hash, check_password_hash
# from sqlalchemy.orm import relationship
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user
from forms import CommentForm, LoginForm
# from flask_gravatar import Gravatar
from datetime import datetime
# import os





############################### API DESCRIPTION ###################################
# Get all information about local shows from one site with the local gig api
# Employing web scraping to get show information from local sites to provide
# up to date info on local shows



app = Flask(__name__)

#db
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///dadrockkc3.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'huffingpaint60'
ckeditor = CKEditor(app)
Bootstrap(app)
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)

YOUTUBE_URL = "https://www.youtube.com/channel/UCihF4V5Y1pZUuKQha4vtsIA/videos"

# database for all venues

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
    venue_comments = relationship('VenueComment', back_populates='comment_author')

    def to_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}

db.create_all()

# database for all venues
class Venue(db.Model):
    __tablename__ = 'venue'
    id = db.Column(db.Integer, primary_key=True)
    venue_name = db.Column(db.String(20), nullable=False)
    city = db.Column(db.String(20), nullable=False)

    #reviews relationship
    venue_reviews = relationship('VenueReview', back_populates='parent_post')
    show_reviews = relationship('ShowReview', back_populates='venue')
    #
db.create_all()



# A database for reviews of Shows
class ShowReview(db.Model):
    __tablename__ = 'show_review'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), nullable=False)
    artist_names = db.Column(db.String(100), nullable=True)
    venue = db.Column(db.String(20), nullable=False)
    date = db.Column(db.String(250), nullable=False)
    genre = db.Column(db.String(15), nullable=False)
    price = db.Column(db.Float(20), nullable=False)
    rating = db.Column(db.String(10), nullable=False)
    review = db.Column(db.String(2000), nullable=False)

    #User relationship
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = relationship('User', back_populates='show_reviews')

    # venue relationship
    venue_id = db.Column(db.Integer, db.ForeignKey('venue.id'))
    venue = relationship('Venue', back_populates='show_reviews')

    # Children
    comments = relationship('ShowComment', back_populates='show_parent')

    def to_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}

db.create_all()

class VenueReview(db.Model):
    __tablename__ = 'venue_review'
    id = db.Column(db.Integer, primary_key=True)
    review_title = db.Column(db.String(20), nullable=False)
    venue_name = db.Column(db.String(20), nullable=False)
    review = db.Column(db.String(2000), nullable=False)

    #User relationship
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = relationship('User', back_populates='venue_reviews')

    #venue relationship
    venue_id = db.Column(db.Integer, db.ForeignKey('venue.id'))
    parent_post = relationship('Venue', back_populates='venue_reviews')

    # Children
    comments = relationship('VenueComment', back_populates='venue_parent')

    def to_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}

db.create_all()

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

    def to_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}


db.create_all()

class ShowComment(db.Model):
    __tablename__ = 'show_comment'
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(250))

    #user relationship
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    comment_author = relationship('User', back_populates='show_comments')

    # Parent
    show_id = db.Column(db.Integer, db.ForeignKey('show_review.id'))
    show_parent = relationship('ShowReview', back_populates='comments')


    def to_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}

db.create_all()




####################################### REST API #########################################


# ADMIN ONLY
def admin_only(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            if current_user.id != 9:
                return abort(403)
        except AttributeError:
            return abort(403)
        return f(*args, **kwargs)
    return decorated_function


@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('404.html'), 404


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# HOME PAGE
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/all-bots')
def all_bots():
    return render_template('bots.html')

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

# RETURN JSON #
@app.route('/json/<dict>')
def return_json(dict):
    return jsonify(dict)

# CREATE ACCOUNT #
@app.route('/create-account/<username>/<password>/<email>', methods=['GET', 'POST'])
def create_user_account(username, password, email):
    ###### This endpoint is for API client use, html version below #################
    form = {'username': username, 'password': password, 'email': email}

    if form:
        # HAD TO PUT .first() TO GET IT TO WORK, OTHERWISE ALL EMAILS WOULD TRIGGER THIS IF STATEMENT
        if User.query.filter_by(email=form['email']).first() or User.query.filter_by(username=form['username']).first():
            return jsonify({'message': 'arg, there be another who bears either the same name, or the same address of electronic mail'})
        to_hash = form['password']
        hash = generate_password_hash(to_hash, method='pbkdf2:sha256', salt_length=8)
        new_user = User(
            username=form['username'],
            email=form['email'],
            password=hash
        )
        db.session.add(new_user)
        db.session.commit()
        return jsonify({'message': f'Welcome {form["username"]}! Tis a pleasure to have you aboard! You may now post reviews and comments. ',
                        'username': form['username'],
                        'email': form['email']})

    return jsonify({'message': 'create-account'})

# HTML CREATE ACCOUNT #
@app.route('/create-account-page', methods=['GET', 'POST'])
def create_account_html():
    ########## This is the html version ###################
    if request.method == 'POST':
        if User.query.filter_by(email=request.form['email']).first() or User.query.filter_by(username=request.form['username']).first():
            return redirect(url_for('return_json', dict={'messsage': 'there is already an account associated with this email or username'}))
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        to_hash = password
        hash = generate_password_hash(to_hash, method='pbkdf2:sha256', salt_length=8)
        new_user = User(
            username=username,
            email=email,
            password=hash
        )
        db.session.add(new_user)
        db.session.commit()
        message = {'username': username, 'email': email}
        return redirect(url_for('return_json', dict=message))

    return render_template('create_user_form.html')

# ADD VENUE #
@app.route('/add-venue', methods=['GET', 'POST'])
def add_venue():
    if request.method == 'POST':
        if not Venue.query.filter_by(venue_name=request.form['venue-name']).first():
            new_venue = Venue(
                venue_name=request.form['venue-name'],
                city=request.form['city']
            )
            db.session.add(new_venue)
            db.session.commit()
            data = {'venue-name': request.form['venue-name'], 'city': request.form['city']}
            return redirect(url_for('return_json', json=data))
    return render_template('add-venue.html')

# POST VENUE REVUEW #
@app.route('/post-venue-review', methods=['GET', 'POST'])
def post_venue_review():
    if request.method == 'POST':
        if Venue.query.filter_by(venue_name=request.form['venue-name']).first():
            new_review = VenueReview(
                review_title=request.form['review-title'],
                venue_name=request.form['venue-name'],
                review=request.form['review'],
                user_id=1,
                venue_id=Venue.query.filter_by(venue_name=request.form['venue-name']).first().id
            )
            db.session.add(new_review)
            db.session.commit()
            message = {'review-title': request.form['review-title'],
                       'venue-name': request.form['venue-name'],
                       'review': request.form['review']}
            return redirect(url_for('return_json', dict=message))
        else:
            message = {'Message': 'this venue is not in the database, you should add it! ;)'}
            return jsonify(message)

    return render_template('venue-review.html')

# VIEW VENUE REVIEW #
@app.route('/venue-review/<int:id>', methods=['GET', 'POST'])
def view_venue_review(id):
    requested_venue = VenueReview.query.get(id)
    comment = CommentForm()
    all_comments = requested_venue.comments

    if request.method == 'POST':
        if not current_user.is_authenticated:
            flash('You must first login to comment')
            return redirect(url_for('login'))
        comment_form_data = comment.comments.data
        new_comment = VenueComment(
            text=comment_form_data,
            user_id=1,
            venue_id=requested_venue.id
        )
        db.session.add(new_comment)
        db.session.commit()
        return redirect(url_for('view_venue_review', id=id))

    return render_template('view-venue-review.html', post=requested_venue, comments=all_comments, form=comment, review_author=requested_venue.user, year=datetime.now().year)

# HTML ALL VENUE REVIEWS
@app.route('/all-venue-reviews', methods=['GET', 'POST'])
def all_venue_reviews_html():
    reviews = VenueReview.query.all()
    return render_template('all-venue-reviews.html', reviews=reviews)


# JSON VENUE REVIEW
@app.route('/get-venue-review/<review_id>')
def venue_review_json(review_id):
    requested_review = VenueReview.query.get(review_id)
    title = requested_review.review_title
    venue =  requested_review.venue_name
    review = requested_review.review
    user = requested_review.user.username
    return jsonify({'review_title': title, 'venue_name': venue, 'review': review, 'user': user})

#JSON ALL VENUE REVIEWS
@app.route('/get-all-venue-reviews')
def all_venue_reviews():
    reviews = VenueReview.query.all()
    review_data = []
    for r in reviews:
        review_dict = {}
        review_dict['title'] = r.review_title
        review_dict['venue'] = r.venue_name
        review_dict['review'] = r.review
        review_dict['user'] = r.user.username
        review_data.append(review_dict)
    return jsonify({'reviews': review_data})

# SHOW REVIEW #
@app.route('/add-show-review', methods=['GET', 'POST'])
def show_review():
    venues = Venue.query.all()
    venue_names = []
    unicorns = ["🦄", "🦄", "🦄", "🦄", "🦄"]
    for venue in venues:
        venue_names.append(venue.venue_name)
    if request.method == 'POST':
        if not current_user.is_authenticated:
            flash('You must first login to make a review')
            return redirect(url_for('login'))
        title = request.form['title']
        artist_names = request.form['artists']
        venue_name = request.form['venue']
        date = request.form['date']
        price = request.form['price']
        rating = request.form['rating']
        review = request.form['review']
        genre = request.form['genre']
        show_review = ShowReview(
            title=title,
            artist_names=artist_names,
            genre=genre,
            date=date,
            rating=rating,
            review=review,
            price=price,
            user_id=current_user.id,
            venue_id=Venue.query.filter_by(venue_name=venue_name).first().id
        )
        db.session.add(show_review)
        db.session.commit()
        return jsonify({'title': title, 'review': review})
    return render_template('add-show-review.html', venue_names=venue_names, unicorns=unicorns)


# SHOW REVIEW HTML
@app.route("/show-review/<int:review_id>", methods=['GET', 'POST'])
def view_show_review(review_id):
    requested_review = ShowReview.query.get(review_id)
    comment = CommentForm()
    all_comments = requested_review.comments
    if request.method == 'POST':
        if not current_user.is_authenticated:
            flash('You must first login to comment')
            return redirect(url_for('login'))
        comment_form_data = comment.comments.data
        new_comment = ShowComment(
            text=comment_form_data,
            user_id=1,
            show_id=requested_review.id
        )
        db.session.add(new_comment)
        db.session.commit()
        return redirect(url_for('view_show_review', review_id=review_id))

    return render_template("show-review.html", post=requested_review, show_author=requested_review.user, form=comment, comments=all_comments, current_user="Scoob", year=datetime.now().year)


# SHOW REVIEW JSON
@app.route('/get-show-review/<int:review_id>')
def show_review_json(review_id):
    review = ShowReview.query.get(review_id)
    if review:
        review_data = {'title': review.title,
                    'artist_names': review.artist_names,
                    'venue': review.venue.venue_name,
                    'date': review.date,
                    'price': review.price,
                    'rating': review.rating,
                    'review': review.review}
        if review.user:
            review_data['user'] = review.user.username
    else:
        return jsonify({'message': 'uh oh! there is no review with this id! r u trippin??'})
    return jsonify(review_data)


# ALL SHOW REVIEWS JSON
@app.route('/get-all-show-reviews')
def all_show_reviews_json():
    reviews = ShowReview.query.all()
    all_review_data = []
    if reviews:
        for review in reviews:
            dict = {'title': review.title,
                    'artist_names': review.artist_names,
                    'venue': review.venue.venue_name,
                    'date': review.date,
                    'price': review.price,
                    'rating': review.rating,
                    'review': review.review}
            all_review_data.append(dict)
        return jsonify({'all_data': all_review_data})
    else:
        return jsonify({'message': 'sorry partner, but this here waterin\' hole is bone dry'})


# ALL SHOW REVIEWS HTML
@app.route('/all-show-reviews')
def all_show_reviews_html():
    reviews = ShowReview.query.all()
    return render_template('all-show-reviews.html', reviews=reviews)


################## SESSION MANAGEMENT ####################
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        user = User.query.filter_by(email=email).first()
        if not user:
            flash('No user with that email')
            return redirect(url_for('login'))
        if user and not check_password_hash(user.password, password):
            flash('Password is incorrect')
            return redirect(url_for('login'))
        if user and check_password_hash(user.password, password):
            if user.id == 1:
                admin = True
                print(admin)
                print(user.posts)
                login_user(user)
                return redirect(url_for('all_venue_reviews_html', admin=admin))
            else:
                login_user(user)
                return redirect(url_for('all_venue_reviews_html'))

    return render_template("login.html", form=form, current_user=current_user, year=datetime.now().year)

# LOGOUT
@app.route('/log-out')
def logout():
    logout_user()
    return redirect(url_for('home', current_user=current_user))


# DELETE FUNCTIONS
@app.route('/delete-venue-review/<int:post_id>')
@admin_only
def delete_venue_review(post_id):
    post_to_delete = VenueReview.query.get(post_id)
    db.session.delete(post_to_delete)
    db.session.commit()
    return redirect(url_for('all_venue_reviews_html', current_user=current_user, year=datetime.now().year))


@app.route('/delete-show-review/<int:post_id>')
@admin_only
def delete_show_review(post_id):
    post_to_delete = ShowReview.query.get(post_id)
    db.session.delete(post_to_delete)
    db.session.commit()
    return redirect(url_for('all_show_reviews_html'))

@app.route('/delete-comment/<type>/<int:id>')
@admin_only
def delete_comment(id, type):
    if type == 'show':
        comment = ShowComment.query.get(id)
        db.session.delete(comment)
        db.session.commit()
        return redirect(url_for('view_show_review', review_id=id))
    if type == 'venue':
        comment = VenueComment.query.get(id)
        db.session.delete(comment)
        db.session.commit()
        return redirect(url_for('view_venue_review', id=id))


"""

Worked on  9/16/21: template for forms, css for forms
//TODO: template for creating show review
//TODO: add show review to database
//TODO: update database to include a title for the show review class.
//TODO: show venue review
//TODO: page for all venue reviews
//TODO: page for all show reviews
//TODO: user login page 
//TODO: logout 
//TODO: make navbar look good
//TODO: admin management
//TODO: make delete method 
//TODO: make bot page
//TODO: Make all posting and commenting exclusive to account holders
TODO: Fix appearance of posts and comments
TODO: install iterm 
TODO: push all items to github
TODO: host site on heroku / switch to postgre




⌘ means Command
⌥ means Option (also called “Alt”)
⌃ means Control
⇧ means Shift

"""

if __name__ == '__main__':
    app.run(debug=True)