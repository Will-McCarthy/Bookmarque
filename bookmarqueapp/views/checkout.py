from flask import render_template # for file extends
from bookmarqueapp import app

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
    return render_template('checkout/shopping_cart.html')

@app.route('/cart/history')
def order_history():
    return render_template('checkout/order_history.html')
