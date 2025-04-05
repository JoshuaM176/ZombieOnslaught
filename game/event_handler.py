class Events():

    def __init__(self):
        self.money = 0

    def earn_money(self, money):
        self.money += money

    def get_money(self):
        rtn = self.money
        self.money = 0
        return rtn