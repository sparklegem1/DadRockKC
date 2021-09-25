from flask_wtf import FlaskForm
from flask_ckeditor import CKEditorField
from wtforms import SubmitField
from wtforms.validators import DataRequired


class CommentForm(FlaskForm):
    comments = CKEditorField("Comments", validators=[DataRequired()])
    submit = SubmitField('Share Comment')
