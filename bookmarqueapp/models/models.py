import enum
from bookmarqueapp import app


class ShoppingCart():
    def __init__(self):
        print('web user')

class Promotion():
    def __init__(self):
        print('web user')

class Order():
    def __init__(self):
        print('web user')

class OrderStatus(enum.Enum):
    PENDING = 1
    PLACED = 2
    SHIPPED = 3
    ARRIVED = 4
