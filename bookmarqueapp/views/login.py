from flask import Flask, redirect, request, render_template, url_for
from flask import session
from flask_mysqldb import MySQL #Mysql
from flask_login import LoginManager, current_user, login_user, logout_user, login_required #Logins
from datetime import timedelta
import time

from bookmarqueapp import app, mysql, login_manager
from bookmarqueapp.models.models import User

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
            email_server.send_email(html_message, subject, email, DEBUG_MODE)

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
        print('remember = ' + str(remember))
        print(user_email)
        print(supplied_password)
        cursor = mysql.connection.cursor()
        cursor.execute('''SELECT userID FROM users WHERE userEmail LIKE %s;''', [user_email])
        user_id = cursor.fetchone()

        if user_id: # if the query returns anything
            user = load_user(user_id = user_id)
            # Use the user returned from load_user above to compare password from the form
            #if user not found = email not found
            #if password is incorrect = wrong password
            if user and supplied_password == user.password:
                # The function below allows you to use current_user to reference the user's session variables.
                login_user(user, force=True, remember=remember)
                user.is_authenticated = True
                print(user.is_authenticated)
                return redirect(url_for('profile'))

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

            message = MIMEMultipart()
            message["From"] = gmail_server_user
            #For testing emails, I am sending emails to our email account, this should be changed to a variable which contains our user's email.
            test_address = "projdeploy@gmail.com"
            #replace test_address with user_email for deployment
            message["To"] = test_address
            message["Subject"] = "Reset Password"
            msgAlternative = MIMEMultipart('alternative')
            #Inline html, which could be replaced with larger template files if needed
            msgText = MIMEText(html_message, 'html', 'utf-8')
            msgAlternative.attach(msgText)
            message.attach(msgAlternative)
            print("Send out an email here")
            text = message.as_string()
            print(text)
            server.sendmail(gmail_server_user, test_address, text)
        return redirect('/')

@app.route('/reset-password/<email_encrypted>', methods=['POST', 'GET'])
def reset_password(email_encrypted):
    #### unencrypt param here ####
    if request.method == 'POST':
        print(str(email_encrypted))
        email = email_encrypted # definitely not secure but hopefully works

        password = request.form.get('password')
        passConfirm = request.form.get('passConfirm') # used to check if password is same in both fields
        submit = request.form.get('Save')
        if (password is None or password == ""):
            password = 'password'
        if (submit is None):
            submit = "Cancel"
        if (submit == "Save" and password == passConfirm and len(password) >= 8):
            cursor = mysql.connection.cursor()
            cursor.execute('''UPDATE users SET userPassword = %s WHERE userEmail = %s;''', ([password], [email]))
            mysql.connection.commit()
        return render_template('index.html')
    if request.method == 'GET':
        return render_template('login/reset_password.html', email_encrypted=email_encrypted)

@app.route('/verify/<email_encrypted>')
def verify_email(email_encrypted):
    #### unencrypt param here ####
    print(str(email_encrypted))
    email = email_encrypted # definitely not secure but hopefully works
    cursor = mysql.connection.cursor()
    cursor.execute('''UPDATE users SET UserStatus = "Active" WHERE userEmail=%s;''', [email])
    mysql.connection.commit()
    return render_template('login/email_confirmation.html')

#This function shoud be called when a user is first logging in.
#Also, it's inherently called for every single page, so when you access current_user.fname, it will always be what was in the DB when you first loaded the page
@login_manager.user_loader
def load_user(user_id):
    cursor = mysql.connection.cursor()
    cursor.execute('''SELECT * FROM users WHERE userID = %s;''', (user_id,))
    information = cursor.fetchall()
    print(information)
    mysql.connection.commit()
    user = User(information[0][0], information[0][1], information[0][6], information[0][2], information[0][3])
    # SQL to return an instance of information pertaining to a user from DB
    return user;

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('homepage'))

# action taken on trying to access a page that needs a login
@login_manager.unauthorized_handler
def unauthorized_callback():
    return render_template('login/login_message.html')


# mainly for testing remember me, session inactivity for 5 seconds will result in logout
# by default sessions are permenantly active for 31 days so need to manually adjust
@app.before_request
def before_request():
    session.permanent = True
    app.permanent_session_lifetime = timedelta(seconds=5)
