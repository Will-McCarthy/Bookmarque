import enum
from bookmarqueapp import app

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
