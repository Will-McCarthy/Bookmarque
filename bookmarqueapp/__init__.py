from flask import Flask
from flask import render_template # for file extends
from flask import redirect
from flask import request
from flask import url_for
from flask_mysqldb import MySQL
from sassutils.wsgi import SassMiddleware # for sass/scss compilation
from . import config as cfg # for loading in db configurations


app = Flask(__name__)
app.config['MYSQL_HOST'] = cfg.mysql["host"]
app.config['MYSQL_USER'] = cfg.mysql["user"]
app.config['MYSQL_PASSWORD'] = cfg.mysql["password"]
app.config['MYSQL_DB'] = cfg.mysql["db"]
mysql = MySQL(app)
# configure directory locations for Sass/SCSS
app.wsgi_app = SassMiddleware(app.wsgi_app, {
    'bookmarqueapp': ('static/sass', 'static/css', '/static/css')
})

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

@app.route('/manage-books')
def manageBooks():
    return render_template('manage_books.html')


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

@app.route('/manage-books/book-entry')
def bookEntry():
    return render_template('book_entry.html')

@app.route('/cart')
def shopping_cart():
    return render_template('shopping_cart.html')

@app.route('/cart/history')
def order_history():
    return render_template('order_history.html')

@app.route('/profile', methods = ['POST', 'GET'])
def profile():
    cursor = mysql.connection.cursor()
    cursor.execute('''SELECT * FROM users WHERE userID = '101';''')
    information = cursor.fetchall()
    cursor.execute('''SELECT addressStreet, addressCity, addressState, addressZip FROM users JOIN address ON users.addressID = address.addressID WHERE userID = "101";''')
    address = cursor.fetchall()
    cursor.execute('''SELECT userEmail FROM users WHERE userID = "101";''')
    email = cursor.fetchone()
    email = email[0]
    cursor.execute('''SELECT MIN(users_has_card.cardID), cardNumber, cardExpDate, cardType, cardSVC FROM users_has_card JOIN card ON card.cardID = users_has_card.cardID WHERE userEmail = %s;''', [email])
    card = cursor.fetchall()
    initCard = card[0]
    initial = information[0]
    initAdd = address[0]
    if request.method == 'POST':

        fName = request.form.get('fName')
        if (fName is None or fName == ""):
            fName = initial[2]

        lName = request.form.get('lName')
        if (lName is None or lName == ""):
            lName = initial[3]

        address = request.form.get('address')
        if (address is None or address == ""):
            address = initAdd[0]

        phone = request.form.get('phone')
        if (phone is None or phone == ""):
            phone = initial[7]

        city = request.form.get('city')
        if (city is None or city == ""):
            city = initAdd[1]

        state = request.form.get('state')
        if (state is None or state == ""):
            state = initAdd[2]

        zipCode = request.form.get('zip')
        if (zipCode is None or zipCode == ""):
            zipCode = initAdd[3]

        # handles update_password form
        password = request.form.get('password')
        if (password is None or password == ""):
            password = initial[6]
        passConfirm = request.form.get('passConfirm') # used to check if password is same in both fields
        submit = request.form.get('Save')
        if (submit is None):
            submit = "Cancel"
        if (submit == "Save" and password == passConfirm):
            cursor.execute('''UPDATE users SET userPassword = %s WHERE userID = "101";''', [password])

        # handles update_card form and create_card form
        cardList = request.form.get('cardList')
        if (cardList is None or cardList == ""):
            cardList = initCard[3]

        cardNumber = request.form.get('cardNumber')
        if (cardNumber is None or cardNumber == ""):
            cardNumber = initCard[1]

        monthList = request.form.get('monthList')

        yearList = request.form.get('yearList')

        SVC = request.form.get('SVC')
        if (SVC is None or SVC == ""):
            SVC = initCard[4]

        # confirm is for update card
        confirm = request.form.get("saveCard")
        print(confirm)
        if (confirm is None):
            confirm = "Cancel"
        if (confirm == "Save"):
            cursor.execute('''UPDATE card JOIN users_has_card ON card.cardID = users_has_card.cardID JOIN users ON users.userEmail = users_has_card.userEmail JOIN (SELECT MIN(cardID) AS min FROM users_has_card ) AS min ON min.min = users_has_card.cardID SET cardType = %s, cardNumber = %s, cardSVC = %s WHERE users_has_card.userEmail = %s;''', (cardList, cardNumber, [SVC], email))

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
            cursor.execute('''INSERT INTO card (cardID, cardNumber, cardType, cardSVC) VALUES (%s, %s, %s, %s);''', ([cardValue], cardNumber, cardList, SVC))
            cursor.execute('''INSERT INTO users_has_card (userEmail, cardID) VALUES (%s, %s);''', (email, [cardValue]))

        status = request.form.get('status')
        password = request.form.get('password')
        if (status is None and password is None): #not on update_password and status is unchecked
            status = "Deactive"
        else:
            status = initial[8]

        #ensures addresses have unique ids
        cursor.execute('''SELECT MAX(addressID) FROM address;''');
        value = cursor.fetchone()
        addressValue = value[0]
        addressValue += 1

        if (status == "Active"): # subscription for promos is checked
            cursor.execute('''UPDATE users SET userFName = %s, userLName = %s, userPhone = %s, userSubStatus = %s WHERE userID = "101";''', (fName, lName, phone, status))
        else: # subcription for promos is not checked
            cursor.execute('''UPDATE users SET userFName = %s, userLName = %s, userPhone = %s, userSubStatus = "Deactive" WHERE userID = "101";''', (fName, lName, phone))

        cursor.execute('''SELECT addressID FROM users WHERE userID = "101";''')
        checkValue = cursor.fetchone()
        check = checkValue[0]
        #print(check is None)
        if (password is None and check is None): # not on update_password form and there is no existing address associated
            print(addressValue)
            cursor.execute('''INSERT INTO address (addressID, addressStreet, addressCity, addressState, addressZip) VALUES (%s, %s, %s, %s, %s);''', ([addressValue], address, city, state, zipCode))
            cursor.execute('''UPDATE users SET addressID = %s WHERE userID = "101";''', [addressValue])
        else:
            cursor.execute('''UPDATE address JOIN users ON users.addressID = address.addressID SET addressStreet = %s, addressCity = %s, addressState = %s, addressZip = %s WHERE users.userID = "101";''', (address, city, state, zipCode))
        mysql.connection.commit()

    cursor.execute('''SELECT * FROM users WHERE userID = '101';''')
    information = cursor.fetchall()
    cursor.execute('''SELECT addressStreet, addressCity, addressState, addressZip FROM users JOIN address ON users.addressID = address.addressID WHERE userID = "101";''')
    address = cursor.fetchall()
    cursor.execute('''SELECT userEmail FROM users WHERE userID = "101";''')
    email = cursor.fetchone()
    email = email[0]
    cursor.execute('''SELECT MIN(users_has_card.cardID), cardNumber, cardExpDate, cardType, cardSVC FROM users_has_card JOIN card ON card.cardID = users_has_card.cardID WHERE userEmail = %s;''', [email])
    card = cursor.fetchall()
    mysql.connection.commit()
    return render_template('profile.html', details=information[0], add=address[0], card=card[0])
    #return render_template('profile.html')

@app.route('/profile/update-password')
def password_panel():
    cursor = mysql.connection.cursor()
    cursor.execute('''SELECT * FROM users WHERE userID = '101';''')
    information = cursor.fetchall()
    cursor.execute('''SELECT addressStreet, addressCity, addressState, addressZip FROM users JOIN address ON users.addressID = address.addressID WHERE userID = "101";''')
    address = cursor.fetchall()
    cursor.execute('''SELECT userEmail FROM users WHERE userID = "101";''')
    email = cursor.fetchone()
    email = email[0]
    cursor.execute('''SELECT MIN(users_has_card.cardID), cardNumber, cardExpDate, cardType, cardSVC FROM users_has_card JOIN card ON card.cardID = users_has_card.cardID WHERE userEmail = %s;''', [email])
    card = cursor.fetchall()
    mysql.connection.commit()
    return render_template('update_password.html', details=information[0], add=address[0], card=card[0])

@app.route('/profile/update-card')
def card_panel():
    cursor = mysql.connection.cursor()
    cursor.execute('''SELECT * FROM users WHERE userID = '101';''')
    information = cursor.fetchall()
    cursor.execute('''SELECT addressStreet, addressCity, addressState, addressZip FROM users JOIN address ON users.addressID = address.addressID WHERE userID = "101";''')
    address = cursor.fetchall()
    cursor.execute('''SELECT userEmail FROM users WHERE userID = "101";''')
    email = cursor.fetchone()
    email = email[0]
    cursor.execute('''SELECT MIN(users_has_card.cardID), cardNumber, cardExpDate, cardType, cardSVC FROM users_has_card JOIN card ON card.cardID = users_has_card.cardID WHERE userEmail = %s;''', [email])
    card = cursor.fetchall()
    mysql.connection.commit()
    return render_template('update_card.html', details=information[0], add=address[0], card=card[0])

@app.route('/profile/create-card')
def card_panel_2():
    cursor = mysql.connection.cursor()
    cursor.execute('''SELECT * FROM users WHERE userID = '101';''')
    information = cursor.fetchall()
    cursor.execute('''SELECT addressStreet, addressCity, addressState, addressZip FROM users JOIN address ON users.addressID = address.addressID WHERE userID = "101";''')
    address = cursor.fetchall()
    cursor.execute('''SELECT userEmail FROM users WHERE userID = "101";''')
    email = cursor.fetchone()
    email = email[0]
    cursor.execute('''SELECT MIN(users_has_card.cardID), cardNumber, cardExpDate, cardType, cardSVC FROM users_has_card JOIN card ON card.cardID = users_has_card.cardID WHERE userEmail = %s;''', [email])
    card = cursor.fetchall()
    mysql.connection.commit()
    return render_template('create_card.html', details=information[0], add=address[0], card=card[0])

@app.route('/profile/edit')
def edit_profile():
    return render_template('edit_profile.html')

# registration and login #
@app.route('/register', methods=['POST'])
def register_user():
    if request.method == 'POST':

        # pull hidden input value for url which called /register
        next_url = request.form.get("next")

        # if url exists redirect user to the page they were on
        if next_url:
            return redirect(next_url)

    return redirect('/') # if all else fails go to the homepage

@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        print('login')
    else:
        print('do not login')

    return redirect('/')
