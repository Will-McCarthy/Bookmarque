from flask import Flask, redirect, request, render_template, url_for
from flask import session
from flask_mysqldb import MySQL #Mysql
from flask_login import LoginManager, current_user, login_user, logout_user, login_required #Login

from bookmarqueapp import app, mysql, db, login_manager, email_server
from bookmarqueapp.models.books import Book, BookCategory, Categories
from bookmarqueapp.models.users import User, Address
from bookmarqueapp.models.payment import PaymentCard, CardType
from bookmarqueapp.models.emailFactory import ForgotPasswordEmailFactory, VerifyAccountEmailFactory, OrderSummaryEmailFactory, PromotionEmailFactory, PasswordUpdateEmailFactory

from datetime import datetime


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
@login_required
def shopping_cart():
    cursor = mysql.connection.cursor()
    cID = current_user.get_id() #need to look into checking for non-registered users

    #print(cID)
    cursor.execute('''SELECT COUNT(*) FROM shopping_cart WHERE userID = %s;''', [cID])
    cartExist = cursor.fetchone()
    cartExist = cartExist[0]
    if (cartExist == 0):
        cursor.execute('''INSERT INTO shopping_cart SET userID = %s;''', [cID])

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

@app.route('/checkout', methods = ['POST', 'GET'])
def checkout():
    #Abritary shipping value?
    shipping = 7.50

    #Retrieve User's cartID
    cursor = mysql.connection.cursor()
    cID = current_user.get_id()
    cursor.execute('''SELECT cartID FROM shopping_cart WHERE userID = %s;''', [cID])
    cart = cursor.fetchone()
    cart = cart[0]

    #Retrieving items in user's cart
    cursor.execute('''SELECT * FROM shopping_cart_has_book JOIN book ON book.ISBN = shopping_cart_has_book.ISBN WHERE cartID = %s;''', [cart])
    cartInfo = cursor.fetchall()

    #Retrieving cart price total before modifiers
    cursor.execute('''SELECT SUM(cartBookQuantity * bookPrice) FROM shopping_cart_has_book JOIN book ON book.ISBN = shopping_cart_has_book.ISBN WHERE cartID = %s;''', [cart])
    total = cursor.fetchone()
    #total must be assigned to something for page to render
    if total[0]:
        total = total[0]
    else:
        total = 0
        shipping = 0



    if request.method == 'POST':
        checkout = request.form.get("checkoutButton")
        if (checkout and checkout == "Place Order" and cartInfo):
            print("Im in checkout")
            # Place order button has been pressed
            today = datetime.today().strftime('%Y-%m-%d')
            #Pull data from forms
            promo_code = request.form.get("promotion_hidden")
            shipping_addressID = request.form['shipping-option']
            payment_cardID = request.form['payment-option']

            #Pulling neccessary information from promotion for discount on total
            cursor.execute('''SELECT * FROM promotion WHERE promoCode = %s AND promoEnd > %s;''', (promo_code, today))
            promotion = cursor.fetchone()

            #Then we should increment the promotion's timeUsed db column.
            cursor.execute('''UPDATE promotion SET promoUses = promoUses+1 WHERE promoCode = %s''', ([promo_code]))


            #In a production environment, we should check for consistency between client data and server data.
            #A malicious attacker could change the payment-option html value to another cardID,
            # and charge a card that wasn't connected to their account
            #Therefore, we would be making sure that the payment_cardID == (one of the current_user.cardIDs)

            #Get final cart price here after shipping, tax, and promotion discount
            tax = total * 0.04
            newTotal = total + tax

            #Apply promotion discount to sum total if available
            if(promotion):
                 discount = total*promotion[1]
                 newTotal -= discount
            else:
                promotion = [-1]
            newTotal += shipping

            #Create order
            cursor.execute('''INSERT INTO `order` (orderTime, orderStatus, orderAmount, promoID, addressID, cardID, userID) VALUES (%s,%s,%s,%s,%s,%s,%s);''', (today, "Success", newTotal, promotion[0], shipping_addressID, payment_cardID, cID))

            #We need to fetch the most recent orderID that we just created for order_has_book
            cursor.execute('''SELECT orderID FROM `order` WHERE userID = %s ORDER BY orderID DESC;''', [cID])
            orderID = cursor.fetchone()
            orderID = orderID[0]

            #Translating user's cart items into order_has_book
            for book in cartInfo:
                quantity = book[2]
                bookID = book[1]
                cursor.execute('''INSERT INTO order_has_book (orderID, ISBN, orderBookQuantity) VALUES (%s, %s, %s);''', ([orderID, bookID, quantity]))

            #Wiping user's cart because order has been made
            cursor.execute('''DELETE FROM shopping_cart_has_book WHERE cartID = %s;''', [cart])

            #Finally redirect to order confirmation
            mysql.connection.commit()

            #Redirect them to the order confirmation route
            #Change this redirect to order confirmation screen
            #HERE
            return redirect('/checkout/confirm')
        else:
            #Apply Promotion button has been pressed
            apply = request.form.get("applyButton")
            if (apply and apply == "Apply"):
                promo_code = request.form.get("promoCode")
                # HTML and SQL Date format is represented as YYYY-MM-DD
                today = datetime.today().strftime('%Y-%m-%d')

                #Verify Promotion exists and today's date is before the end of the promotion date.
                cursor = mysql.connection.cursor()
                cursor.execute('''SELECT * FROM promotion WHERE promoCode = %s AND promoEnd > %s;''', (promo_code, today))
                promotion = cursor.fetchone()
                success = False
                if(promotion):
                    #Success! promotion exists, refresh page with appropriate visual changes
                    success = True
                    mysql.connection.commit()
                    return render_template('checkout/checkout.html', cartInfo = cartInfo, total=total, shipping=shipping, promo_code=promo_code, promo_success=True, promo_discount=promotion[1] )

                #Promotion invalid, rerender page with appropriate visual changes
                mysql.connection.commit()
                return render_template('checkout/checkout.html', cartInfo = cartInfo, total=total, shipping=shipping, promo_code=promo_code, promo_success=False )
            else:
                #This is called when the user tries to place an order when they have nothing in their cart.
                return render_template('checkout/checkout.html', cartInfo = cartInfo, total= total, shipping=shipping)




    if request.method == 'GET':
        mysql.connection.commit()
        return render_template('checkout/checkout.html', cartInfo = cartInfo, total= total, shipping=shipping)



@app.route('/checkout/create-card', methods = ['POST', 'GET'])
@login_required
def checkout_create_card():
    #Abritary shipping value?
    shipping = 7.50

    #Retrieve User's cartID
    cursor = mysql.connection.cursor()
    cID = current_user.get_id()
    cursor.execute('''SELECT cartID FROM shopping_cart WHERE userID = %s;''', [cID])
    cart = cursor.fetchone()
    cart = cart[0]

    #Retrieving items in user's cart
    cursor.execute('''SELECT * FROM shopping_cart_has_book JOIN book ON book.ISBN = shopping_cart_has_book.ISBN WHERE cartID = %s;''', [cart])
    cartInfo = cursor.fetchall()

    #Retrieving cart price total before modifiers
    cursor.execute('''SELECT SUM(cartBookQuantity * bookPrice) FROM shopping_cart_has_book JOIN book ON book.ISBN = shopping_cart_has_book.ISBN WHERE cartID = %s;''', [cart])
    total = cursor.fetchone()
    #total must be assigned to something for page to render
    if total[0]:
        total = total[0]
    else:
        total = 0
        shipping = 0

    # save card data
    if request.method == 'POST':

        confirm = request.form.get("createCard")

        # validate form was submitted completely
        if (confirm and confirm == "Confirm"):
            cardList = request.form.get('cardList')
            cardNumber = request.form.get('cardNumber')
            SVC = request.form.get('SVC')
            monthList = request.form.get('monthList')
            yearList = request.form.get('yearList')

            if ((cardList and cardList != "") and (cardNumber and cardNumber != "")
                    and (SVC and SVC != "") and (monthList and monthList != "")
                    and (yearList and yearList != "")):

                expiration = str(yearList) + str(monthList) + "01" # convert into datetime format

                card = PaymentCard(cardNumber=cardNumber, cardExpDate=expiration, cardType=cardList, cardSVC=SVC)

                # add card to user object and database
                current_user.cards.append(card)
                db.session.commit()

        return redirect(url_for('checkout'))

    if request.method == 'GET':
        return render_template('checkout/checkout_create_card.html', cartInfo = cartInfo, total= total, shipping=shipping)

@app.route('/checkout/create-address', methods = ['POST', 'GET'])
@login_required
def checkout_create_address():
    #Abritary shipping value?
    shipping = 7.50

    #Retrieve User's cartID
    cursor = mysql.connection.cursor()
    cID = current_user.get_id()
    cursor.execute('''SELECT cartID FROM shopping_cart WHERE userID = %s;''', [cID])
    cart = cursor.fetchone()
    cart = cart[0]

    #Retrieving items in user's cart
    cursor.execute('''SELECT * FROM shopping_cart_has_book JOIN book ON book.ISBN = shopping_cart_has_book.ISBN WHERE cartID = %s;''', [cart])
    cartInfo = cursor.fetchall()

    #Retrieving cart price total before modifiers
    cursor.execute('''SELECT SUM(cartBookQuantity * bookPrice) FROM shopping_cart_has_book JOIN book ON book.ISBN = shopping_cart_has_book.ISBN WHERE cartID = %s;''', [cart])
    total = cursor.fetchone()
    #total must be assigned to something for page to render
    if total[0]:
        total = total[0]
    else:
        total = 0
        shipping = 0
    # save address data
    if request.method == 'POST':
        print("We're POSTING")

        confirm = request.form.get("createAddress")

        # validate form was submitted completely
        if (confirm and confirm == "Confirm"):
            print("Creating addy")
            street = request.form.get('address')
            city = request.form.get('city')
            state = request.form.get('state')
            zip = request.form.get('zip')
            print("ADDY"+street+" "+city+", " + state + " " + zip)


            if ((street and street != "") and (city and city != "")
                    and (state and state != "") and (zip and zip != "")):
                print("Now we're creating an object")


                address = Address(addressStreet=street, addressCity=city,
                    addressState=state, addressZip=zip)

                # add address to user object and database
                current_user.address = address
                db.session.commit()
                print("Date should be in the DB Now")

        return redirect(url_for('checkout'))

    if request.method == 'GET':
        return render_template('checkout/checkout_create_address.html', cartInfo = cartInfo, total= total, shipping=shipping)

@app.route('/checkout/confirm')
def confirm():
    #get customer ID
    cursor = mysql.connection.cursor()
    cID = current_user.get_id()

    #Get order and order ID
    cursor.execute('''SELECT * FROM `order` WHERE userID = %s ORDER BY orderID DESC;''', [cID])
    order = cursor.fetchone()
    oID = order[0]

    #Get the books in the order
    cursor.execute('''SELECT * FROM order_has_book JOIN book ON book.ISBN = order_has_book.ISBN WHERE orderID = %s;''', [oID])
    orderInfo = cursor.fetchall()

    #orderInfo feilds:
    #orderID, orderTime, orderStatus, orderAmount, promoID, addressID, cardID, userID

    #get variables for the html page and email
    shipping = 7.50
    total = order[3]
    promo_code = order[4]
    promo_success = True
    if promo_code == -1: promo_success = False

    #send email here
    email_factory = OrderSummaryEmailFactory()
    email_factory.email(cID, orderInfo, total, shipping, promo_code, promo_success)

    return render_template('checkout/order_confirm.html', orderInfo = orderInfo, total=total, shipping=shipping, promo_code=promo_code, promo_success=promo_success )
