class Payment():
    def __init__(self, id, user_id, purchase_id, amount, created_at):
        self.id = id
        self.user_id = user_id
        self.purchase_id = purchase_id
        self.amount = amount
        self.created_at = created_at

    def __repr__(self):
        return f'<Payment {self.id}>'

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'purchase_id': self.purchase_id,
            'amount': self.amount,
            'created_at': self.created_at
        }