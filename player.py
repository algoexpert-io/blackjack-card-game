from dealer import Dealer


class Player(Dealer):
    def __init__(self, balance):
        super().__init__()
        self.balance = balance
