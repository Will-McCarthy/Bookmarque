from flask import Flask, redirect, request, render_template, url_for
from flask_mysqldb import MySQL #Mysql
from flask_login import current_user, login_required #Logins
import datetime
from bookmarqueapp import app, mysql, db
from bookmarqueapp.models.users import User

@app.route('/profile')
@login_required
def profile():
    return render_template('profile/profile.html')

@app.route('/profile/update-password')
@login_required
def password_panel():
    cursor = mysql.connection.cursor()
    cursor.execute('''SELECT * FROM users WHERE userID = %s;''', [current_user.userID])
    information = cursor.fetchall()
    cursor.execute('''SELECT addressStreet, addressCity, addressState, addressZip FROM users JOIN address ON users.addressID = address.addressID WHERE userID = %s;''', [current_user.userID])
    address = cursor.fetchall()
    cursor.execute('''SELECT userEmail FROM users WHERE userID = %s;''', [current_user.userID])
    email = cursor.fetchone()
    email = email[0]
    #cursor.execute('''SELECT MIN(users_has_card.cardID), cardNumber, cardExpDate, cardType, cardSVC FROM users_has_card JOIN card ON card.cardID = users_has_card.cardID WHERE userEmail = %s;''', [email])
    cursor.execute('''SELECT users_has_card.cardID, cardNumber, cardExpDate, cardType, cardSVC FROM users_has_card JOIN card ON card.cardID = users_has_card.cardID WHERE userEmail = %s;''', [email])


    cursor.execute('''SELECT users_has_card.userEmail, users_has_card.cardID, cardNumber, cardExpDate, cardType, cardSVC FROM card JOIN users_has_card ON card.cardID = users_has_card.cardID JOIN users ON users.userEmail = users_has_card.userEmail;''')
    cardDropdown = cursor.fetchall()

    card = cursor.fetchall()

    cursor.execute('''SELECT users_has_card.userEmail, users_has_card.cardID, cardNumber, cardExpDate, cardType, cardSVC FROM card JOIN users_has_card ON card.cardID = users_has_card.cardID JOIN users ON users.userEmail = users_has_card.userEmail;''')
    cardDropdown = cursor.fetchall()


    mysql.connection.commit()
    return render_template('profile/update_password.html')

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
    card = cursor.fetchall()

    cursor.execute('''SELECT users_has_card.userEmail, users_has_card.cardID, cardNumber, cardExpDate, cardType, cardSVC FROM card JOIN users_has_card ON card.cardID = users_has_card.cardID JOIN users ON users.userEmail = users_has_card.userEmail;''')
    cardDropdown = cursor.fetchall()

    if request.method == "POST":
        # select edCard contains the the card the user selects from dropdown
        selectedCard = request.form.get('cardSelected')
        if (selectedCard is None or selectedCard == ""):
            selectedCard = cardDropdown[0]
    else:
        selectedCard = cardDropdown[0]


    mysql.connection.commit()
    return render_template('profile/update_card.html', details=information[0], add=address, card=card, cardDropdown=cardDropdown, selectedCard=selectedCard)

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
    card = cursor.fetchall()

    cursor.execute('''SELECT users_has_card.userEmail, users_has_card.cardID, cardNumber, cardExpDate, cardType, cardSVC FROM card JOIN users_has_card ON card.cardID = users_has_card.cardID JOIN users ON users.userEmail = users_has_card.userEmail;''')
    cardDropdown = cursor.fetchall()

    if request.method == "POST":
        # select edCard contains the the card the user selects from dropdown
        selectedCard = request.form.get('cardSelected')
        if (selectedCard is None or selectedCard == ""):
            selectedCard = cardDropdown[0]
    else:
        selectedCard = cardDropdown[0]

    mysql.connection.commit()
    return render_template('profile/create_card.html', details=information[0], add=address, card=card, cardDropdown=cardDropdown, selectedCard=selectedCard)

@app.route('/profile/edit')
@login_required
def edit_profile():
    return render_template('profile/edit_profile.html')
