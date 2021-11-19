class Card:
    SUIT_SYMBOLS = {
        0: u"\u2666",  # diamonds
        1: u"\u2665",  # hearts
        2: u"\u2663",  # clubs
        3: u"\u2660"  # spades
    }

    VALUE_NAMES = {
        1: "A",
        2: "2",
        3: "3",
        4: "4",
        5: "5",
        6: "6",
        7: "7",
        8: "8",
        9: "9",
        10: "T",
        11: "J",
        12: "Q",
        13: "K"
    }

    def __init__(self, suit, value):
        self.suit = suit
        self.value = value
        self.hidden = False

    def __str__(self):
        if self.hidden:
            return "Unknown"
        return f"{self.SUIT_SYMBOLS[self.suit]}{self.VALUE_NAMES[self.value]}"
