class PaymentDao:
    def __init__(self, db):
        self.db = db

    def save(self, payment):
        self.db.save(payment)
        return True