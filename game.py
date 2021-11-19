from deck import Deck
from hand import Hand


class Game:
    MINIMUM_BET = 1

    def __init__(self, player, dealer):
        self.player = player
        self.dealer = dealer
        self.bet = None
        self.deck = Deck()

    def place_bet(self):
        while True:
            bet = float(input("Place your bet: "))
            if bet > self.player.balance:
                print("You do not have sufficient funds.")
            elif bet < self.MINIMUM_BET:
                print(f"The minimum bet is ${self.MINIMUM_BET}.")
            else:
                self.bet = bet
                self.player.balance -= bet
                break

    def get_player_hit_or_stay(self):
        while True:
            hit_or_stay = input("Would you like to hit or stay? ").lower()

            if hit_or_stay in ["hit", "stay"]:
                break

            print("That is not a valid option.")

        return hit_or_stay == "hit"  # return true if player hit, false if stay

    def deal_starting_cards(self):
        self.player.hand = Hand(self.deck.deal(2))
        self.dealer.hand = Hand(self.deck.deal(2))
        self.dealer.hand.cards[1].hidden = True
        print("You are dealt:", self.player.get_str_hand())
        print("The dealer is dealt:", self.dealer.get_str_hand())

    def player_turn(self):
        while True:
            hit = self.get_player_hit_or_stay()
            if not hit:
                break

            new_card = self.deck.deal(1)[0]
            self.player.hit(new_card)
            print("You are dealt:", new_card)
            print("You now have:", self.player.get_str_hand())

            if self.player.hand.get_value() > 21:
                return True  # player lost

        return False  # player did not lose

    def dealer_turn(self):
        self.dealer.hand.cards[1].hidden = False
        print("The dealer has:", self.dealer.get_str_hand())

        while self.dealer.hand.get_value() <= 16:
            new_card = self.deck.deal(1)[0]
            self.dealer.hit(new_card)
            print("The dealer hits and is dealt:", new_card)
            print("The dealer has:", self.dealer.get_str_hand())

        if self.dealer.hand.get_value() > 21:
            return True

        return False

    def handle_blackjack(self):
        if self.player.hand.get_value() != 21:
            return False

        if self.dealer.hand.get_value() == 21:
            self.player.balance += self.bet
            print(
                "Both you and the dealer have Blackjack, you tie. Your bet has been returned.")
            return True

        self.player.balance += self.bet * 2.5
        print(f"Blackjack! You win {self.bet * 1.5} :)")
        return True

    def reset_round(self):
        self.deck = Deck()
        self.player.hand = None
        self.dealer.hand = None
        self.bet = None

    def determine_winner(self):
        player_value = self.player.hand.get_value()
        dealer_value = self.dealer.hand.get_value()

        if dealer_value < player_value:
            self.player.balance += self.bet * 2
            print(f"You win ${self.bet}!")
        elif dealer_value > player_value:
            print(f"The dealer wins, you lose ${self.bet} :(")
        else:
            self.player.balance += self.bet
            print("You tie. Your bet has been returned.")

    def confirm_start(self):
        answer = input(
            f"You are starting with ${self.player.balance}, would you like to play? ").lower()
        return answer in ['y', 'yes', 'start']

    def start_round(self):
        self.place_bet()
        self.deal_starting_cards()

        if self.handle_blackjack():
            return

        player_lost = self.player_turn()
        if player_lost:
            print(f"Your hand value is over 21 and you lose ${self.bet} :(")
            return

        dealer_lost = self.dealer_turn()
        if dealer_lost:
            self.player.balance += self.bet * 2
            print(f"The dealer busts, you win ${self.bet} :)")
            return

        self.determine_winner()
        self.reset_round()

    def start_game(self):
        while self.player.balance > 0:
            if not self.confirm_start():
                print(f"You left the game with ${self.player.balance}.")
                break

            self.start_round()
            print()
        else:
            print(
                "You've ran out of money. Please restart this program to try again. Goodbye.")
