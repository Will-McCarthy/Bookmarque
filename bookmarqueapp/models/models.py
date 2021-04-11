import enum
from bookmarqueapp import app, db

class Book(db.Model):

    __tablename__ = 'book'
    ISBN = db.Column(db.String(13), primary_key=True) # char(13) PK
    bookTitle = db.Column(db.String(115)) # varchar(115)
    authorFName = db.Column(db.String(45))
    authorLName = db.Column(db.String(45))
    bookImage = db.Column(db.String(50))
    bookPrice = db.Column(db.Float)
    bookQuantity = db.Column(db.Integer)
    bookRating = db.Column(db.Integer)
    bookPublisher = db.Column(db.String(45))
    bookPublicationDate = db.Column(db.DateTime)
    bookDescription = db.Column(db.String(1000))

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
