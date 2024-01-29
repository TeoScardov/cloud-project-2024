class Purchase():
    def __init__(self, id, user_id, product_id, quantity, total, date):
        self.id = id
        self.user_id = user_id
        self.product_id = product_id
        self.quantity = quantity
        self.total = total
        self.date = date

    def __repr__(self):
        return f'<Purchase {self.id}>'

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'product_id': self.product_id,
            'quantity': self.quantity,
            'total': self.total,
            'date': self.date
        }