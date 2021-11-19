class Hand:
    def __init__(self, cards):
        self.cards = cards

    def get_value(self):
        value = 0
        aces = 0

        for card in self.cards:
            val = card.value
            if val == 1:
                aces += 1
            else:
                value += min(val, 10)

        if aces == 0:
            return value

        if value + 11 > 21:
            return value + aces
        elif aces == 1:
            return value + 11
        elif value + 11 + (aces - 1) <= 21:
            return value + 11 + (aces - 1)
        else:
            return value + aces

    def add(self, card):
        self.cards.append(card)

    def __str__(self):
        string_cards = [str(card) for card in self.cards]
        return ", ".join(string_cards)
