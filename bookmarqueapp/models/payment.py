import enum
from sqlalchemy.ext.hybrid import hybrid_property
from bookmarqueapp import app, db, fernet

class PaymentCard(db.Model):

    __tablename__ = 'card'
    cardID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    cardNumber = db.Column(db.String(250)) # do not access directly
    cardExpDate = db.Column(db.DateTime)
    cardType = db.Column(db.String(45))
    cardSVC = db.Column(db.String(250)) # do not access directly

    users = db.relationship('User', secondary='users_has_card', back_populates='cards')

    def __init__(self, cardNumber, cardExpDate, cardType, cardSVC, **kwargs):

        super(PaymentCard, self).__init__(**kwargs)
        self.cardType = cardType
        self.cardExpDate = cardExpDate

        self.card_number = cardNumber
        self.card_svc = cardSVC

    # encryption/decryption methods #
    @hybrid_property
    def card_number(self):
        return fernet.decrypt(self.cardNumber.encode()).decode()

    @card_number.setter
    def card_number(self, number):
        self.cardNumber = fernet.encrypt(number.encode())

    @hybrid_property
    def card_svc(self):
        return fernet.decrypt(self.cardSVC.encode()).decode()

    @card_svc.setter
    def card_svc(self, svc):
        self.cardSVC = fernet.encrypt(svc.encode())

class CardType(enum.Enum):
    AMEX = 'Amex'
    DISCOVER = 'Discover'
    MASTERCARD = 'MasterCard'
    VISA = 'Visa'
