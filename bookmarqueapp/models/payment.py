import enum
from sqlalchemy.ext.hybrid import hybrid_property
from bookmarqueapp import app, db, fernet

class PaymentCard(db.Model):

    __tablename__ = 'card'
    cardID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    cardNumber = db.Column(db.String(250)) # varchar(115)
    cardExpDate = db.Column(db.DateTime)
    cardType = db.Column(db.String(45))
    cardSVC = db.Column(db.String(250))

    users = db.relationship('User', secondary='users_has_card', back_populates='cards')

    def __init__(self, cardNumber, cardExpDate, cardType, cardSVC, **kwargs):

        super(PaymentCard, self).__init__(**kwargs)
        self.cardType = cardType.value
        self.cardExpDate = cardExpDate

        self.number = cardNumber
        self.svc = cardSVC

    # encryption/decryption methods #
    @hybrid_property
    def number(self):
        return fernet.decrypt(self.cardNumber.encode()).decode()

    @number.setter
    def number(self, number_string):
        self.cardNumber = fernet.encrypt(number_string.encode())

    @hybrid_property
    def svc(self):
        return fernet.decrypt(self.cardSVC.encode()).decode()

    @svc.setter
    def svc(self, svc):
        self.cardSVC = fernet.encrypt(svc.encode())

class CardType(enum.Enum):
    AMEX = 'Amex'
    DISCOVER = 'Discover'
    MASTERCARD = 'MasterCard'
    VISA = 'Visa'
