from flask import Flask, redirect, request, render_template, url_for
from flask import session
from flask_mysqldb import MySQL #Mysql
from flask_login import LoginManager, current_user, login_user, logout_user, login_required #Login

from bookmarqueapp import app, db, mysql, login_manager, email_server
from bookmarqueapp.models.books import Book, BookCategory, Categories
from bookmarqueapp.models.users import User, Address

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
                search_terms = term.strip().split(" ") # strip and split the input name on spaces
                current = []
                for word in search_terms:
                    current += Book.query.filter(
                        db.or_(
                            Book.bookTitle.contains(word),
                            Book.bookPublisher.contains(word),
                            Book.bookDescription.contains(word),
                            Book.categories.any(BookCategory.categoryName.contains(word)),
                            Book.authorFName.like(word),
                            Book.authorLName.like(word)
                        )).all()

                    if word.isdigit():
                        current += Book.query.filter(Book.ISBN.contains(word)).all()

                if len(current) != 0:
                    results = unique_list(current)

            elif type == "isbn":
                if term.isdigit():
                    results = Book.query.filter(Book.ISBN.contains(term)).all()

            elif type == "title":
                results = Book.query.filter(Book.bookTitle.contains(term)).all()

            elif type == "author":
                search_names = term.strip().split(" ") # strip and split the input name on spaces

                # iterate through names and see if any match to either first or last name of authors
                for name in search_names:

                    current = Book.query.filter(
                        db.or_(
                            Book.authorFName.like(name),
                            Book.authorLName.like(name)
                        )).all()

                    if len(current) != 0:
                        if results == None:
                            results = current
                        else:
                            results += current

                # if results, ensure uniqueness
                if results:
                    results = unique_list(results)


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

def unique_list(list):
    unique = []
    for item in list:
        if item not in unique:
            unique.append(item)
        list = unique
    return list


@app.route('/view/<ISBN>', methods = ['POST', 'GET'])
def book_details(ISBN):
    current_book = Book.query.filter(Book.ISBN == ISBN).one()

    if request.method == 'POST':
        cursor = mysql.connection.cursor()
        amount = request.form.get('addCartAmount')
        submit = request.form.get('addCart')
        cID = current_user.get_id()
        #print (cID)
        if (submit == "Add to Cart" and cID is not None):
            #cID = current_user.get_id() #need to look into checking for non-registered users
            #print(cID)
            cursor.execute('''SELECT COUNT(*) FROM shopping_cart WHERE userID = %s;''', [cID])
            cartExist = cursor.fetchone()
            cartExist = cartExist[0]
            if (cartExist == 0):
                cursor.execute('''INSERT INTO shopping_cart SET userID = %s;''', [cID])
                
            cursor.execute('''SELECT cartID FROM shopping_cart WHERE userID = %s;''', [cID])
            cart = cursor.fetchone()
            cart = cart[0]
            cursor.execute('''SELECT COUNT(*) FROM shopping_cart_has_book WHERE ISBN = %s AND cartID = %s;''', ([ISBN, cart]))
            count = cursor.fetchone()
            count = count[0]
            if (count != 0): #handles adding book to cart that has already been added
                cursor.execute('''UPDATE shopping_cart_has_book SET cartBookQuantity = cartBookQuantity + %s WHERE ISBN = %s AND cartID = %s;''', ([amount, ISBN, cart]))
            else: #handles adding book to cart that has not yet been added
                cursor.execute('''INSERT INTO shopping_cart_has_book (cartID, ISBN, cartBookQuantity) VALUES (%s, %s, %s);''', ([cart, ISBN, amount]))
            mysql.connection.commit()

    #current_book = Book.query.filter(Book.ISBN == ISBN).one()
    return render_template('browse/book_details.html', book=current_book)
