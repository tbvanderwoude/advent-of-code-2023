from aoc_util import *
import functools
from collections import Counter
from enum import IntEnum

class HandType(IntEnum):
    Five = 6
    Four = 5
    FullHouse = 4
    Three = 3
    TwoPair = 2
    OnePair = 1
    HighCard = 0

def determine_type(s):
    counter = Counter(s)
    counts = sorted(list(counter.items()), key=lambda x: -x[1])
    highest = counts[0][1]
    match highest:
        case 5:
            return HandType.Five
        case 4:
            return HandType.Four
        case 3:
            second_highest = counts[1][1]
            if second_highest == 2:
                return HandType.FullHouse
            else:
                return HandType.Three
        case 2:
            second_highest = counts[1][1]
            if second_highest == 2:
                return HandType.TwoPair
            else:
                return HandType.OnePair
        case 1:
            return HandType.HighCard

cards = ['A', 'K', 'Q', 'J', 'T', '9', '8', '7', '6', '5', '4', '3','2']
@functools.total_ordering
class Hand:
    def __init__(self,s,bid):
        self.s = s
        self.bid = bid
        self.type = determine_type(s)
    def __eq__(self, other):
        return self.s == other.s
    
    def get_card_scores(self):
        return [len(cards) - cards.index(c) for c in self.s]
    def __lt__(self, other):
        if self.type != other.type:
            return self.type < other.type
        else:
            return self.get_card_scores() < other.get_card_scores()
        
    def __repr__(self):
        return f"Hand({self.s})"


lines = load_input(7)
# for line in lines:
hand_str = "AA99A"
hands = []
determine_type(hand_str)
for line in lines:
    hand_str, bid = line.split(' ')
    bid_num = int(bid)
    hand = Hand(hand_str,bid_num)
    hands.append(hand)

sorted_cards = list(enumerate(sorted(hands),1))
total_winnings = sum([h.bid * i for (i,h) in sorted_cards])
print(total_winnings)