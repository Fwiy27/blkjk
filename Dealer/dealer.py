from os import system
import sys

from Deck.deck import Deck

def clear_screen():
    if sys.platform.startswith('win'):
        system('cls')
    else:
        system('clear')

def calculate_count(hand):
    sum = 0
    alternate_sum = 0
    for card in hand:
        if isinstance(card['value'], list):
            sum += card['value'][0]
            alternate_sum += card['value'][1]
        else:
            sum += card['value']
            alternate_sum += card['value']
    return sum if alternate_sum == sum else [sum, alternate_sum]

def print_hand(hand):
    for card in hand:
        print(f'[{card["card"]}]', end='')
    print(f' | {calculate_count(hand)}')

def fix_hand(hand):
    hand_count = calculate_count(hand)
    for i in range(0, len(hand)):
        if isinstance(hand[i]['value'], list):
                if max(hand_count) > 21:
                    hand[i]['value'] = hand[i]['value'][0]
                else: 
                    hand[i]['value'] = hand[i]['value'][1]
    return hand
    
class Dealer:
    def __init__(self, size):
        self.d = Deck(size)
        self.user_hand = []
        self.dealer_hand = []
        self.status = 'play'

    def print_board(self):
        clear_screen()
        print_hand(self.dealer_hand)
        print_hand(self.user_hand)
    
    def deal(self):
        # Deal 2 to dealer
        for i in range(2):
            self.dealer_hand.append(self.d.draw())
        
        # Deal 2 to user
        for i in range(2):
            self.user_hand.append(self.d.draw())
        
        # Set proper counts
        self.dealer_hand = fix_hand(self.dealer_hand)
        self.user_hand = fix_hand(self.user_hand)

        if calculate_count(self.dealer_hand) == 21:
            self.status = 'lose'

        # Print hands
        self.print_board()

        if self.status == 'lose':
            print('Dealer Wins')
        
    def hit(self, who):
        if who == 'user':
            self.user_hand.append(self.d.draw())
            self.user_hand = fix_hand(self.user_hand)
        else:
            self.dealer_hand.append(self.d.draw())
            self.dealer_hand = fix_hand(self.dealer_hand)

###
d = Dealer(1)
d.deal()
input()
d.hit('user')
d.print_board()