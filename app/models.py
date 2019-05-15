"""Database models and definitions."""
from datetime import datetime
from hashlib import md5

from sqlalchemy.orm import validates

from . import db

#association table for many-to-many relationship for aurhors
metaauthors = db.Table('metaauthors',
    db.Column('author_id', db.Integer, db.ForeignKey('author.author_id'), primary_key=True),
    db.Column('book_id', db.String(32), db.ForeignKey('book.book_id'), primary_key=True)
)

#association table for many-to-many relationship for authors
metacategories = db.Table('metacategories',
    db.Column('category_id', db.Integer, db.ForeignKey('category.category_id'), primary_key=True),
    db.Column('book_id', db.String(32), db.ForeignKey('book.book_id'), primary_key=True)
)


class Book(db.Model):
    __tablename__ = "book"

    book_id = db.Column(db.String(32), primary_key=True)
    added = db.Column(db.DateTime(), nullable=False)
    title = db.Column(db.Text, nullable=False)
    description = db.Column(db.Text, nullable=True)
    authors = db.relationship('Author', secondary=metaauthors, lazy='subquery',
                              backref=db.backref('Book', lazy=True))
    categories = db.relationship('Category', secondary=metacategories, lazy='subquery',
                                 backref=db.backref('Book', lazy=True))

    @classmethod
    def insert_book(cls, title, authors, description, categories, book_id=None):
        """
        Custom setter for books
        """
        # id doubles as checksum to avoid duplicates
        # todo: use non-cryptographic hash for perormance
        book_id = book_id if book_id else md5((title + description + ''.join(authors).strip() + ''.join(categories).strip()).encode('utf-8')).hexdigest()

        categories = [Category.get_or_insert(category.strip()) for category in categories]
        authors = [Author.get_or_insert(author.strip()) for author in authors]

        return cls(book_id=book_id, added=datetime.now(), title=title, description=description, authors=authors, categories=categories)

    def __repr__(self):
        return '<book {!r}>'.format(self.name)

    @validates("book_id")
    def validate_id(cls, key, book_id):
        """
        Check for duplicates based on id
        """
        if Book.query.filter(Book.book_id == book_id).first():
            raise AssertionError("Duplicate book")
        else:
            return book_id


class GetOrInsertMixin:
    """
    Mixin for method shared by Author and Category
    """
    @classmethod
    def get_or_insert(cls, query_to_check):
        duplicate = cls.query.filter(cls.name == query_to_check).first()

        if duplicate:
            return duplicate
        else:
            return cls(name=query_to_check)


class Author(GetOrInsertMixin, db.Model):

    __tablename__ = 'author'
    author_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, unique=True)

    def __repr__(self):
        return '<author {!r}>'.format(self.name)


class Category(GetOrInsertMixin, db.Model):

    __tablename__ = 'category'
    category_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, unique=True)

    def __repr__(self):
        return '<category {!r}>'.format(self.name)
