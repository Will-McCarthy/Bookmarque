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

@app.route('/search/<type>/<term>', methods=['POST', 'GET'])
@app.route('/search/<type>', methods=['POST', 'GET'])
@app.route('/search', methods=['POST', 'GET'])
def search(type=None, term=None):

    # if posted to, process the post and redirect to itself as url
    if request.method == 'POST':
        type = request.form.get('search-type').lower() # lowercase to standardize url
        term = request.form.get('search-text')

        # type and term become none if blank
        if not term or term == "":
            term = None

        return redirect(url_for('search', type=type, term=term))

    if request.method == 'GET':
        results = None # start with empty results

        # if received both search types
        if type and term:
            # iterate through search options
            if type == "all":
                results = Book.query.all()
            elif type == "isbn":
                print('isbn')
            elif type == "title":
                print('title')

                Book.query.filter(Book.bookTitle.contains(term))


            elif type == "author":
                search_names = term.strip().split(" ") # strip and split the input name on spaces

                # iterate through names and see if any match to either first or last name of authors
                for name in search_names:
                    print(name)

                    current = Book.query.filter(
                        db.or_(
                            Book.authorFName.like(name),
                            Book.authorLName.like(name)
                        )
                    ).all()

                    if len(current) != 0:
                        if results == None:
                            results = current
                        else:
                            results += current

                # if results, ensure uniqueness
                if results:
                    unique_results = []
                    for book in results:
                        if book not in unique_results:
                            unique_results.append(book)
                    results = unique_results

            elif type == "genre":

                # determine if string category or int category
                # int category
                if term.isdigit():
                    # verify term is a valid category and try to get results
                    try:
                        term = Categories(int(term))
                        results = Book.query.filter(Book.categories.any(BookCategory.categoryID == term.value)).all()
                        term = term.name.capitalize().replace("_", " ")
                    except:
                        term = None
                # string category name
                else:
                    print(term)
                    formatted_category = term.strip().replace(" ", "_")
                    results = Book.query.filter(Book.categories.any(BookCategory.categoryName.like(formatted_category))).all()

            # type is not of approved type so show default page with term if present
            else:
                results = Book.query.all()
                type = None

        # received blank for either so show default search view
        else:
            results = Book.query.all()

        print(results)
        # always render with results as param, None type will be handled within template
        return render_template('browse/search_view.html', search_results=results, type=type, term=term)

    return redirect(url_for('search'))

@app.route('/view/<ISBN>')
def book_details(ISBN):
    current_book = Book.query.filter_by(ISBN=ISBN).first()
    if current_book:
        return render_template('browse/book_details.html', book=current_book)
    else: # if no matching isbn
        return redirect(url_for('search'))
