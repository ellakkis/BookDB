import os
from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func

basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
# To solve RuntimeError: Working outside of application context
app.app_context().push()
# CREATE DATABASE
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///new-books-collection.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    rating = db.Column(db.Integer)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())

    def __repr__(self):
        return f'<Books {self.title}>'


db.create_all()


def get_book(book_id):
    return Book.query.get_or_404(book_id)


def add_book(book):
    db.session.add(book)
    db.session.commit()


def delete_book(book_id):
    book = Book.query.get_or_404(book_id)
    db.session.delete(book)
    db.session.commit()


def update_book(book_id, new_rating):
    book_to_edit = get_book(book_id)
    book_to_edit.rating = new_rating
    db.session.commit()


@app.route('/')
def home():
    all_books = Book.query.all()
    return render_template('index.html', books=all_books)


@app.route("/add", methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        a_book = Book(
            title=request.form.get('name'),
            author=request.form.get('author'),
            rating=request.form.get('rating')
        )
        add_book(a_book)
    return render_template('add.html')


@app.route('/edit/<book_id>', methods=['GET', 'POST'])
def edit(book_id):
    if request.method == 'POST':
        update_book(book_id, request.form['rating'])
        return redirect(url_for('home'))
    else:
        book_to_edit = get_book(book_id)
        return render_template('edit.html', book=book_to_edit)


@app.route('/del/<book_id>')
def delete_a_book(book_id):
    delete_book(book_id)
    return redirect('/')


if __name__ == "__main__":
    app.run(debug=True)
