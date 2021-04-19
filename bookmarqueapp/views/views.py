from flask import Flask, render_template, url_for
from bookmarqueapp import app, db
from bookmarqueapp.models.books import Book, BookCategory, Categories

@app.route('/')
def homepage():

    featured = Book.query.filter(Book.categories.any(BookCategory.categoryID
        == Categories.FEATURED.value))
    new = Book.query.filter(Book.categories.any(BookCategory.categoryID
        == Categories.NEWLY_RELEASED.value))

    return render_template('index.html', featured=featured, newly_released=new)

@app.route('/search/')
def search():
    return render_template('browse/search_view.html')

@app.route('/view/<ISBN>')
def book_details(ISBN):
    current_book = Book.query.filter(Book.ISBN == ISBN).one()
    return render_template('browse/book_details.html', book=current_book)
