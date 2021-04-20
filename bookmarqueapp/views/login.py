from flask import Flask, redirect, request, render_template, url_for
from flask import session
from flask_login import LoginManager, current_user, login_user, logout_user, login_required #Logins
from datetime import timedelta
import time

from bookmarqueapp import app, db, login_manager, email_server
from bookmarqueapp.models.users import User, UserType, UserStatus, UserFactory, Address
from bookmarqueapp.models.payment import PaymentCard, CardType

# registration and login #
@app.route('/register', methods=['POST'])
def register_user():
    if request.method == 'POST':

        # get information from form
        # pull hidden input value for url which called '/register'
        next_url = request.form.get('next')
        email = request.form.get('email')

        # If this exists, then we know the above sql statement returned an object matching the email
        if not User.query.filter_by(userEmail=email).first():

            # user information
            first_name = request.form.get('fName')
            last_name = request.form.get('lName')
            password = request.form.get('password')
            phone = request.form.get('phone')

            user = User(userEmail=email, userFName=first_name,
                        userLName=last_name, userPhone=phone)

            user.password = password # set and encrypt

            # hard coded values
            user.set_subscription(False)
            user.set_status(UserStatus.INACTIVE)
            user.set_type(UserType.CUSTOMER)

            # if we have payment information add to the database and associate with user
            if (request.form.get('payment-skipped') == 'false'):
                card_type = request.form.get('cardType')
                card_number = request.form.get('cardNumber')
                exp_month = request.form.get('expMonth')
                exp_year = request.form.get('expYear')
                svc = request.form.get('svc')
                exp_date = str(exp_year) + str(exp_month) + "01" # into datetime format

                card = PaymentCard(cardNumber=card_number, cardExpDate=exp_date,
                                    cardType=card_type, cardSVC=svc)
                user.cards.append(card)

            # if we have shipping information add to the database and associate with user
            if (request.form.get('shipping-skipped') == 'false'):
                street = request.form.get('address')
                city = request.form.get('city')
                state = request.form.get('state')
                zip = request.form.get('zip')

                address = Address(addressStreet=street, addressCity=city,
                    addressState=state, addressZip=zip)
                user.address = address

            db.session.add(user)
            db.session.commit()

            # send email with link in form of /verify/ + user_id
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
            if (user.check_password(supplied_password)): # verify password
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
        email = request.form.get('email')
        user = User.query.filter_by(userEmail=email).first()

        if user:
            # send email with link in form of /verify/ + user_id
            reset_password_link = url_for('reset_password', email_encrypted = email, _external=True)
            print(reset_password_link)
            html_message = '''
                <h1>Reset Password Here:</h1>
                <span>Click this <a href="''' + reset_password_link + '''">link</a> to reset password. If this was not you, ignore this message.</span>
            '''
            subject = "Reset Password"
            email_server.send_email(html_message, subject, email, app.debug)

        return redirect(url_for('homepage'))

@app.route('/reset-password/<email_encrypted>', methods=['POST', 'GET'])
def reset_password(email_encrypted):
    if request.method == 'POST':
        email = email_encrypted # definitely not secure but hopefully works
        password = request.form.get('password')
        passConfirm = request.form.get('passConfirm') # used to check if password is same in both fields

        if password:
            user = User.query.filter_by(userEmail=email).first()
            if user:
                user.password = password
                db.session.commit()

        return render_template('index.html')

    if request.method == 'GET':

        # check link is valid by seeing if email is real
        email = email_encrypted
        user = User.query.filter_by(userEmail=email).first()

        if user: # if query returned someone with that email
            return render_template('login/reset_password.html', email_encrypted=email_encrypted)
        else:
            return redirect(url_for('homepage'))

@app.route('/verify/<email_encrypted>')
def verify_email(email_encrypted):

    email = email_encrypted # definitely not secure but hopefully works
    user = User.query.filter_by(userEmail=email).first()
    if user:
        user.set_status(UserStatus.ACTIVE)
        db.session.commit()
        return render_template('login/messages/email_confirmation.html')
    else:
        return redirect(url_for('homepage'))

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
