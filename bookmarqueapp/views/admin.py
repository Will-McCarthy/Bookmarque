from flask import Flask, redirect, request, render_template, url_for
from flask_mysqldb import MySQL #Mysql
from flask_login import LoginManager, current_user, login_user, logout_user, login_required #Logins
from functools import wraps

from bookmarqueapp import app, mysql
from bookmarqueapp.models.users import User, UserType

# custom decorator for validating user access level
# takes a variadic number of UserType enums
def restrict_access(*user_types):
    def decorator(fn):
        @wraps(fn)
        def can_access(*args, **kwargs):
            for type in user_types:
                if current_user.type == type.value:
                    print('access granted')
                    return fn(*args, **kwargs)
            print('access denied')
            return redirect(url_for('homepage'))
        return can_access
    return decorator

@app.route('/admin')
@login_required
@restrict_access(UserType.ADMIN)
def admin():
    return render_template('admin/admin_view.html')

@app.route('/admin/manage-books', methods = ['POST', 'GET'])
@login_required
@restrict_access(UserType.ADMIN)
def manageBooks():
    cursor = mysql.connection.cursor()
    if request.method == 'POST':
        check = True
        ISBN = request.form.get('ISBN')
        if (ISBN is None or ISBN == "" or len(ISBN) > 13 or len(ISBN) < 13):
            check = False
        bookTitle = request.form.get('title')
        if (bookTitle == ""):
            check = False

        author = request.form.get('author')
        if (author != ""):
            author = author.split();
            for x in author:
                if (x is None):
                    x = ""
        else:
            check = False

        publisher = request.form.get('publisher')
        if (publisher is None):
            publisher = ""
        
        pubDate = request.form.get('pubDate')
        if (pubDate is None):
            pubDate = "1971-01-01"
        
        price = request.form.get('price')
        if (price == ""):
            check = False

        copies = request.form.get('copies')
        if (copies == "" or copies is None):
            copies = 1
            
        subject = request.form.get('subject')
        if (subject == ""):
            check = False
        
        if check and subject is not None:
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
                if (subject is not None):
                    subject = subject[0]
                    cursor.execute('''INSERT INTO book_has_book_categories (ISBN, categoryID) VALUES (%s, %s);''', (ISBN, [subject]))

        if check and len(author) > 1:
            cursor.execute('''INSERT INTO book (ISBN, bookTitle, authorFName, authorLName, bookQuantity, bookPublisher, bookPublicationDate, bookPrice) VALUES (%s, %s, %s, %s, %s, %s, %s, %s);''', (ISBN, bookTitle, author[0], author[1], [copies], publisher, pubDate, [price]))
        elif check:
            cursor.execute('''INSERT INTO book (ISBN, bookTitle, authorLName, bookQuantity, bookPublisher, bookPublicationDate, bookPrice) VALUES (%s, %s, %s, %s, %s, %s, %s);''', (ISBN, bookTitle, author[0], [copies], publisher, pubDate, [price]))

        mysql.connection.commit()
        return redirect(url_for('manageBooks'))

    cursor.execute('''SELECT book.ISBN, bookTitle, CONCAT(authorFName, " ", authorLName) AS authorName, bookPublisher, bookPublicationDate, group_concat(categoryName) AS categories, bookPrice, bookQuantity FROM book JOIN book_has_book_categories ON book.ISBN = book_has_book_categories.ISBN JOIN book_categories ON book_has_book_categories.categoryID = book_categories.categoryID GROUP BY ISBN;''')
    bookData = cursor.fetchall()
    mysql.connection.commit()
    return render_template('admin/manage_books.html', bookData = bookData)

@app.route('/admin/manage-books/book-entry')
@login_required
@restrict_access(UserType.ADMIN)
def bookEntry():
    return render_template('admin/book_entry.html')

@app.route('/admin/manage-users', methods=['POST', 'GET'])
@login_required
@restrict_access(UserType.ADMIN)
def manageUsers():
    if request.method == 'POST':
        #user_id = request.form.get('id')
        print('posted here')
        id = request.form.get('id')
        status = request.form.get('status')
        status = 'Active' if (status == 'Suspended') else 'Suspended'
        cursor = mysql.connection.cursor()
        cursor.execute('UPDATE users SET userStatus="' + status + '" WHERE userID=' + id)
        mysql.connection.commit()

    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM users')
    user_fetch = cursor.fetchall()
    return render_template('admin/manage_users.html', users = user_fetch)

# @app.route('/admin/manage-users/user-entry')
# @login_required
# @restrict_access(UserType.ADMIN)
# def userEntry():
#     return render_template('admin/user_entry.html')

@app.route('/admin/manage-promotions', methods=['POST','GET'])
@login_required
@restrict_access(UserType.ADMIN)
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
        return render_template('admin/manage_promotions.html', promotions = promotion_fetch)
