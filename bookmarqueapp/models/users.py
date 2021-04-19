import enum
from sqlalchemy.ext.hybrid import hybrid_property
from bookmarqueapp import app, db, fernet


# factory design pattern object generator
class UserFactory():

    def get_user(self, id):
        type = User.query.filter_by(userID=id).one().userType

        if type == UserType.ADMIN.value:
            return Admin.query.filter_by(userID=id).one()
        elif type == UserType.CUSTOMER.value:
            return Customer.query.filter_by(userID=id).one()
        elif type == UserType.WEB_USER.value:
            return WebUser.query.filter_by(userID=id).one()
        return None

class User(db.Model):

    # global vars for login management
    is_authenticated = False
    logged_in = False

    __tablename__ = 'users'
    userID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    userEmail = db.Column(db.String(45)) # varchar(115)
    userFName = db.Column(db.String(45))
    userLName = db.Column(db.String(45))
    userStatus = db.Column(db.String(45))
    userType = db.Column(db.String(45))
    userPassword = db.Column(db.String(250))
    userPhone = db.Column(db.String(45))
    userSubStatus = db.Column(db.String(45))


    addressID = db.Column(db.Integer, db.ForeignKey('address.addressID'))
    address = db.relationship('Address', lazy=True)

    cards = db.relationship('PaymentCard', secondary='users_has_card', back_populates='users')

    # override print
    def __str__(self):
        return (str(self.userID) + ', ' + self.userEmail + ', ' + self.userFName + ', ' + self.userLName
        + ', ' + self.userStatus + ', ' + self.userType)

    # specific for flask_login
    def is_authenticated(self):
        return self.is_authenticated

    def get_id(self):
        return str(self.userID)

    def set_status(self, status):
        self.userStatus = status.value

    def set_type(self, type):
        self.userType = type.value

    # set to value of boolean
    def set_subscription(self, active):
        self.userSubStatus = 'Active' if active else 'Deactive'

    # encryption/decryption methods
    @hybrid_property
    def password(self):
        return fernet.decrypt(self.userPassword.encode()).decode()

    # must commit to database before using value
    @password.setter
    def password(self, plaintext):
        self.userPassword = fernet.encrypt(plaintext.encode())

    # return true if encrypted password matches attempted_password
    def check_password(self, attempted_password):
        return (self.password == attempted_password)



# inheritance classes #
class Customer(User):

    def __init__(self, **kwargs):
        super(Customer, self).__init__(**kwargs)

class Admin(User):

    def __init__(self, **kwargs):
        super(Admin, self).__init__(**kwargs)


class WebUser(User):

    def __init__(self, **kwargs):
        super(WebUser, self).__init__(**kwargs)

# enumerations
class UserStatus(enum.Enum):
    ACTIVE = 'Active'
    INACTIVE = 'Inactive'
    SUSPENDED = 'Suspended'

class UserType(enum.Enum):
    ADMIN = 'Admin'
    CUSTOMER = 'Customer'
    WEB_USER = 'Web'

# user info
class Address(db.Model):

    __tablename__= 'address'
    addressID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    addressStreet = db.Column(db.String(45))
    addressCity = db.Column(db.String(45))
    addressState = db.Column(db.String(45))
    addressZip = db.Column(db.String(45))

class PaymentCard(db.Model):

    __tablename__ = 'card'
    cardID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    cardNumber = db.Column(db.String(45)) # varchar(115)
    cardExpDate = db.Column(db.DateTime)
    cardType = db.Column(db.String(45))
    cardSVC = db.Column(db.Integer)

    users = db.relationship('User', secondary='users_has_card', back_populates='cards')

# associative table
users_has_card = db.Table('users_has_card',
    db.Column('userEmail', db.String(45), db.ForeignKey('users.userEmail'), primary_key=True),
    db.Column('cardID', db.Integer, db.ForeignKey('card.cardID'),
    primary_key=True))

class CardType(enum.Enum):
    AMEX = 1
    DISCOVER = 2
    MASTERCARD = 3
    VISA = 4
