from flask import Flask, redirect, request, render_template, url_for
from flask_mysqldb import MySQL #Mysql
from flask_login import LoginManager, current_user, login_user, logout_user, login_required #Logins
from functools import wraps

from bookmarqueapp import app, mysql, email_server
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
    if request.method == 'POST':
        if request.form.get('promoID'):
            #DELETE PROMO BUTTON PRESSED
            promo_ID = request.form.get('promoID')
            print(promo_ID)
            cursor = mysql.connection.cursor()
            cursor.execute('''DELETE FROM promotion WHERE promoID = '''+promo_ID)
            mysql.connection.commit()
            return redirect(url_for('managePromotions'))
        elif request.form.get('name'):
            #ADD PROMO BUTTON PRESSED
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
            #TEST EMAIL, CREATE A PROMOTION/DOESN
            #send_promo_email(promo_name, promo_code, promo_end,promo_discount)
            return redirect(url_for('managePromotions'))
    else:
        cursor = mysql.connection.cursor()
        cursor.execute('''SELECT * FROM promotion;''')
        promotion_fetch = cursor.fetchall()
        mysql.connection.commit()
        return render_template('admin/manage_promotions.html', promotions = promotion_fetch)


def send_promo_email(promo_name, promo_code, promo_end,promo_discount):
    subject = "Save " + str(float(promo_discount)*100) + "% at Bookmarque today for our " + promo_name
    message = " <h2> Bookmarque discount </h2><hr><p> For a limited time, you can save " + str(float(promo_discount)*100) + "%. This promotion expires on " + promo_end + "</p><br><br><p>Use " + promo_code + " at checkout to save today!"
    email_server.send_email(message, subject, "projdeploy@gmail.com", test_mode=False)

