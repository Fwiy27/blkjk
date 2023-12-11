from os import system
import sys
import time

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
    def __init__(self, size=6, money=5000):
        self.d = Deck(size)
        self.user_hand = []
        self.dealer_hand = []
        self.money = money
        self.bet_amount = 250

    def print_board(self):
        clear_screen()
        print(f'Money: ${self.money}')
        print('---------------')
        print_hand(self.dealer_hand)
        print_hand(self.user_hand)
    
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
        
        # Set proper counts
        self.dealer_hand = fix_hand(self.dealer_hand)
        self.user_hand = fix_hand(self.user_hand)

        if calculate_count(self.dealer_hand) == 21:
            self.status = 'lose'

    def hit(self, who):
        if who == 'user':
            self.user_hand.append(self.d.draw())
            self.user_hand = fix_hand(self.user_hand)
        else:
            self.dealer_hand.append(self.d.draw())
            self.dealer_hand = fix_hand(self.dealer_hand)

    def play(self):
        bet_amount = None
        while bet_amount == None:
            clear_screen()
            print(f'Money: ${self.money}')
            bet_amount = input('Bet Amount: ')
            if bet_amount == 'clear':
                clear_screen()
                exit()
            elif bet_amount != '':
                try:
                    self.bet_amount = max(min(int(bet_amount), self.money), 0)
                except:
                    bet_amount = None
                    input('Invalid Bet Amount, Press Enter to Continue . . .')
                

        self.status = 'play'
        stand = False
        clear_screen()
        self.deal()
        while self.status == 'play':
            self.print_board()
            while calculate_count(self.user_hand) <= 21 and not stand:
                command = input('Command: ')
                match command:
                    case "hit" | "h":
                        self.hit('user')
                    case "stand" | "s":
                        stand = True
                    case "clear":
                        clear_screen()
                        exit()
                    case _:
                        input('Invalid Command, Press Enter to Continue . . .')
                clear_screen()
                self.print_board()
            if calculate_count(self.user_hand) <= 21:
                while calculate_count(self.dealer_hand) < 17:
                    self.hit('dealer')
                    time.sleep(1)
                    clear_screen()
                    self.print_board()
                self.status = 'tbd'
            else:  
                self.status = 'lose'
        
        # check for winner
        if self.status != 'lose':
            if calculate_count(self.user_hand) > calculate_count(self.dealer_hand):
                self.status = 'win'
            elif calculate_count(self.dealer_hand) > 21:
                self.status = 'win'
            else: self.status = 'lose'
        
        # update money
        match self.status:
            case "win":
                self.money += self.bet_amount
                input('WON, Press Enter to Continue . . .')
            case "lose":
                self.money -= self.bet_amount
                input('LOST, Press Enter to Continue . . .')
        
        self.play()
