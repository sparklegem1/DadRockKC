from flask import Flask, render_template, redirect, url_for, flash, request
from flask_bootstrap import Bootstrap
from web_bots import *
# from flask_ckeditor import CKEditor
# from datetime import date
# from functools import wraps
# from flask import abort
# from werkzeug.security import generate_password_hash, check_password_hash
# from flask_sqlalchemy import SQLAlchemy
# from sqlalchemy.orm import relationship
# from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user
# from forms import CreatePostForm, RegisterForm, LoginForm, CommentForm
# from flask_gravatar import Gravatar
# from datetime import datetime
# import os


app = Flask(__name__)


kucklehead_scraper = KnuckleHeadScraper()
kucklehead_scraper.get_shows()

