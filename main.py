import os

from app import instantiate_app, db
from app.models import Book, Author, Category

app = instantiate_app(os.getenv('FLASK_ENV') or 'development')

@app.cli.command()
def setup_db():
    """Convenience method for adding/modyfing database entries during development"""
    db.create_all()
    db.session.commit()
