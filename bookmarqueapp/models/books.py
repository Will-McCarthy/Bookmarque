import enum
from bookmarqueapp import app, db

# associative table
book_has_book_categories = db.Table('book_has_book_categories',
    db.Column('ISBN', db.String(13), db.ForeignKey('book.ISBN'), primary_key=True),
    db.Column('categoryID', db.Integer, db.ForeignKey('book_categories.categoryID'),
    primary_key=True))

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

    categories = db.relationship('BookCategory', secondary='book_has_book_categories', back_populates='books', lazy=True)

class BookCategory(db.Model):
    __tablename__ = 'book_categories'
    categoryID = db.Column(db.Integer, primary_key=True)
    categoryName = db.Column(db.String(45))

    books = db.relationship('Book', secondary='book_has_book_categories', back_populates='categories')

class Categories(enum.Enum):

    FEATURED = 1
    EDUCATION = 2
    DOMESTIC_FICTION = 3
    DRAMA = 4
    CLASSIC = 5
    THRILLER = 6
    ROMANCE = 7
    HISTORY = 8
    YOUNG_ADULT = 9
    ESOTERIC = 10
    SCIENCE_FICTION = 11
    SCIENCE = 12
    SELF_HELP = 13
    NON_FICTION = 14
    HORROR = 15
    BUSINESS = 16
    SHORT_STORIES = 17
    NEWLY_RELEASED = 18
