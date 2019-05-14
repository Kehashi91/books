from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from wtforms.validators import DataRequired, Optional, ValidationError


class SearchForm(FlaskForm):
    """
    Form for both search and imports
    todo: try to make filters global, not separate for every field
    """
    category = StringField('category',  validators=[Optional()],
                           filters=[lambda x: None if x == '' or x is None else x.strip()])
    author = StringField('author',  validators=[Optional()],
                         filters=[lambda x: None if x == '' or x is None else x.strip()])
    # In the lambdas we have to check if x is already None, otherwise we get type error for strip

    def validate(self):
        """Ensure at least one field is filled"""
        if not FlaskForm.validate(self):  # keep base validation
            return False

        if not self.category.data and not self.author.data:
            raise ValidationError("Fill at least one field!")

        return True


class AddBookForm(FlaskForm):
    """
    Form for manual insert
    """
    title = StringField('title',  validators=[DataRequired()])
    author = StringField('author',  validators=[DataRequired()])
    description = TextAreaField('description')
    category = StringField('category')