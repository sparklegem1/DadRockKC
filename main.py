from flask import Flask, render_template, redirect, url_for, flash, request, jsonify
from flask_bootstrap import Bootstrap
from web_bots import *
from flask_sqlalchemy import SQLAlchemy
# from flask_ckeditor import CKEditor
# from datetime import date
# from functools import wraps
# from flask import abort
# from werkzeug.security import generate_password_hash, check_password_hash

# from sqlalchemy.orm import relationship
# from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user
# from forms import CreatePostForm, RegisterForm, LoginForm, CommentForm
# from flask_gravatar import Gravatar
# from datetime import datetime
# import os




############################### API DESCRIPTION ###################################
# Get all information about local shows from one site with the local gig api
# Employing web scraping to get show information from local sites to provide
# up to date info on local shows



app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/all-kunckleheads')
def knuckleheads_times():
    knucklehead_scraper = KnuckleHeadScraper()
    knucklehead_scraper.get_shows()
    return jsonify(knucklehead_schedule=knucklehead_scraper.show_info)


##### KnuckleHeads Scraper ####
# kucklehead_scraper = KnuckleHeadScraper()
# kucklehead_scraper.get_shows()
# kucklehead_scraper.find_price(kucklehead_scraper.show_info[0])

####### Record Bar Scraper #######
# recordbar_scraper = RiotRoomScraper()
# recordbar_scraper.get_shows()


if __name__ == '__main__':
    app.run(debug=True)