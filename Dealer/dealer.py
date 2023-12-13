from os import system
import sys
import time
import random

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

def print_hand(hand, who, hidden=False):
    print(who, end='')
    if not hidden:
        for card in hand:
            print(f'[{card["card"]}]', end='')
        print(f' | {calculate_count(hand)}')
    else:
        print(f'[{hand[0]["card"]}] | {hand[0]["value"]}')

def fix_hand(hand, high=False):
    hand_count = calculate_count(hand)
    if isinstance(hand, list):
        if not high:
            for i in range(0, len(hand)):
                if isinstance(hand[i]['value'], list):
                    if max(hand_count) > 21:
                        hand[i]['value'] = hand[i]['value'][0]
                    else: 
                        hand[i]['value'] = hand[i]['value'][1]
            return hand
        else:
            for i in range(0, len(hand)):
                if isinstance(hand[i]['value'], list):
                    if max(hand_count) < 21:
                        hand[i]['value'] = hand[i]['value'][1]
                    else: 
                        hand[i]['value'] = hand[i]['value'][0]
               
    
class Dealer:
    def __init__(self, size=6, money=5000):
        self.d = Deck(size)
        self.user_hand = []
        self.dealer_hand = []
        self.money = money
        self.bet_amount = 250

    def print_board(self, hidden=False):
        clear_screen()
        print(f'Money: ${self.money}')
        print('---------------')
        print_hand(self.dealer_hand, 'Dealer: ', hidden)
        print_hand(self.user_hand, 'User: ')
    
    def deal(self):
        if len(self.d.deck) <= 10:
            self.d.shuffle()
        self.dealer_hand = []
        self.user_hand = []

        # Deal 2 to dealer
        for i in range(2):
            self.dealer_hand.append(self.d.draw())
        
        # Deal 2 to user
        for i in range(2):
            self.user_hand.append(self.d.draw())
        
    def hit(self, who):
        if who == 'user':
            self.user_hand.append(self.d.draw())
            self.user_hand = fix_hand(self.user_hand)
        else:
            self.dealer_hand.append(self.d.draw())
            self.dealer_hand = fix_hand(self.dealer_hand)

    def check_win(self, hidden = False):
        dealer_count = calculate_count(self.dealer_hand)
        user_count = calculate_count(self.user_hand)

        # Dealer has 21
        if isinstance(dealer_count, list) and max(dealer_count) == 21:
            self.dealer_hand = fix_hand(self.dealer_hand)
            return 'lose'
        
        # User goes over 21
        if isinstance(user_count, list):
            if min(user_count) > 21:
                self.user_hand = fix_hand(self.user_hand)
                return 'lose'
        else:
            if user_count > 21:
                return 'lose'
        
        if not hidden:
            # Dealer goes over 21
            if isinstance(dealer_count, list):
                if min(dealer_count) > 21:
                    self.dealer_hand = fix_hand(self.dealer_hand)
                    return 'win'
            else:
                if dealer_count > 21:
                    return 'win'
                
            # Dealer's hand is >= 18 but user hand is higher
            if isinstance(dealer_count, int) and isinstance(user_count, int):
                if dealer_count >= 18: 
                    if user_count > dealer_count:
                        return 'win'
                    else:
                        return 'lose'
        
        return 'play'
    
    def play(self):
        while self.money > 0:
            clear_screen()
            print(f'Money: {self.money}')
            bet = input('Bet: ')
            try:
                self.bet_amount = max(min(self.money, int(bet)), 0)
            except:
                pass
           


            # Initialize status and player
            player = 'user'
            status = 'play'
            hidden = True

            # Deal Cards
            self.deal()

            # Check for dealer 21
            status = self.check_win(True)

            # User Hits until Stand or Over 21
            while status == 'play':
                # 1 Action
                if player == 'user':
                    self.print_board(True)
                    # User Plays
                    match input('Command: '):
                        case "hit" | "h":
                            self.hit('user')
                        case "stand" | "s":
                            player = 'dealer'
                else:
                    hidden = False
                    # Dealer Plays (optional)
                    self.print_board()
                    input('Press Enter to Continue . . .')
                    if isinstance(calculate_count(d.dealer_hand), list):
                        if max(calculate_count(d.dealer_hand)) >= 18:
                            self.dealer_hand = fix_hand(d.dealer_hand)
                    else:
                        if calculate_count(d.dealer_hand) < 18:
                            self.hit('dealer')

                # Check for win
                status = self.check_win(hidden)

            # After win or loss
            self.print_board()
            match status:
                case 'win':
                    self.money += self.bet_amount
                    input('WIN')
                case 'lose':
                    self.money -= self.bet_amount
                    input('LOSE')
        
        
# random.seed(763)

d = Dealer()

d.play()