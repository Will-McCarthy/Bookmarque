import enum
from flask_mysqldb import MySQL #Mysql
from bookmarqueapp import app, mysql

# factory design pattern object generator
class UserFactory():

    def get_user(self, type):
        if type == UserType.ADMIN.value:
            return Admin()
        elif type == UserType.CUSTOMER.value:
            return Customer()
        elif type == UserType.WEB_USER.value:
            return WebUser()
        return None

class User():

    # global vars for login management
    is_authenticated = False
    logged_in = False

    def __init__(self, id=None, email=None, fname=None, lname=None, status=None,
                    type=None, password=None, phone=None, subscription=None,
                    address=None, payments=[]):

        self.id = id
        self.email = email
        self.fname = fname
        self.lname = lname
        self.status = status
        self.type = type
        self.password = password
        self.phone = phone
        self.subscription = subscription
        self.address = address
        self.payment_cards = payments

    def set(self, id=None, email=None, fname=None, lname=None, status=None,
                    type=None, password=None, phone=None, subscription=None,
                    address=None, payments=[]):

        self.id = id
        self.email = email
        self.fname = fname
        self.lname = lname
        self.status = status
        self.type = type
        self.password = password
        self.phone = phone
        self.sub_status = subscription
        self.address = address
        self.payment_cards = payments

    def __str__(self):
        return (str(self.id) + ', ' + self.email + ', ' + self.fname + ', ' + self.lname
        + ', ' + self.status + ', ' + self.type)

    # specific for flask_login
    def is_authenticated(self):
        return self.is_authenticated

    def get_id(self):
        return self.id

    # def is_active(self):
    #     return self.is_active
    #
    # def is_anonymous(self):
    #     return self.is_anonymous

class Customer(User):

    def __init__(self):
        super().__init__()

class Admin(User):

    def __init__(self):
        super().__init__()


class WebUser(User):

    def __init__(self):
        super().__init__()


# enumerations
class UserStatus(enum.Enum):
    ACTIVE = 'Active'
    INACTIVE = 'Inactive'
    SUSPENDED = 'Suspended'

# inheritance here
class UserType(enum.Enum):
    ADMIN = 'Admin'
    CUSTOMER = 'Customer'
    WEB_USER = 'Web'
