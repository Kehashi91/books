from flask import Blueprint, render_template, request, redirect, url_for, flash
from wtforms.validators import ValidationError
from pydash.objects import get
from sqlalchemy import and_

from .models import Book
from .forms import SearchForm, AddBookForm
from . import db
from .api_getters import BulkSearch


gobooks = Blueprint('gobooks', __name__)


@gobooks.route("/", methods=["GET", "POST"])
@gobooks.route("/list", methods=["GET", "POST"])
def list_books():
    """
    View of books with simple pagination. Allows filtering and querying by category and author (however searches only
    exact matches.
    """
    page = request.args.get('page', 1, type=int)
    author = request.args.get('author')
    category = request.args.get('category')

    form = SearchForm()

    if author and category:
        books = Book.query.filter(and_(Book.categories.any(name=category), (Book.authors.any(name=author))))
    elif author:
        books = Book.query.filter(Book.authors.any(name=author))
    elif category:
        books = Book.query.filter(Book.categories.any(name=category))
    else:
        books = Book.query
    books = books.order_by(Book.added.desc()).paginate(page, 25, False)

    prev_page = url_for('gobooks.list_books', author=author, category=category, page=books.prev_num)\
        if books.has_prev else None
    next_page = url_for('gobooks.list_books', author=author, category=category, page=books.next_num) \
        if books.has_next else None

    try:
        if form.validate_on_submit():
            author = form.author.data
            category =  form.category.data
            return redirect(url_for('gobooks.list_books', author=author, category=category, page=page))
    except ValidationError as e:
        flash(e)

    return render_template("list.html", books=books, form=form, author=author, category=category, prev_page=prev_page,
                           next_page=next_page)


@gobooks.route("/add", methods=["GET", "POST"])
def add_book():
    """
    Add book manually using a form, checking for duplicates
    """
    form = AddBookForm()

    if form.validate_on_submit():
        try:
            book = Book.insert_book(title=form.title.data,
                        authors=[form.author.data],
                        description=form.description.data,
                        categories=[form.category.data])

            db.session.add(book)
            db.session.commit()

            flash("Succesfuly added!")

        except AssertionError:
            flash("Entry already exists!")

    return render_template("add.html", form=form)


@gobooks.route("/import", methods=["GET", "POST"])
def import_books():
    """
    Import books from google API. We limit results to 1000 to avoid potential API ratelimits and to return the response
    in sensible time. We count duplicates that we encounter, both existing in the database and those resulting from
    API pagination overlap.
    """
    form = SearchForm()  # we can reuse search form
    duplicates = 0
    try:
        if form.validate_on_submit():

            search = BulkSearch(max_results=1000)
            books = search.search_bulk(keywords=form.category.data, author=form.author.data)

            for book in books:
                try:
                    book = Book.insert_book(title=get(book, "volumeInfo.title"),
                                            authors=get(book, 'volumeInfo.authors', list()),
                                            description=get(book, "volumeInfo.description", "No description"),
                                            categories=get(book, 'volumeInfo.categories', list()))
                    db.session.add(book)

                except AssertionError:
                    duplicates += 1

            db.session.commit()

            if len(books):
                flash(f"Succesfuly imported {len(books)}! Encountered {duplicates} duplicate entries")
            else:
                flash(f"No books found! :(")

    except ValidationError as e:
        flash(e)

    return render_template("import.html", form=form)

