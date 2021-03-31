import enum

class User():
    id = None
    email = None
    password = None
    fname = None
    lname = None
    is_active = True
    logged_in = False
    is_authenticated = False


    def __init__(self, id, email, password, fname, lname):
        self.id = id
        self.email = email
        self.password = password
        self.fname = fname
        self.lname = lname

    def get_id(self):
        return self.id

    def is_authenticated(self):
        return self.is_authenticated



class RegisteredUser:


    def __init__(self):
        print('registered user')

class PaymentCard():

    id = None
    cardNumber = None
    cardType = None
    expirationDate = None
    svc = None

    def __init__(self, cardNumber, cardType, expirationDate, svc):
        self.cardNumber = cardNumber
        self.cardType = cardType
        self.expirationDate = expirationDate
        self.svc = svc

    def get_id(self):
        return self.id

class Address():

    id = None
    street = None
    state = None
    city = None
    zipcode = None

    def __init__(self, street, state, city, zipcode):
        self.cardNumber = cardNumber
        self.cardType = cardType
        self.expirationDate = expirationDate
        self.svc = svc

    def get_id(self):
        return self.id


class WebUser:

    def __init__(self):
        print('web user')

class Admin:
    def __init__(self):
        print('web user')

class ShoppingCart:
    def __init__(self):
        print('web user')

class Promotion:
    def __init__(self):
        print('web user')

class Order:
    def __init__(self):
        print('web user')

class Book:

    def __init__(self):
        print('web user')


# enumerations
class UserStatus(enum.Enum):
    ACTIVE = 'Active'
    INACTIVE = 'Inactive'
    SUSPENDED = 'Suspended'

class CardType(enum.Enum):
    AMEX = 'American Express'
    DISCOVER = 'Discover'
    MASTERCARD 'MasterCard'
    VISA = 'Visa'

class OrderStatus(enum.Enum):
    PENDING = 'Pending'
    PLACED = 'Placed'
    SHIPPED = 'Shipped'
    ARRIVED = 'Arrived'
