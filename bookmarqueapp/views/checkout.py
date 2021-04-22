from flask import Flask, redirect, request, render_template, url_for
from flask import session
from flask_mysqldb import MySQL #Mysql
from flask_login import LoginManager, current_user, login_user, logout_user, login_required #Login

from bookmarqueapp import app, mysql, db, login_manager, email_server
from bookmarqueapp.models.users import User, Address
from bookmarqueapp.models.payment import PaymentCard, CardType

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

@app.route('/cart')
def shopping_cart():
    return render_template('checkout/shopping_cart.html')

@app.route('/cart/history')
def order_history():
    return render_template('checkout/order_history.html')

@app.route('/checkout', methods = ['POST', 'GET'])
def checkout():
    if request.method == 'POST':
        checkout = request.form.get("checkoutButton")
        if (checkout and checkout == "checkout"):
            # Place order button has been pressed
            #Pull data from forms
            promotion = request.form.get("promotion_hidden")
            shipping_addressID = request.form['shipping-option']
            payment_cardID = request.form['payment-option']

            #In a production environment, we should check for consistency between client data and server data.
            #A malicious attacker could change the payment-option html value to another cardID, 
            # and charge a card that wasn't connected to their account
            #Therefore, we would be making sure that the payment_cardID == (one of the current_user.cardIDs)

            #At this point, we would pull all items from the user's cart from the db
            #Sum their totals
            #Apply promotion discount to sum total.
            #Apply tax to sum total.
            #Create order with shipping_addressID & payment_cardID & promotionUsed
            #Then we should increment the promotion's timeUsed db column.

            #Finally redirect to order confirmation

            return render_template('checkout/checkout.html')
        else:
            #Apply Promotion button has been pressed
            apply = request.form.get("promoCode")
            # HTML and SQL Date format is represented as YYYY-MM-DD 
            today = datetime.today().strftime('%Y-%m-%d')

            #Verify Promotion exists and today's date is before the end of the promotion date.
            cursor = mysql.connection.cursor()
            cursor.execute('''SELECT * FROM promotion WHERE promoCode = %s AND promoEnd > %s;''', (apply, today))
            promotion = cursor.fetchone()
            success = False
            if(promotion):
                #Success! promotion exists, refresh page with appropriate visual changes
                success = True
                return render_template('checkout/checkout.html', promo_code=apply, promo_success=True, promo_discount=promotion[1] )
                
            #Promotion invalid, rerender page with appropriate visual changes
            return render_template('checkout/checkout.html', promo_code=apply, promo_success=False )

        

    if request.method == 'GET':
        return render_template('checkout/checkout.html')
        
    

@app.route('/checkout/create-card', methods = ['POST', 'GET'])
@login_required
def checkout_create_card():
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
        return render_template('checkout/checkout_create_card.html')

@app.route('/checkout/create-address', methods = ['POST', 'GET'])
@login_required
def checkout_create_address():
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
        return render_template('checkout/checkout_create_address.html')
