import random
import copy
from enum import Enum

class Suit(Enum):
    HEARTS = "❤️"
    SPADE = "♠️"
    CLUBS = "♣️"
    DIAMONDS = "♦️"

class Face(Enum):
    TWO = "2"
    THREE = "3"
    FOUR = "4"
    FIVE = "5"
    SIX = "6"
    SEVEN = "7"
    EIGHT = "8"
    NINE = "9"
    TEN = "10"
    JACK = "J"
    QUEEN = "Q"
    KING = "K"
    ACE = "A"

    def face_value(self) -> int:
        match self:
            case Face.JACK | Face.QUEEN | Face.KING:
                return 10
            case Face.ACE:
                return 11
            case _:
                return int(self.value)

class Card:
    def __init__(self, face, suit):
        self.face = face
        self.suit = suit

    def __hash__(self) -> int:
        return hash(self.face.name) * hash(self.suit.name)

    def __repr__(self):
        return f"[{self.face.value}{self.suit.value}]"

class MultiDeck:
    def __init__(self):
        self.num_decks = random.choice([2, 4, 6, 8])
        one_deck = [Card(face, suit) for suit in Suit for face in Face]
        self.cards = [copy.deepcopy(card) for _ in range(self.num_decks) for card in one_deck]
        self.shuffle()
    
    def shuffle(self):
        random.shuffle(self.cards)
    
    def deal_card(self):
        if not self.cards:
            self.__init__()
        return self.cards.pop()

class Game:
    def __init__(self):
        self.deck = MultiDeck()
        self.player_hand = []
        self.dealer_hand = []
    
    def deal_initial_cards(self):
        for _ in range(2):
            self.player_hand.append(self.deck.deal_card())
            self.dealer_hand.append(self.deck.deal_card())
    
    def calculate_score(self, hand):
        score = sum(card.face.face_value() for card in hand)
        num_aces = sum(1 for card in hand if card.face == Face.ACE)
        while score > 21 and num_aces:
            score -= 10
            num_aces -= 1
        return score
    
    def display_hands(self, reveal_dealer=False):
        print(f"\nYour hand: {self.player_hand} (Score: {self.calculate_score(self.player_hand)})")
        if reveal_dealer:
            print(f"Dealer's hand: {self.dealer_hand} (Score: {self.calculate_score(self.dealer_hand)})")
        else:
            print(f"Dealer's hand: [{self.dealer_hand[0]}, Hidden Card]")
    
    def player_turn(self):
        while True:
            self.display_hands()
            choice = input("Do you want to hit or stay? (h/s): ").lower()
            if choice == 'h':
                self.player_hand.append(self.deck.deal_card())
                if self.calculate_score(self.player_hand) > 21:
                    print("You busted! Dealer wins.")
                    return False
            elif choice == 's':
                break
        return True
    
    def dealer_turn(self):
        while self.calculate_score(self.dealer_hand) < 17:
            self.dealer_hand.append(self.deck.deal_card())
        self.display_hands(reveal_dealer=True)
    
    def determine_winner(self):
        player_score = self.calculate_score(self.player_hand)
        dealer_score = self.calculate_score(self.dealer_hand)
        
        if dealer_score > 21:
            print("Dealer busted! You win!")
        elif player_score > dealer_score:
            print("You win!")
        elif player_score < dealer_score:
            print("Dealer wins.")
        else:
            print("It's a tie!")
    
    def play(self):
        print("\nWelcome to Multi-Deck Blackjack!\n")
        while True:
            self.deck = MultiDeck()
            self.player_hand = []
            self.dealer_hand = []
            
            self.deal_initial_cards()
            
            if self.player_turn():
                self.dealer_turn()
                self.determine_winner()
            
            play_again = input("\nDo you want to play again? (y/n): ").lower()
            if play_again != 'y':
                print("Thanks for playing!")
                break

if __name__ == "__main__":
    game = Game()
    game.play()
