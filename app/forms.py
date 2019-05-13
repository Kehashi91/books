from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from wtforms.validators import DataRequired


class SearchForm(FlaskForm):
    category = StringField('category')
    author = StringField('author')


class AddBookForm(FlaskForm):
    title = StringField('title',  validators=[DataRequired()])
    author = StringField('author',  validators=[DataRequired()])
    description = TextAreaField('description')
    category = StringField('category')