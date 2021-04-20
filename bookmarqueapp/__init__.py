from flask import Flask, render_template  # for file extends
from flask_mysqldb import MySQL #Mysql
from flask_login import LoginManager #Logins
from sassutils.wsgi import SassMiddleware # for sass/scss compilation
from flask_sqlalchemy import SQLAlchemy # ORM management
from cryptography.fernet import Fernet # symmetric encryption tool
import datetime
# custom imports
from . import config as cfg # for loading in custom configuration information
from . import email_server # setup of email server and associated functions
#from . models import User, UserStatus

app = Flask(__name__)

# general
app.config['DEBUG'] = True # changes whether certain tests are run and emails are sent
app.config['SECRET_KEY'] = b'_5#y2L"F4Q8z\n\xec]/'

# mysqldb setup
app.config['MYSQL_HOST'] = cfg.mysql["host"]
app.config['MYSQL_USER'] = cfg.mysql["user"]
app.config['MYSQL_PASSWORD'] = cfg.mysql["password"]
app.config['MYSQL_DB'] = cfg.mysql["db"]
mysql = MySQL(app)

# sql alchemy setup
app.config['SQLALCHEMY_DATABASE_URI'] = ('mysql://' + cfg.mysql["user"] + ':'
                + cfg.mysql["password"] + '@' + cfg.mysql["host"] + '/'
                + cfg.mysql["db"])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# fernet (encryption algorithm) setup
fernet = Fernet(cfg.encryption["key"])

# login initialization
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app)

# configure directory locations for Sass/SCSS
app.wsgi_app = SassMiddleware(app.wsgi_app, {
    'bookmarqueapp': ('static/sass', 'static/css', '/static/css')
})

# mysql test url
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
# of a file, the Flask documentation discusses this practice being necessary
####
from bookmarqueapp.views import views, admin, checkout, login, profile




####### encryption testing #######
# from bookmarqueapp.models.users import User
# from bookmarqueapp.models.payment import PaymentCard, CardType
# # expDate = datetime.datetime.today()
# # ex = PaymentCard('2333 4444 5555 6666', expDate, CardType.AMEX, '333')
#
# ex = PaymentCard.query.filter_by(cardID="1018").first()
# #
# #
# # db.session.add(ex)
# # db.session.commit()
#
# print('here')
# print(ex.number)
# print(ex.svc)
# print(ex.cardType)
#
# # from bookmarqueapp.models.users import User
# jane = User.query.filter_by(userEmail="admin@gmail.com").one()
# print(jane)
# jane.password = "password"
# jane.cards.append(ex)
# db.session.commit()
# print(jane.password)
