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

# Logic depends on which part is being solved
# Lord have mercy upon me
PART = 1

cards_1 = ['A', 'K', 'Q', 'J', 'T', '9', '8', '7', '6', '5', '4', '3','2']

cards_2 = ['A', 'K', 'Q', 'T', '9', '8', '7', '6', '5', '4', '3','2', 'J']

def determine_type(s, jokers = False):
    counter = Counter(s)
    counter_map = dict(counter)
    # Current problem: there is no tie-breaking depending on card value where the joker assumes the value of the highest card of a certain value
    # For instance, "AAKKJ" should become a Three of A not K
    counts = list(sorted(list(counter.items()), key=lambda x: -x[1]))
    highest = counts[0][1]
    if jokers:
        highest_is_joker = counts[0][0] == 'J'
        if not highest_is_joker and 'J' in counter_map:
            no_jokers = counter_map['J']
            print(f"{s} contains {no_jokers} jokers; Increasing highest ({highest}) by {no_jokers}")
            highest += no_jokers
            for i in range(len(counts)):
                if counts[i][0] == 'J':
                    counts[i] = ('J',0)
                    break    
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

@functools.total_ordering
class Hand:
    def __init__(self,s,bid = 0):
        self.s = s
        self.bid = bid
        self.type = determine_type(s, jokers = PART == 2)

    def __eq__(self, other):
        return self.s == other.s
    
    def get_card_scores(self):
        cards = cards_1 if PART == 1 else cards_2
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
print(sorted_cards)

total_winnings = sum([h.bid * i for (i,h) in sorted_cards])
print(total_winnings)

PART = 2

for hand in hands:
    hand.type = determine_type(hand.s, jokers = PART == 2)
    print(hand,hand.type,'\n')

sorted_cards = list(enumerate(sorted(hands),1))
print(sorted_cards)
total_winnings = sum([h.bid * i for (i,h) in sorted_cards])
print(total_winnings)

assert(Hand("QQQQ2") > Hand("JKKK2"))