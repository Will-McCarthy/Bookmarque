import enum
from flask_mysqldb import MySQL #Mysql
from bookmarqueapp import app, mysql


class Book():

    # constructor using all data
    def __init__(self, ISBN, title, author_fname, author_lname, image, price,
                quantity, rating, publisher, publication_date, description,
                category):

        self.ISBN = ISBN
        self.title = title
        self.author_fname = author_fname
        self.author_lname = author_lname
        self.image = image
        self.price = price
        self.quantity = quantity
        self.rating = rating
        self.publisher = publisher
        self.publication_date = publication_date
        self.description = descriptionn
        self.category = category


    def add_to_db(self):
        print('adding to database')


class DataAccess():
    def __init__(self):
        print('da')


class BookDataAccess(DataAccess):
    def __init__(self):
        print('bda')


class BookCategory(enum.Enum):

    FEATURED = 1
    EDUCATION = 2
    DOMESTIC_FICTION = 3
    DRAMA = 4
    CLASSIC = 5
    THRILLER = 6
    ROMANCE = 7
    HISTORY = 8
    YA = 9
    ESOTERIC = 10
    SCI_FI = 11
    SCIENCE = 12
    SELF_HELP = 13
    NON_FICTION = 14
    HORROR = 15
    BUSINESS = 16
    SHORT_STORIES = 17
    NEWLY_RELEASED = 18


class User():

    # global vars for login management
    is_authenticated = False
    logged_in = False

    def __init__(self, id, email, password, fname, lname):
        self.id = id
        self.email = email
        self.fname = fname
        self.lname = lname

        # class attributes
        self.user_status = None
        self.user_type = None
        self.password = password
        self.phone = None
        self.sub_status = None

        self.payment_cards = []
        self.address = None

    def get_id(self):
        return self.id

    def is_authenticated(self):
        return self.is_authenticated



class RegisteredUser(User):

    def __init__(self):
        print('registered user')

class WebUser(User):

    def __init__(self):
        print('web user')

class Admin(User):
    def __init__(self):
        print('web user')

class Employee(User):
    def __init__(self):
        print('emloyee')

class PaymentCard():

    def __init__(self, cardNumber, cardType, expirationDate, svc):
        self.cardNumber = cardNumber
        self.cardType = cardType
        self.expirationDate = expirationDate
        self.svc = svc

    def get_id(self):
        return self.id

class Address():

    def __init__(self, street, state, city, zipcode):
        self.cardNumber = cardNumber
        self.cardType = cardType
        self.expirationDate = expirationDate
        self.svc = svc

    def get_id(self):
        return self.id

class ShoppingCart():
    def __init__(self):
        print('web user')

class Promotion():
    def __init__(self):
        print('web user')

class Order():
    def __init__(self):
        print('web user')


# enumerations
class UserStatus(enum.Enum):
    ACTIVE = 1
    INACTIVE = 2
    SUSPENDED = 3

# inheritance here?
class UserType(enum.Enum):
    ADMIN = 1
    CUSTOMER = 2
    WEB_USER = 3

class CardType(enum.Enum):
    AMEX = 1
    DISCOVER = 2
    MASTERCARD = 3
    VISA = 4

class OrderStatus(enum.Enum):
    PENDING = 1
    PLACED = 2
    SHIPPED = 3
    ARRIVED = 4
