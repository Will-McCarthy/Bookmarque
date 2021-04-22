from flask import Flask, redirect, request, render_template, url_for
from flask import session
from flask_mysqldb import MySQL #Mysql
from flask_login import LoginManager, current_user, login_user, logout_user, login_required #Login

from bookmarqueapp import app, db, mysql, login_manager, email_server
from bookmarqueapp.models.books import Book, BookCategory, Categories
from bookmarqueapp.models.users import User, Address

#from flask import session
#from flask_mysqldb import MySQL #Mysql
#from flask_login import LoginManager, current_user, login_user, logout_user, login_required #Login

#from bookmarqueapp import app, mysql, db, login_manager, email_server
#from bookmarqueapp.models.users import User, Address

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

@app.route('/view/<ISBN>', methods = ['POST', 'GET'])
def book_details(ISBN):
    current_book = Book.query.filter(Book.ISBN == ISBN).one()

    if request.method == 'POST':
        cursor = mysql.connection.cursor()
        amount = request.form.get('addCartAmount')
        submit = request.form.get('addCart')
        if submit == "Add to Cart":
            cID = current_user.get_id()
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
