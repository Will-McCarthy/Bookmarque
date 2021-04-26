from flask import Flask, render_template, url_for, redirect, request
from bookmarqueapp import app, db
from bookmarqueapp.models.books import Book, BookCategory, Categories

@app.route('/')
def homepage():

    featured = Book.query.filter(Book.categories.any(BookCategory.categoryID
        == Categories.FEATURED.value))
    new = Book.query.filter(Book.categories.any(BookCategory.categoryID
        == Categories.NEWLY_RELEASED.value))

    return render_template('index.html', featured=featured, newly_released=new)

@app.route('/search', methods=['POST', 'GET'])
@app.route('/search/<type>/<term>', methods=['POST', 'GET'])
def search(type=None, term=None):

    results = None # start with empty results

    # if posted to, process the post and redirect to itself
    if request.method == 'POST':
        type = request.form.get('search-type')
        term = request.form.get('search-text')
        return redirect(url_for('search', type=type, term=term))

    if request.method == 'GET':
        print('get')

        # if received both search types
        if type and term:
            # iterate through search options
            if type == "all":
                print('all')
            elif type == "isbn":
                print('isbn')
            elif type == "title":
                print('title')
            elif type == "author":
                print('author')
            elif type == "genre":
                print('genre')

                # determine if string category or int category


                # verify term is a valid category and try to get results
                try:
                    term = Categories(int(term))
                    results = Book.query.filter(Book.categories.any(BookCategory.categoryID == term.value)).all()
                    term = term.name.capitalize().replace("_", " ")
                except:
                    term = None

            # type is not of approved type so show default page with term if present
            else:
                results = Book.query.all()
                type = None

        # received blank for either so show default search view
        else:
            results = Book.query.all()

        # always render with results as param, None type will be handled within template
        return render_template('browse/search_view.html', search_results=results, type=type, term=term)

    # all else fails, show defautl search page
    return redirect(url_for('search'))

@app.route('/view/<ISBN>')
def book_details(ISBN):
    current_book = Book.query.filter_by(ISBN=ISBN).first()
    if current_book:
        return render_template('browse/book_details.html', book=current_book)
    else: # if no matching isbn
        return redirect(url_for('search'))
