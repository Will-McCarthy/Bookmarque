from flask import Flask, redirect, request, render_template, url_for
from flask import session
from flask_mysqldb import MySQL #Mysql
from flask_login import LoginManager, current_user, login_user, logout_user, login_required #Logins

from bookmarqueapp import app, mysql, login_manager, email_server, DEBUG_MODE
from bookmarqueapp.models.users import User

@app.route('/profile', methods = ['POST', 'GET'])
@login_required
def profile():
    cursor = mysql.connection.cursor()
    cursor.execute('''SELECT * FROM users WHERE userID = %s;''', [current_user.id])
    information = cursor.fetchall()
    cursor.execute('''SELECT addressStreet, addressCity, addressState, addressZip FROM users JOIN address ON users.addressID = address.addressID WHERE userID = %s;''', [current_user.id])
    address = cursor.fetchall()
    addTest = cursor.rowcount;
    cursor.execute('''SELECT userEmail FROM users WHERE userID = %s;''', [current_user.id])
    email = cursor.fetchone()
    email = email[0]
    cursor.execute('''SELECT users_has_card.cardID, cardNumber, cardExpDate, cardType, cardSVC FROM users_has_card JOIN card ON card.cardID = users_has_card.cardID WHERE userEmail = %s;''', [email])
    card = cursor.fetchall()
    cardTest = cursor.rowcount
    if (cardTest > 0):
        initCard = card[0]
    initial = information[0]
    if (addTest > 0):
        initAdd = address[0]
    if request.method == 'POST':

        fName = request.form.get('fName')
        if (fName is None or fName == ""):
            fName = initial[2]

        lName = request.form.get('lName')
        if (lName is None or lName == ""):
            lName = initial[3]

        address = request.form.get('address')
        if ((address is None or address == "") and addTest > 0):
            address = initAdd[0]

        phone = request.form.get('phone')
        if (phone is None or phone == ""):
            phone = initial[7]

        city = request.form.get('city')
        if ((city is None or city == "") and addTest > 0):
            city = initAdd[1]

        state = request.form.get('state')
        if ((state is None or state == "") and addTest > 0):
            state = initAdd[2]

        zipCode = request.form.get('zip')
        if ((zipCode is None or zipCode == "") and addTest > 0):
            zipCode = initAdd[3]

        # handles update_password form
        password = request.form.get('password')
        if (password is None or password == ""):
            password = initial[6]
        passConfirm = request.form.get('passConfirm') # used to check if password is same in both fields
        submit = request.form.get('Save')
        if (submit is None):
            submit = "Cancel"
        if (submit == "Save" and password == passConfirm and len(password) >= 8):
            cursor.execute('''UPDATE users SET userPassword = %s WHERE userID = %s;''', ([password], current_user.id))

            message = "<h2>Your password has been changed. </h2> <p><br> Your password has been changed, as you asked. </p> <br> <p> If you didn’t ask to change your password, we’re here to help keep your account secure. Visit our support page for more info. </p>"
            subject = "Your password has been changed"
            
            email_server.send_email(message, subject, current_user.email, DEBUG_MODE)


        # handles update_card form and create_card form
        cardList = request.form.get('cardList')
        if ((cardList is None or cardList == "") and cardTest > 0):
            cardList = initCard[3]

        cardNumber = request.form.get('cardNumber')
        if ((cardNumber is None or cardNumber == "") and cardTest > 0):
            cardNumber = initCard[1]

        if (cardTest > 0):
            cID = initCard[0]
        monthList = request.form.get('monthList')
        if ((monthList is None or monthList == "") and cardTest > 0):
            cursor.execute('''SELECT MONTH(cardExpDate) FROM card WHERE cardID = %s;''', [cID])
            monthList = cursor.fetchone()
            monthList = monthList[0]

        yearList = request.form.get('yearList')
        if ((yearList is None or yearList == "") and cardTest > 0):
            cursor.execute('''SELECT YEAR(cardExpDate) FROM card WHERE cardID = %s;''', [cID])
            yearList = cursor.fetchone()
            yearList = yearList[0]

        dateConcat = str(yearList) + str(monthList) + "01" #converts year and month into datetime format

        SVC = request.form.get('SVC')
        if ((SVC is None or SVC == "") and cardTest > 0):
            SVC = initCard[4]

        # confirm is for update card
        confirm = request.form.get("saveCard")
        if (confirm is None):
            confirm = "Cancel"
        if ((confirm == "Save") and cardTest > 0):
            #cursor.execute('''UPDATE card JOIN users_has_card ON card.cardID = users_has_card.cardID JOIN users ON users.userEmail = users_has_card.userEmail JOIN (SELECT MIN(cardID) AS min FROM users_has_card ) AS min ON min.min = users_has_card.cardID SET cardType = %s, cardNumber = %s, cardSVC = %s, cardExpDate = %s WHERE users_has_card.userEmail = %s;''', (cardList, cardNumber, [SVC], dateConcat, email))
            cursor.execute('''UPDATE card JOIN users_has_card ON card.cardID = users_has_card.cardID JOIN users ON users.userEmail = users_has_card.userEmail JOIN (SELECT cardID AS min FROM users_has_card ) AS min ON min.min = users_has_card.cardID SET cardType = %s, cardNumber = %s, cardSVC = %s, cardExpDate = %s WHERE users_has_card.userEmail = %s;''', (cardList, cardNumber, [SVC], dateConcat, email))

        # ensures cards have unique ids
        cursor.execute('''SELECT MAX(cardID) FROM card;''');
        val = cursor.fetchone()
        cardValue = val[0]
        cardValue += 1

        cursor.execute('''SELECT COUNT(*) FROM users_has_card WHERE userEmail = %s;''', [email])
        maxCard = cursor.fetchone()
        maxCard = maxCard[0]

        #test is for create card
        test = request.form.get("createCard")
        if (test is None):
            test = "Exit"
        if (test == "Confirm" and maxCard <= 2):
            cursor.execute('''INSERT INTO card (cardID, cardNumber, cardType, cardSVC, cardExpDate) VALUES (%s, %s, %s, %s, %s);''', ([cardValue], cardNumber, cardList, SVC, dateConcat))
            cursor.execute('''INSERT INTO users_has_card (userEmail, cardID) VALUES (%s, %s);''', (email, [cardValue]))

        status = request.form.get('status')
        password = request.form.get('password')
        cardList = request.form.get('cardList')
        if (status is None and password is None and cardList is None): #not on update_password and status is unchecked
            status = "Deactive"

        #ensures addresses have unique ids
        cursor.execute('''SELECT MAX(addressID) FROM address;''');
        value = cursor.fetchone()
        addressValue = value[0]
        addressValue += 1

        if (status == "Active"): # subscription for promos is checked
            cursor.execute('''UPDATE users SET userFName = %s, userLName = %s, userPhone = %s, userSubStatus = %s WHERE userID = %s;''', (fName, lName, phone, status, [current_user.id]))
        else: # subcription for promos is not checked
            cursor.execute('''UPDATE users SET userFName = %s, userLName = %s, userPhone = %s, userSubStatus = "Deactive" WHERE userID = %s;''', (fName, lName, phone, [current_user.id]))

        cursor.execute('''SELECT addressID FROM users WHERE userID = %s;''', [current_user.id])
        checkValue = cursor.fetchone()
        check = checkValue[0]
        #print(check is None)
        if (password is None and check is None and cardList is None): # not on update_password form and there is no existing address associated
            cursor.execute('''INSERT INTO address (addressID, addressStreet, addressCity, addressState, addressZip) VALUES (%s, %s, %s, %s, %s);''', ([addressValue], address, city, state, zipCode))
            cursor.execute('''UPDATE users SET addressID = %s WHERE userID = %s;''', ([addressValue], current_user.id))
        else:
            cursor.execute('''UPDATE address JOIN users ON users.addressID = address.addressID SET addressStreet = %s, addressCity = %s, addressState = %s, addressZip = %s WHERE users.userID = %s;''', (address, city, state, zipCode, [current_user.id]))
        mysql.connection.commit()


    cursor.execute('''SELECT * FROM users WHERE userID = %s;''', [current_user.id])
    information = cursor.fetchall()
    cursor.execute('''SELECT addressStreet, addressCity, addressState, addressZip FROM users JOIN address ON users.addressID = address.addressID WHERE userID = %s;''', [current_user.id])
    address = cursor.fetchall()
    cursor.execute('''SELECT userEmail FROM users WHERE userID = %s;''', [current_user.id])
    email = cursor.fetchone()
    email = email[0]
    #cursor.execute('''SELECT MIN(users_has_card.cardID), cardNumber, cardExpDate, cardType, cardSVC FROM users_has_card JOIN card ON card.cardID = users_has_card.cardID WHERE userEmail = %s;''', [email])
    cursor.execute('''SELECT users_has_card.cardID, cardNumber, cardExpDate, cardType, cardSVC FROM users_has_card JOIN card ON card.cardID = users_has_card.cardID WHERE userEmail = %s;''', [email])
    cards = cursor.fetchall()

    #cursor.execute('''SELECT users_has_card.userEmail, users_has_card.cardID, cardNumber, cardExpDate, cardType, cardSVC FROM card JOIN users_has_card ON card.cardID = users_has_card.cardID JOIN users ON users.userEmail = users_has_card.userEmail;''')
    #cardDropdown = cursor.fetchall()

    cursor.execute('''SELECT COUNT(addressStreet) FROM users JOIN address ON users.addressID = address.addressID WHERE userID = %s;''', [current_user.id])
    addressCheck = cursor.fetchone()
    addressCheck = addressCheck[0]

    mysql.connection.commit()

    #print(information[0][0])
    #print(address)
    #print(card)
    if (addressCheck == 0):
        return render_template('profile/profile.html', details=information[0], add=address, cards=cards)
    else:
        return render_template('profile/profile.html', details=information[0], add=address[0], cards=cards)
    #return render_template('profile.html')

@app.route('/profile/update-password')
@login_required
def password_panel():
    cursor = mysql.connection.cursor()
    cursor.execute('''SELECT * FROM users WHERE userID = %s;''', [current_user.id])
    information = cursor.fetchall()
    cursor.execute('''SELECT addressStreet, addressCity, addressState, addressZip FROM users JOIN address ON users.addressID = address.addressID WHERE userID = %s;''', [current_user.id])
    address = cursor.fetchall()
    cursor.execute('''SELECT userEmail FROM users WHERE userID = %s;''', [current_user.id])
    email = cursor.fetchone()
    email = email[0]
    #cursor.execute('''SELECT MIN(users_has_card.cardID), cardNumber, cardExpDate, cardType, cardSVC FROM users_has_card JOIN card ON card.cardID = users_has_card.cardID WHERE userEmail = %s;''', [email])
    cursor.execute('''SELECT users_has_card.cardID, cardNumber, cardExpDate, cardType, cardSVC FROM users_has_card JOIN card ON card.cardID = users_has_card.cardID WHERE userEmail = %s;''', [email])
    cards = cursor.fetchall()

    #cursor.execute('''SELECT users_has_card.userEmail, users_has_card.cardID, cardNumber, cardExpDate, cardType, cardSVC FROM card JOIN users_has_card ON card.cardID = users_has_card.cardID JOIN users ON users.userEmail = users_has_card.userEmail;''')
    #cardDropdown = cursor.fetchall()

    #card = cursor.fetchall()

    #cursor.execute('''SELECT users_has_card.userEmail, users_has_card.cardID, cardNumber, cardExpDate, cardType, cardSVC FROM card JOIN users_has_card ON card.cardID = users_has_card.cardID JOIN users ON users.userEmail = users_has_card.userEmail;''')
    #cardDropdown = cursor.fetchall()

    #if request.method == "POST":
        # select edCard contains the the card the user selects from dropdown
    #    selectedCard = request.form.get('cardSelected')
    #    if (selectedCard is None or selectedCard == ""):
    #        selectedCard = cardDropdown[0]
    #else:
    #    selectedCard = cardDropdown[0]
    cursor.execute('''SELECT COUNT(addressStreet) FROM users JOIN address ON users.addressID = address.addressID WHERE userID = %s;''', [current_user.id])
    addressCheck = cursor.fetchone()
    addressCheck = addressCheck[0]

    mysql.connection.commit()

    if (addressCheck == 0):
        return render_template('profile/update_password.html', details=information[0], add=address, cards=cards)
    else:
        return render_template('profile/update_password.html', details=information[0], add=address[0], cards=cards)

@app.route('/profile/update-card')
@login_required
def card_panel():
    cursor = mysql.connection.cursor()
    cursor.execute('''SELECT * FROM users WHERE userID = %s;''', [current_user.id])
    information = cursor.fetchall()
    cursor.execute('''SELECT addressStreet, addressCity, addressState, addressZip FROM users JOIN address ON users.addressID = address.addressID WHERE userID = %s;''', [current_user.id])
    address = cursor.fetchall()
    cursor.execute('''SELECT userEmail FROM users WHERE userID = %s;''', [current_user.id])
    email = cursor.fetchone()
    email = email[0]
    #cursor.execute('''SELECT MIN(users_has_card.cardID), cardNumber, cardExpDate, cardType, cardSVC FROM users_has_card JOIN card ON card.cardID = users_has_card.cardID WHERE userEmail = %s;''', [email])
    cursor.execute('''SELECT users_has_card.cardID, cardNumber, cardExpDate, cardType, cardSVC FROM users_has_card JOIN card ON card.cardID = users_has_card.cardID WHERE userEmail = %s;''', [email])
    cards = cursor.fetchall()

    #cursor.execute('''SELECT users_has_card.userEmail, users_has_card.cardID, cardNumber, cardExpDate, cardType, cardSVC FROM card JOIN users_has_card ON card.cardID = users_has_card.cardID JOIN users ON users.userEmail = users_has_card.userEmail;''')
    #cardDropdown = cursor.fetchall()

    #if request.method == "POST":
        # select edCard contains the the card the user selects from dropdown
    #    selectedCard = request.form.get('cardSelected')
    #    if (selectedCard is None or selectedCard == ""):
    #        selectedCard = cardDropdown[0]
    #else:
    #    selectedCard = cardDropdown[0]
    cursor.execute('''SELECT COUNT(addressStreet) FROM users JOIN address ON users.addressID = address.addressID WHERE userID = %s;''', [current_user.id])
    addressCheck = cursor.fetchone()
    addressCheck = addressCheck[0]

    mysql.connection.commit()
    if (addressCheck == 0):
        return render_template('profile/update_card.html', details=information[0], add=address, cards=cards)
    else:
        return render_template('profile/update_card.html', details=information[0], add=address[0], cards=cards)

@app.route('/profile/create-card')
@login_required
def card_panel_2():
    cursor = mysql.connection.cursor()
    cursor.execute('''SELECT * FROM users WHERE userID = %s;''', [current_user.id])
    information = cursor.fetchall()
    cursor.execute('''SELECT addressStreet, addressCity, addressState, addressZip FROM users JOIN address ON users.addressID = address.addressID WHERE userID = %s;''', [current_user.id])
    address = cursor.fetchall()
    cursor.execute('''SELECT userEmail FROM users WHERE userID = %s;''', [current_user.id])
    email = cursor.fetchone()
    email = email[0]
    #cursor.execute('''SELECT MIN(users_has_card.cardID), cardNumber, cardExpDate, cardType, cardSVC FROM users_has_card JOIN card ON card.cardID = users_has_card.cardID WHERE userEmail = %s;''', [email])
    cursor.execute('''SELECT users_has_card.cardID, cardNumber, cardExpDate, cardType, cardSVC FROM users_has_card JOIN card ON card.cardID = users_has_card.cardID WHERE userEmail = %s;''', [email])
    cards = cursor.fetchall()

    #cursor.execute('''SELECT users_has_card.userEmail, users_has_card.cardID, cardNumber, cardExpDate, cardType, cardSVC FROM card JOIN users_has_card ON card.cardID = users_has_card.cardID JOIN users ON users.userEmail = users_has_card.userEmail;''')
    #cardDropdown = cursor.fetchall()

    #if request.method == "POST":
        # select edCard contains the the card the user selects from dropdown
    #    selectedCard = request.form.get('cardSelected')
    #    if (selectedCard is None or selectedCard == ""):
    #        selectedCard = cardDropdown[0]
    #else:
    #    selectedCard = cardDropdown[0]
    cursor.execute('''SELECT COUNT(addressStreet) FROM users JOIN address ON users.addressID = address.addressID WHERE userID = %s;''', [current_user.id])
    addressCheck = cursor.fetchone()
    addressCheck = addressCheck[0]

    mysql.connection.commit()

    if (addressCheck == 0):
        return render_template('profile/create_card.html', details=information[0], add=address, cards=cards)
    else:
        return render_template('profile/create_card.html', details=information[0], add=address[0], cards=cards)

@app.route('/profile/edit')
@login_required
def edit_profile():
    return render_template('profile/edit_profile.html')
