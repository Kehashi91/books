from flask import Blueprint, render_template, request, redirect, url_for
from pydash.objects import get
from sqlalchemy import and_
from pydash import map_

import logging

from .models import Book, Category, Author
from .forms import SearchForm, AddBookForm
from . import db
from .api_getters import search_books


books = Blueprint('books', __name__)


@books.route("/", methods=["GET", "POST"])
@books.route("/list", methods=["GET", "POST"])
def list_books():

    author = request.args.get('author')
    category = request.args.get('category')

    form = SearchForm()

    if author and category:
        books = Book.query.filter(and_(Book.categories.any(name=category), (Book.authors.any(name=author)))).all()
    elif author:
        books = Book.query.filter(Book.authors.any(name=author)).all()
    elif category:
        books = Book.query.filter(Book.categories.any(name=category)).all()
    else:
        books = Book.query.all()

    if form.validate_on_submit():
        kwargs = {k: v.strip() for (k, v) in form.data.items() if k is not "csrf_token" and v is not ''}
        return redirect(url_for('books.list_books', **kwargs))

    return render_template("list.html", books=books, form=form)


@books.route("/add", methods=["GET", "POST"])
def add_book():

    form = AddBookForm()

    if form.validate_on_submit():
        book = Book(name=form.title.data,
                    authors=[Author(name=form.author.data)],
                    description=form.description.data,
                    categories=[Category(name=form.category.data)])
        db.session.add(book)
        db.session.commit()

    return render_template("add.html", form=form)


@books.route("/import", methods=["GET", "POST"])
def import_books():

    form = SearchForm()  # we can reuse search form

    if form.validate_on_submit():
        books = search_books(keywords=form.category.data, author=form.author.data)
        if get(books, 'items'):
            for book in books['items']:
                categories = [Category(name=category) for category in get(book, 'volumeInfo.categories', list())]
                authors = [Author(name=author) for author in get(book, 'volumeInfo.authors', list())]
                name = get(book, "volumeInfo.title")
                description = get(book, "volumeInfo.description", "x")
                book = Book(name=name, description=description, authors=authors, categories=categories)
                db.session.add(book)
            db.session.commit()

    return render_template("import.html", form=form)
