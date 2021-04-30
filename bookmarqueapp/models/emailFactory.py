from flask import Flask, redirect, request, render_template, url_for
from flask import session
from flask_mysqldb import MySQL #Mysql
from flask_login import LoginManager, current_user, login_user, logout_user, login_required #Logins
from datetime import timedelta
import time

import enum
from sqlalchemy.ext.hybrid import hybrid_property

from bookmarqueapp import app, db, login_manager, email_server, mysql
from bookmarqueapp.models.users import User, UserType, UserStatus, UserFactory, Address
from bookmarqueapp.models.payment import PaymentCard, CardType



class EmailFactory:
    def email(self, userID):
        pass


#Requirement for email construction:
# - User ID     for emailing to email with link
# - Verified and works
class ForgotPasswordEmailFactory(EmailFactory):
    def email(self, userID):
        #Pull email from user_id here
        user = User.query.filter_by(userID=userID).first()
        email = user.userEmail

        reset_password_link = url_for('reset_password', email_encrypted = email, _external=True)
        print(reset_password_link)
        subject = "Reset Password"
        html_message = '''
            <h1>Reset Password Here:</h1>
            <span>Click this <a href="''' + reset_password_link + '''">link</a> to reset password. If this was not you, ignore this message.</span>
        '''
        email_server.send_email(html_message, subject, email, app.debug)



#Requirement for email construction:
# - User ID     for emailing to email with link
# - Verified and works
class VerifyAccountEmailFactory(EmailFactory):
    def email(self, userID):
        #Pull email from user_id here
        user = User.query.filter_by(userID=userID).first()
        email = user.userEmail

        # send email with link in form of /verify/ + user_id
        verification_link = url_for('verify_email', email_encrypted = email, _external=True)
        print(verification_link)
        subject = "Confirm Email"
        html_message = '''
            <h1>Please Confirm Your Email</h1>
            <span>Click this <a href="''' + str(verification_link) + '''">link</a> or if this was not you, ignore this message.</span>
        '''
        email_server.send_email(html_message, subject, email, app.debug)

#Requirement for email construction:
# - User ID     for recipient name/email
# - Order Info  All of the books in a given order
# - total       total cost
# - shipping    shipping price
# - promo_code  promo code ID
# - promo_success   if there is a promo code
class OrderSummaryEmailFactory(EmailFactory):
    def __init__(self):
        self.orderID = 0
    def email(self, userID, orderInfo, total, shipping, promo_code, promo_success, merchandise):
        user = User.query.filter_by(userID=userID).first()
        email = user.userEmail

        subject = "Order Summary"
        html_message = render_template('checkout/order_summary.html', orderInfo = orderInfo, total=total, shipping=shipping, promo_discount=promo_code, promo_success=promo_success, merchandise=merchandise )
        email_server.send_email(html_message, subject, email, app.debug)

#Requirement for email construction:
# - Promotion ID for promotion information
# - User ID      for recipient name/email
# - Verified and works
class PromotionEmailFactory(EmailFactory):
    def __init__(self):
        self.promoID = 0

    def setPromoID(self, promoID):
        self.promoID = promoID

    def email(self, userID):
        #Pull email from user_id here
        user = User.query.filter_by(userID=userID).first()
        email = user.userEmail

        #Pull promotion information from promoID here
        cursor = mysql.connection.cursor()
        cursor.execute('''SELECT * FROM promotion WHERE promoID = ''' + str(self.promoID))
        count = cursor.fetchone()
        mysql.connection.commit()
        promo_discount = count[1]
        promo_end = count[3]
        promo_name =  count[6]
        promo_code = count[7]

        subject = "Save " + str(float(promo_discount)*100) + "% at Bookmarque today for our " + promo_name
        html_message =  '''
            <h2> Bookmarque discount </h2>
            <hr>
            <p> For a limited time, you can save ''' + str(float(promo_discount)*100) + '''
            %. This promotion expires on ''' + str(promo_end) + '''</p>
            <br><br>
            <p> Use ''' + promo_code + ''' at checkout to save today! </p>
        '''
        email_server.send_email(html_message, subject, email, app.debug)

#Requirement for email construction:
# - User ID      for recipient name/email
# - Verified and works
class PasswordUpdateEmailFactory(EmailFactory):
    def email(self, userID):
        #Pull email from user_id here
        user = User.query.filter_by(userID=userID).first()
        email = user.userEmail

        subject = "Your password has been changed"
        message = '''
            <h2>Your password has been changed. </h2>
            <br>
            <p> Your password has been changed, as you asked. </p>
            <br>
            <p> If you didn’t ask to change your password, we’re here to help keep your account secure. Visit our support page for more info. </p>
        '''
        email_server.send_email(message, subject, current_user.userEmail, app.debug)
