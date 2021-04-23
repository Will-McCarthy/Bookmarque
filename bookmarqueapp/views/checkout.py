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

@app.route('/cart')
def shopping_cart():
    cursor = mysql.connection.cursor()
    cID = current_user.get_id() #need to look into checking for non-registered users
    cursor.execute('''SELECT cartID FROM shopping_cart WHERE userID = %s;''', [cID])
    cart = cursor.fetchone()
    cart = cart[0]
    cursor.execute('''SELECT * FROM shopping_cart_has_book JOIN book ON book.ISBN = shopping_cart_has_book.ISBN WHERE cartID = %s;''', [cart])
    cartInfo = cursor.fetchall()
    return render_template('checkout/shopping_cart.html', cartInfo=cartInfo)

@app.route('/cart/history')
def order_history():
    return render_template('checkout/order_history.html')
