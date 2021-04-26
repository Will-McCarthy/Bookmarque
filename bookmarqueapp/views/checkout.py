from flask import Flask, redirect, request, render_template, url_for
from flask import session
from flask_mysqldb import MySQL #Mysql
from flask_login import LoginManager, current_user, login_user, logout_user, login_required #Login

from bookmarqueapp import app, db, mysql, login_manager, email_server
from bookmarqueapp.models.books import Book, BookCategory, Categories
from bookmarqueapp.models.users import User, Address

@app.route('/checkout1')
def checkout1():
    return render_template('checkout/checkout1.html')

@app.route('/checkout2')
def checkout2():
    return render_template('checkout/checkout2.html')

@app.route('/checkout3')
def checkout3():
    return render_template('checkout/checkout3.html')

@app.route('/checkout4')
def checkout4():
    return render_template('checkout/checkout4.html')

@app.route('/checkout5')
def checkout5():
    return render_template('checkout/checkout5.html')

@app.route('/checkout6')
def checkout6():
    return render_template('checkout/checkout6.html')

@app.route('/cart', methods = ['POST', 'GET'])
def shopping_cart():
    cursor = mysql.connection.cursor()
    cID = current_user.get_id() #need to look into checking for non-registered users
    cursor.execute('''SELECT cartID FROM shopping_cart WHERE userID = %s;''', [cID])
    cart = cursor.fetchone()
    cart = cart[0]
    if request.method == "POST":
        delete = request.form.get("deleteButton")
        if (delete == "Delete"):
            ISBN = request.form.get("bookID")
            cursor.execute('''DELETE FROM shopping_cart_has_book WHERE cartID = %s AND ISBN = %s;''', ([cart, ISBN]))
        update = request.form.get("updateAmount")
        if (update == "Update"):
            ISBN = request.form.get("book")
            quantity = request.form.get("bookQuantity")
            cursor.execute('''UPDATE shopping_cart_has_book SET cartBookQuantity = %s WHERE ISBN = %s AND cartID = %s;''', ([quantity, ISBN, cart]))
            
    cursor.execute('''SELECT * FROM shopping_cart_has_book JOIN book ON book.ISBN = shopping_cart_has_book.ISBN WHERE cartID = %s;''', [cart])
    cartInfo = cursor.fetchall()
    cursor.execute('''SELECT SUM(cartBookQuantity * bookPrice) FROM shopping_cart_has_book JOIN book ON book.ISBN = shopping_cart_has_book.ISBN WHERE cartID = %s;''', [cart])
    total = cursor.fetchone()
    test = total[0]
    mysql.connection.commit()
    shipping = 7.50
    if (test is None):
        shipping = 0
        return render_template('checkout/shopping_cart.html', cartInfo=cartInfo, total=0, shipping=shipping)
    else:
        return render_template('checkout/shopping_cart.html', cartInfo=cartInfo, total=total[0], shipping=shipping)

@app.route('/cart/history')
def order_history():
    return render_template('checkout/order_history.html')
