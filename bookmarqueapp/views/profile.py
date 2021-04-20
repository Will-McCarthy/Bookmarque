from flask import Flask, redirect, request, render_template, url_for
from flask import session
from flask_mysqldb import MySQL #Mysql
from flask_login import LoginManager, current_user, login_user, logout_user, login_required #Login

from bookmarqueapp import app, mysql, db, login_manager, email_server
from bookmarqueapp.models.users import User, Address
from bookmarqueapp.models.payment import PaymentCard, CardType

@app.route('/profile')
@login_required
def profile():
    return render_template('profile/profile.html')

@app.route('/profile/update-password',methods = ['POST', 'GET'])
@login_required
def update_password():

    if request.method == 'POST':
        # validate password matching
        password = request.form.get('password')
        passConfirm = request.form.get('passConfirm') # used to check if password is same in both fields

        submit = request.form.get('Save')
        if (not submit or not password):
            submit = "Cancel"
        elif (submit == "Save" and password == passConfirm and len(password) >= 8):
            current_user.password = password
            db.session.commit()

            message = "<h2>Your password has been changed. </h2> <p><br> Your password has been changed, as you asked. </p> <br> <p> If you didn’t ask to change your password, we’re here to help keep your account secure. Visit our support page for more info. </p>"
            subject = "Your password has been changed"

            email_server.send_email(message, subject, current_user.userEmail, app.debug)

        return redirect(url_for('profile'))

    if request.method == 'GET':
        return render_template('profile/update_password.html')

@app.route('/profile/update-card', methods = ['POST', 'GET'])
@login_required
def update_card():
    if request.method == 'POST':
        cardID = request.form.get('cardOptions')
        selected_card = PaymentCard.query.filter_by(cardID=cardID).first()

        if selected_card:
            return render_template('profile/update_card.html', card = selected_card)
    return redirect(url_for('profile'))


@app.route('/profile/update-card/save', methods = ['POST', 'GET'])
@login_required
def save_update_card():
    if request.method == 'POST':

        confirm = request.form.get("saveCard")
        cardID = request.form.get('IdCard')

        # validate form was submitted with an ID
        if (confirm and confirm == "Save") and (cardID and cardID != ""):
            selected_card = PaymentCard.query.filter_by(cardID=cardID).first()
            if selected_card:

                cardList = request.form.get('cardList')
                if (cardList and cardList != ""):
                    selected_card.cardType = cardList

                cardNumber = request.form.get('cardNumber')
                if (cardNumber and cardList != ""):
                    selected_card.card_number = cardNumber

                SVC = request.form.get('SVC')
                if (SVC and SVC != ""):
                    selected_card.card_svc = SVC

                # expiration date processed jointly
                monthList = request.form.get('monthList')
                yearList = request.form.get('yearList')
                if (monthList and monthList != "") and (yearList and yearList != ""):
                    # convert into datetime format
                    expiration = str(yearList) + str(monthList) + "01"
                    print(expiration)
                    selected_card.cardExpDate = expiration

                db.session.commit()

    return redirect(url_for('profile'))

@app.route('/profile/create-card', methods = ['POST', 'GET'])
@login_required
def create_card():
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

        return redirect(url_for('profile'))

    if request.method == 'GET':
        return render_template('profile/create_card.html')

@app.route('/profile/edit', methods = ['POST', 'GET'])
@login_required
def edit_profile():
    # save profile changes
    if request.method == 'POST':
        print('posted here')

        # personal info
        fName = request.form.get('fName') # save first name
        if (fName and fName != ""):
            current_user.userFName = fName

        lName = request.form.get('lName') # save last name
        if (fName and fName != ""):
            current_user.userLName = lName

        phone = request.form.get('phone')
        if (phone and phone != ""):
            current_user.userPhone = phone

        sub_status = request.form.get('subscription')
        subscribed = True if sub_status else False
        current_user.set_subscription(subscribed)

        # address
        street = request.form.get('street')
        city = request.form.get('city')
        state = request.form.get('state')
        zip = request.form.get('zip')

        # if address fields exists and are not blank
        if ((street and street != "") and (city and city != "") and (state and state != "")
                                and (zip and zip != "")):
            if (not current_user.address): # if no address created yet
                user_address = Address(addressStreet=street, addressCity=city,
                                    addressState=state, addressZip=zip)
                current_user.address = user_address
            else:
                current_user.address.addressStreet = street
                current_user.address.addressCity = city
                current_user.address.addressState = state
                current_user.address.addressZip = zip


        db.session.commit() # commit changes to database

        return redirect(url_for('profile'))

    if request.method == 'GET':
        return render_template('profile/edit_profile.html')
