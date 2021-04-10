from flask import Flask, redirect, request, render_template, url_for
from flask_mysqldb import MySQL #Mysql
from flask_login import LoginManager, current_user, login_user, logout_user, login_required #Logins

from bookmarqueapp import app, mysql
from bookmarqueapp.models.models import User

@app.route('/admin')
def admin():
    return render_template('admin/admin_view.html')

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
    return render_template('admin/manage_books.html', bookData = bookData)

@app.route('/manage-books/book-entry')
def bookEntry():
    return render_template('admin/book_entry.html')

@app.route('/manage-users')
def manageUsers():
    return render_template('admin/manage_users.html')

@app.route('/manage-users/user-entry')
def userEntry():
    return render_template('admin/user_entry.html')

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
        return render_template('admin/manage_promotions.html', promotions = promotion_fetch)
