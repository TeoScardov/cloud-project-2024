
class PurchaseDao:
    def __init__(self):
        self.conn = sqlite3.connect('shop.db')
        self.c = self.conn.cursor()

    def insertPurchase(self, purchase):
        self.c.execute("INSERT INTO purchase VALUES (?, ?, ?, ?, ?, ?)",
                       (purchase.member_id, purchase.product_id, purchase.quantity, purchase.price, purchase.date, purchase.paytype))
        self.conn.commit()
        return self.c.rowcount

    def selectPurchaseList(self, member_id):
        self.c.execute("SELECT * FROM purchase WHERE member_id=?", (member_id,))
        return self.c.fetchall()

    def __del__(self):
        self.conn.close()