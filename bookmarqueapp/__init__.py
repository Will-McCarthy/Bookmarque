from flask import Flask
from flask import render_template # for file extends
from sassutils.wsgi import SassMiddleware # for sass/scss compilation


app = Flask(__name__)

# configure directory locations for Sass/SCSS
app.wsgi_app = SassMiddleware(app.wsgi_app, {
    'bookmarqueapp': ('static/sass', 'static/css', '/static/css')
})

@app.route('/')
def homepage():
    return render_template('index.html')

@app.route('/login')
def login_panel():
    return render_template('login.html')

# registration pages, hard coded for now
@app.route('/registration/information')
def reg1():
    return render_template('reg1.html')

@app.route('/registration/payment')
def reg2():
    return render_template('reg2.html')

@app.route('/registration/shipping')
def reg3():
    return render_template('reg3.html')

@app.route('/registration/confirmation')
def reg4():
    return render_template('reg4.html')

@app.route('/search/')
def search():
    return render_template('search_view.html')

@app.route('/view/The+Vacationers')
def book_details():
    return render_template('book_details_example.html')

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

