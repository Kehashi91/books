import os
import click

from app import instantiate_app, db
from app.models import Book, Author, Category

app = instantiate_app(os.getenv('FLASK_ENV') or 'development')

@app.cli.command()
def setup_db():
    """Convenience method for adding/modyfing database entries during development"""

    def setup_db():
        """Convenience method for adding/modyfing database entries during development"""
    click.echo("wat")
    x = Book.query.filter(Book.categories.any(name='ciec')).all()
    print(x)



#'CREATE USER books PASSWORD test123;'
'''def setup_db():
    """Convenience method for adding/modyfing database entries during development"""
    admin = Author(name='zorcz')
    sadmin = Author(name='zorcz2')
    cat1 = Category(name='ciec')
    cat3 = Category(name='bj')
    book = Book(name='zorczbook', description='adaad', authors=[admin, sadmin], categories=[cat1, cat3])
    book2 = Book(name='zorczbook', description='adaad', authors=[sadmin], categories=[cat1])
    db.session.add(admin)
    db.session.add(sadmin)
    db.session.add(cat1)
    db.session.add(cat3)
    db.session.add(book2)
    db.session.add(book)
'''