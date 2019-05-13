"""Database models and definitions."""

from . import db



#association table for many-to-many relationship for aurhors
metaauthors = db.Table('metaauthors',
    db.Column('author_id', db.Integer, db.ForeignKey('author.author_id'), primary_key=True),
    db.Column('book_id', db.Integer, db.ForeignKey('book.book_id'), primary_key=True)
)

#association table for many-to-many relationship for aurhors
metacategories = db.Table('metacategories',
    db.Column('category_id', db.Integer, db.ForeignKey('category.category_id'), primary_key=True),
    db.Column('book_id', db.Integer, db.ForeignKey('book.book_id'), primary_key=True)
)


class Book(db.Model):
    __tablename__ = "book"

    book_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    description = db.Column(db.Text, nullable=True)
    authors = db.relationship('Author', secondary=metaauthors, lazy='subquery',
                              backref=db.backref('Book', lazy=True))
    categories = db.relationship('Category', secondary=metacategories, lazy='subquery',
                                 backref=db.backref('Book', lazy=True))

    def __repr__(self):
        return '<book {!r}>'.format(self.name)


class Author(db.Model):

    __tablename__ = 'author'
    author_id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(32), unique = True)

    def __repr__(self):
        return '<author {!r}>'.format(self.name)


class Category(db.Model):

    __tablename__ = 'category'
    category_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), unique=True)

    def __repr__(self):
        return '<category {!r}>'.format(self.name)
