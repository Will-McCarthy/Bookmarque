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

from flask_sqlalchemy import SQLAlchemy

# custom imports
from . import config as cfg # for loading in custom configuration information
from . import email_server # setup of email server and associated functions

DEBUG_MODE = True # changes whether certain tests are run

app = Flask(__name__)
app.config['MYSQL_HOST'] = cfg.mysql["host"]
app.config['MYSQL_USER'] = cfg.mysql["user"]
app.config['MYSQL_PASSWORD'] = cfg.mysql["password"]
app.config['MYSQL_DB'] = cfg.mysql["db"]

# sql alchemy test
app.config['SQLALCHEMY_DATABASE_URI'] = ('mysql://' + cfg.mysql["user"] + ':'
                + cfg.mysql["password"] + '@' + cfg.mysql["host"] + '/'
                + cfg.mysql["db"])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


from bookmarqueapp.models.books import Book, BookCategory, Categories
#query(FooBar).join(Bar).join(Foo).filter(Foo.name == "blah")
# session.query(BlogPost).\
# ...             filter(BlogPost.keywords.any(keyword='firstpost')).\
# ...             all()


results = Book.query.all()
results = Book.query.filter(Book.categories.any(BookCategory.categoryID == Categories.FEATURED.value))
for result in results:
    print(result)
print(results[1])


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

@app.route('/mysqltest')
def test():
    cursor = mysql.connection.cursor()
    cursor.execute('''SELECT * FROM book;''')
    rv = cursor.fetchall()
    print(rv)
    #cursor.execute(''' INSERT INTO info_table VALUES(%s,%s)''',(name,age))
    mysql.connection.commit()
    return render_template('index.html')


####
# while not usually standard practice to include import statements at the bottom
# of a file, the Flask documentation discusses this practice being necessary, as it
# is here in order to make sure other configuration is performed first.
# for instance, we currently need to import from THIS file app, mysql, and login_manager
# and need to make sure they are setup first. could in future migrate this
# functionality more locally.
from bookmarqueapp.views import views, admin, checkout, login, profile
