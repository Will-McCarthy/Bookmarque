from flask import Flask, render_template, url_for, redirect
from bookmarqueapp import app, db
from bookmarqueapp.models.books import Book, BookCategory, Categories

@app.route('/')
def homepage():

    featured = Book.query.filter(Book.categories.any(BookCategory.categoryID
        == Categories.FEATURED.value))
    new = Book.query.filter(Book.categories.any(BookCategory.categoryID
        == Categories.NEWLY_RELEASED.value))

    return render_template('index.html', featured=featured, newly_released=new)

@app.route('/search')
@app.route('/search/<type>/<term>', defaults={'type': None, 'term': None}, methods=['POST', 'GET'])
def search(type, term):


    results = Book.query.all()

    for result in results:
        print(result.bookTitle)

    # search and load page with search results
    # if request.method == 'POST':
    #     print('post')
    #
    # # load fresh search page
    # if request.method == 'GET':
    #     print('get')

#    return render_template('browse/search_view.html', search_results=results)
    return render_template('browse/search_view.html', search_results=results)

@app.route('/view/<ISBN>')
def book_details(ISBN):
    current_book = Book.query.filter_by(ISBN=ISBN).first()
    if current_book:
        return render_template('browse/book_details.html', book=current_book)
    else: # if no matching isbn
        return redirect(url_for('search'))
