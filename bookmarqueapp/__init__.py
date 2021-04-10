from flask import Flask
from flask import render_template # for file extends
from flask import redirect
from flask import request
from flask import url_for
from flask import session
from flask_mysqldb import MySQL #Mysql
from flask_login import LoginManager, current_user, login_user, logout_user, login_required #Logins
from sassutils.wsgi import SassMiddleware # for sass/scss compilation
from datetime import timedelta
import time

# custom imports
from . import config as cfg # for loading in custom configuration information
from . import email_server # setup of email server and associated functions
from . models import User, UserStatus

DEBUG_MODE = True # changes whether certain tests are run

app = Flask(__name__)
app.config['MYSQL_HOST'] = cfg.mysql["host"]
app.config['MYSQL_USER'] = cfg.mysql["user"]
app.config['MYSQL_PASSWORD'] = cfg.mysql["password"]
app.config['MYSQL_DB'] = cfg.mysql["db"]

#Login initialization
#Example secret key, probably should be changed.
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app)


mysql = MySQL(app)
# configure directory locations for Sass/SCSS
app.wsgi_app = SassMiddleware(app.wsgi_app, {
    'bookmarqueapp': ('static/sass', 'static/css', '/static/css')
})

# mainly for testing remember me, session inactivity for 5 seconds will result in logout
# by default sessions are permenantly active for 31 days so need to manually adjust
@app.before_request
def before_request():
    session.permanent = True
    app.permanent_session_lifetime = timedelta(seconds=5)

# action taken on trying to access a page that needs a login
@login_manager.unauthorized_handler
def unauthorized_callback():
    return render_template('login_message.html')

@app.route('/mysqltest')
def test():
    cursor = mysql.connection.cursor()
    cursor.execute('''SELECT * FROM book;''')
    rv = cursor.fetchall()
    print(rv)
    #cursor.execute(''' INSERT INTO info_table VALUES(%s,%s)''',(name,age))
    mysql.connection.commit()
    return render_template('index.html')

@app.route('/')
def homepage():
    cursor = mysql.connection.cursor()
    cursor.execute('''SELECT * FROM book, book_has_book_categories WHERE book.ISBN = book_has_book_categories.ISBN AND categoryID = '1' LIMIT 4;''')
    featured = cursor.fetchall()
    cursor.execute('''SELECT * FROM book, book_has_book_categories WHERE book.ISBN = book_has_book_categories.ISBN AND categoryID = '18' LIMIT 4;''')
    newly_released = cursor.fetchall()
    mysql.connection.commit()
    #print(str(current_user.id) + " " + current_user.lname)
    return render_template('index.html', featured=featured, newly_released=newly_released)

@app.route('/search/')
def search():
    return render_template('search_view.html')

@app.route('/view/<ISBN>')
def book_details(ISBN):
    print(str(ISBN))
    cursor = mysql.connection.cursor()
    cursor.execute('''SELECT * FROM book WHERE book.ISBN = ''' + str(ISBN)+ ''';''')
    fetch = cursor.fetchall()
    cursor.execute('''SELECT book_categories.categoryName FROM book_has_book_categories, book_categories WHERE book_has_book_categories.ISBN = ''' + str(ISBN)+ ''' AND book_has_book_categories.categoryID = book_categories.categoryID;''')
    tag_fetch = cursor.fetchall()
    mysql.connection.commit()
    return render_template('book_details_example.html', data=fetch[0],tags=list(tag_fetch))

@app.route('/admin')
def admin():
    return render_template('admin_view.html')

@app.route('/manage-promotions')
def managePromotions():
    return render_template('manage_promotions.html')

@app.route('/manage-books', methods = ['POST', 'GET'])
def manageBooks():
    cursor = mysql.connection.cursor()
    if request.method == 'POST':
        ISBN = request.form.get('ISBN')

        bookTitle = request.form.get('title')

        author = request.form.get('author')
        if (author != None):
            author = author.split();

        subject = request.form.get('subject')
        if (subject != None):
            if (',' in subject):
                subject = subject.split(',')
                for x in subject:
                    cursor.execute('''SELECT categoryID FROM book_categories WHERE categoryName = %s;''', [x]);
                    x = cursor.fetchone()
                    x = x[0]
                    cursor.execute('''INSERT INTO book_has_book_categories (ISBN, categoryID) VALUES (%s, %s);''', (ISBN, [x]))
            else:
                cursor.execute('''SELECT categoryID FROM book_categories WHERE categoryName = %s;''', [subject]);
                subject = cursor.fetchone()
                subject = subject[0]
                cursor.execute('''INSERT INTO book_has_book_categories (ISBN, categoryID) VALUES (%s, %s);''', (ISBN, [subject]))

        copies = request.form.get('copies')

        cursor.execute('''INSERT INTO book (ISBN, bookTitle, authorFName, authorLName, bookQuantity) VALUES (%s, %s, %s, %s, %s);''', (ISBN, bookTitle, author[0], author[1], [copies]))

        mysql.connection.commit()
        return redirect(url_for('manageBooks'))

    cursor.execute('''SELECT book.ISBN, bookTitle, CONCAT(authorFName, " ", authorLName) AS authorName, group_concat(categoryName) AS categories, bookQuantity FROM book JOIN book_has_book_categories ON book.ISBN = book_has_book_categories.ISBN JOIN book_categories ON book_has_book_categories.categoryID = book_categories.categoryID GROUP BY ISBN;''')
    bookData = cursor.fetchall()
    mysql.connection.commit()
    return render_template('manage_books.html', bookData = bookData)

@app.route('/manage-books/book-entry')
def bookEntry():
    return render_template('book_entry.html')

@app.route('/manage-users')
def manageUsers():
    return render_template('manage_users.html')

@app.route('/manage-users/user-entry')
def userEntry():
    return render_template('user_entry.html')

@app.route('/manage-promotions', methods=['POST','GET'])
def managePromotions():
    print("Something triggered promotion route")
    if request.method == 'POST':
        print("We're in post!")
        promo_name = request.form.get('name')
        promo_discount = request.form.get('discount')
        #promo_start and promo_end should come in as YYYY-MM-DD, maybe we use a calender html assistance.
        promo_start = request.form['start']
        promo_end = request.form['end']
        cursor = mysql.connection.cursor()
        promo_code = request.form['code']
        cursor.execute('''INSERT INTO promotion(promoDiscount, promoStart, promoEnd, promoEmailStatus, promoUses, promoName,promoCode) VALUES (%s,%s,%s,%s,%s,%s,%s)''', (promo_discount, promo_start, promo_end, "Not Sent", 0, promo_name,promo_code))
        promotion_fetch = cursor.fetchall()
        mysql.connection.commit()
        return redirect(url_for('managePromotions'))
    else:
        cursor = mysql.connection.cursor()
        cursor.execute('''SELECT * FROM promotion;''')
        promotion_fetch = cursor.fetchall()
        mysql.connection.commit()
        return render_template('manage_promotions.html', promotions = promotion_fetch)

@app.route('/checkout1')
def checkout1():
    return render_template('checkout1.html')

@app.route('/checkout2')
def checkout2():
    return render_template('checkout2.html')

@app.route('/checkout3')
def checkout3():
    return render_template('checkout3.html')

@app.route('/checkout4')
def checkout4():
    return render_template('checkout4.html')

@app.route('/checkout5')
def checkout5():
    return render_template('checkout5.html')

@app.route('/checkout6')
def checkout6():
    return render_template('checkout6.html')

@app.route('/cart')
def shopping_cart():
    return render_template('shopping_cart.html')

@app.route('/cart/history')
def order_history():
    return render_template('order_history.html')

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

    print(information[0][0])
    print(address)
    print(card)
    return render_template('profile.html', details=information[0], add=address, card=card, cardDropdown=cardDropdown, selectedCard=selectedCard)
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


    cursor.execute('''SELECT users_has_card.userEmail, users_has_card.cardID, cardNumber, cardExpDate, cardType, cardSVC FROM card JOIN users_has_card ON card.cardID = users_has_card.cardID JOIN users ON users.userEmail = users_has_card.userEmail;''')
    cardDropdown = cursor.fetchall()

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
    return render_template('update_password.html', details=information[0], add=address, card=card, cardDropdown=cardDropdown, selectedCard=selectedCard)

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
    return render_template('update_card.html', details=information[0], add=address, card=card, cardDropdown=cardDropdown, selectedCard=selectedCard)

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
    return render_template('create_card.html', details=information[0], add=address, card=card, cardDropdown=cardDropdown, selectedCard=selectedCard)

@app.route('/profile/edit')
@login_required
def edit_profile():
    return render_template('edit_profile.html')

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
        return render_template('reset_password.html', email_encrypted=email_encrypted)

@app.route('/verify/<email_encrypted>')
def verify_email(email_encrypted):
    #### unencrypt param here ####
    print(str(email_encrypted))
    email = email_encrypted # definitely not secure but hopefully works
    cursor = mysql.connection.cursor()
    cursor.execute('''UPDATE users SET UserStatus = "Active" WHERE userEmail=%s;''', [email])
    mysql.connection.commit()
    return render_template('email_confirmation.html')

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
