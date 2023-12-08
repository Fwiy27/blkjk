import random
from colorama import Fore

def multiply_lists(list1, list2, size=1):
    list_f = []
    for i in range(size):
        for item1 in list1:
            for item2 in list2:
                list_f.append(item2 + item1)
    return list_f

def get_info(card) -> dict:
    color = Fore.RED if card[-1] in ['♥', '♦'] else Fore.LIGHTBLACK_EX
    try:
        value = int(card[0]) if len(card) == 2 else int(card[0:2])
    except:
        match card[0]:
            case 'A':
                value = [1, 11]
            case 'J' | 'Q' | 'K':
                value = 10
    return {'card': color + card + Fore.RESET, 'value': value}

face = ['A', '2', '3', '4', '5', '6', '7', '8', 
         '9', '10', 'J', 'Q', 'K']
suit = ['♠', '♥', '♦', '♣']

class Deck:
    def __init__(self, size=1):
        self.size = size
        self.shuffle()

    def draw(self) -> dict:
        index = random.randint(0, len(self.deck) - 1)
        card = self.deck[index]
        self.deck.pop(index)
        return get_info(card)
    
    def shuffle(self):
        self.deck = multiply_lists(suit, face, self.size)