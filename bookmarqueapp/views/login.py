from flask import Flask, redirect, request, render_template, url_for
from flask import session
from flask_mysqldb import MySQL #Mysql
from flask_login import LoginManager, current_user, login_user, logout_user, login_required #Logins
from datetime import timedelta
import time

from bookmarqueapp import app, mysql, db, login_manager, email_server
from bookmarqueapp.models.users import User, UserType, UserStatus, UserFactory

# registration and login #
@app.route('/register', methods=['POST'])
def register_user():
    if request.method == 'POST':

        # get information from form
        # pull hidden input value for url which called '/register'
        next_url = request.form.get('next')
        email = request.form.get('email')

        # Check to see if email is taken
        cursor = mysql.connection.cursor()
        cursor.execute('''SELECT userID FROM users WHERE userEmail LIKE %s;''', [email])
        userid = cursor.fetchall()
        mysql.connection.commit()

        # If this exists, then we know the above sql statement returned an object matching the email
        if not userid:
            print(email + " is available")

            # user information
            first_name = request.form.get('fName')
            last_name = request.form.get('lName')
            phone = request.form.get('phone')
            password = request.form.get('password')

            # if we have payment information add to the database and associate with user
            if (request.form.get('payment-skipped') == 'false'):
                card_type = request.form.get('cardType')
                card_number = request.form.get('cardNumber')
                exp_month = request.form.get('expMonth')
                exp_year = request.form.get('expYear')
                svc = request.form.get('svc')

                cursor.execute('''SELECT MAX(cardID) FROM card;''');
                value = cursor.fetchone()
                card_id = value[0]
                card_id += 1

                exp_date = str(exp_year) + str(exp_month) + "01" # into datetime format

                cursor.execute('''INSERT INTO card (cardID, cardNumber, cardType, cardSVC, cardExpDate) VALUES (%s, %s, %s, %s, %s);''', ([card_id], card_number, card_type, svc, exp_date))
                cursor.execute('''INSERT INTO users_has_card (userEmail, cardID) VALUES (%s, %s);''', (email, [card_id]))

            # if we have shipping information add to the database and associate with user
            if (request.form.get('shipping-skipped') == 'false'):
                address = request.form.get('address')
                city = request.form.get('city')
                state = request.form.get('state')
                zip = request.form.get('zip')

                cursor.execute('''SELECT MAX(addressID) FROM address;''');
                value = cursor.fetchone()
                address_id = value[0]
                address_id += 1

                cursor.execute('''INSERT INTO address (addressID, addressStreet, addressCity, addressState, addressZip) VALUES (%s, %s, %s, %s, %s);''', ([address_id], address, city, state, zip))
                cursor.execute('''INSERT INTO users (userEmail, userFName, userLName, userStatus, userType, userPassword, userPhone, addressID) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)''', [email, first_name, last_name, "Inactive", "Customer", password, phone, address_id])
            else:
                cursor.execute('''INSERT INTO users (userEmail, userFName, userLName, userStatus, userType, userPassword, userPhone) VALUES (%s, %s, %s, %s, %s, %s, %s)''', [email, first_name, last_name, "Inactive", "Customer", password, phone])

            mysql.connection.commit()

            # send email with link in form of /verify/ + user_id
            ### encrypt email ###
            verification_link = url_for('verify_email', email_encrypted = email, _external=True)
            print(verification_link)
            html_message = '''
                <h1>Please Confirm Your Email</h1>
                <span>Click this <a href="''' + str(verification_link) + '''">link</a> or if this was not you, ignore this message.</span>
            '''
            subject = "Confirm Email"
            email_server.send_email(html_message, subject, email, app.debug)

        else:
            print(email + " is taken")


        # if url exists redirect user to the page they were on
        if next_url:
            return redirect(next_url)

    return redirect('homepage') # if all else fails go to the homepage

@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        # PULL In Email and password from login form here and insert into sql statement below.
        user_email = request.form.get('email')
        supplied_password = request.form.get('password')
        remember = False if request.form.get('remember-me') is None else True

        # attempt to query user with email from database
        user = User.query.filter_by(userEmail=user_email).first()

        if user: # if the query returns anything
            if (supplied_password == user.userPassword): # verify password
                # verify status is active
                if user.userStatus == UserStatus.SUSPENDED.value:
                    return render_template('login/messages/suspended_account.html')
                elif user.userStatus == UserStatus.INACTIVE.value:
                    return render_template('login/messages/inactive_account.html')
                login_user(user, force=True, remember=remember) # allows current_user access to user session variables
                user.is_authenticated = True
                return redirect(url_for('profile'))
            else:
                return render_template('login/messages/invalid_login.html')
        else:
            return render_template('login/messages/invalid_login.html')

    return redirect(url_for('homepage'))

@app.route('/forgot-password', methods=['POST'])
def forgot_password():
    if request.method == 'POST':
        # PULL In Email and password from login form here and insert into sql statement below.
        user_email = request.form.get('email')
        print(user_email)
        cursor = mysql.connection.cursor()
        cursor.execute('''SELECT userEmail FROM users WHERE userEmail LIKE %s;''', [user_email])
        confirmed_email = cursor.fetchone()
        print("found email:")
        print(confirmed_email)

        if confirmed_email != None:
            # send email with link in form of /verify/ + user_id
            ### encrypt email ###
            reset_password_link = url_for('reset_password', email_encrypted = user_email, _external=True)
            print(reset_password_link)
            html_message = '''
                <h1>Reset Password Here:</h1>
                <span>Click this <a href="''' + reset_password_link + '''">link</a> to reset password. If this was not you, ignore this message.</span>
            '''
            subject = "Reset Password"
            email_server.send_email(html_message, subject, confirmed_email, app.debug)

        return redirect('/')

@app.route('/reset-password/<email_encrypted>', methods=['POST', 'GET'])
def reset_password(email_encrypted):
    #### unencrypt param here ####
    if request.method == 'POST':
        print(str(email_encrypted))
        email = email_encrypted # definitely not secure but hopefully works
        password = request.form.get('password')
        passConfirm = request.form.get('passConfirm') # used to check if password is same in both fields

        if password:
            cursor = mysql.connection.cursor()
            cursor.execute('''UPDATE users SET userPassword = %s WHERE userEmail = %s;''', ([password], [email]))
            mysql.connection.commit()
        return render_template('index.html')
    if request.method == 'GET':

        # check link is valid by seeing if email is real
        email = email_encrypted
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM users WHERE userEmail=%s;''', [email])
        user = cursor.fetchall()

        if user: # if query returned someone with that email
            return render_template('login/reset_password.html', email_encrypted=email_encrypted)
        else:
            return redirect(url_for('homepage'))

@app.route('/verify/<email_encrypted>')
def verify_email(email_encrypted):
    #### unencrypt param here ####
    print(str(email_encrypted))
    email = email_encrypted # definitely not secure but hopefully works
    cursor = mysql.connection.cursor()
    cursor.execute('''UPDATE users SET UserStatus = "Active" WHERE userEmail=%s;''', [email])
    mysql.connection.commit()
    return render_template('login/messages/email_confirmation.html')

#This function shoud be called when a user is first logging in.
#Also, it's inherently called for every single page, so when you access current_user.fname, it will always be what was in the DB when you first loaded the page
@login_manager.user_loader
def load_user(user_id):

    uf = UserFactory() # uf allows for getting different user types with separate classes
    try:
        user = uf.get_user(user_id)
    except:
        return redirect(url_for('logout'))
    print(user.userEmail)
    return user # SQL to return an instance of information pertaining to a user from DB

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('homepage'))

# action taken on trying to access a page that needs a login
@login_manager.unauthorized_handler
def unauthorized_callback():
    return render_template('login/messages/login_message.html')


# mainly for testing remember me, session inactivity for 5 seconds will result in logout
# by default sessions are permenantly active for 31 days so need to manually adjust
@app.before_request
def before_request():
    session.permanent = True
    app.permanent_session_lifetime = timedelta(seconds=5)
