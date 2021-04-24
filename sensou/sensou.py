import random


class Deck():
    def __init__(self):
        self.cards = [
            (i, j)
            for i in range(1, 14)
            for j in ['h', 'd', 'k', 's']
        ]
        random.shuffle(self.cards)

    def emission(self):
        emission_card = self.cards.pop()
        return emission_card


def point(card):
    point = card[0]
    if point == 1:
        return 14
    else:
        return point

