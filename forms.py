from flask_wtf import FlaskForm
from flask_ckeditor import CKEditorField
from wtforms import SubmitField, StringField, PasswordField
from wtforms.validators import DataRequired


class CommentForm(FlaskForm):
    comments = CKEditorField("Comment", validators=[DataRequired()])
    submit = SubmitField('Share Comment')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    password = StringField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')