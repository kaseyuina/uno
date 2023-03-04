import random

class card:
    def __init__(self, color, number, points):
        self.color = color
        self.number = number
        self.points = points

class player:
    def __init__(self, cards, points, cpu):
        self.cards = cards
        self.points = points
        self.cpu = cpu
    def use_card(self, used_cards, top_card, card_pile, turn):
        #card_effect = [skip, reverse, draw, wild]
        card_effect = [0, 0, 0, False]
        if self.validate_cards(top_card, used_cards) == True:
            for i in used_cards:
                if (top_card[0].number == "wild" or "draw4") and not top_card[0].color == "-":
                    pass
                else:
                    card_pile.append(top_card[0])
                top_card[0] = self.cards[i - 1]
                print("Player" + str(turn + 1) + " used " + str(top_card[0].color) + " " + str(top_card[0].number))
                if top_card[0].number == "skip":
                    card_effect[0] += 2
                elif top_card[0].number == "reverse":
                    card_effect[1] += 1
                elif top_card[0].number == "draw2":
                    card_effect[2] += 2
                elif top_card[0].number == "draw4":
                    card_effect[2] += 4
                    card_effect[3] = True
                elif top_card[0].number == "wild":
                    card_effect[3] = True
            # print(card_effect[0])
            if card_effect[0] > 0:
                card_effect[0] -= 1
            # print(card_effect[0])

            used_cards.sort(reverse=True)
            # print("check2")
            for i in used_cards:
                self.cards.pop(i-1)
            # print("check3")
            return card_effect
        else:
            print("Please select valid card(s)")
            return False
        return 0
    def validate_cards(self, top_card, used_cards):
        first_card = self.cards[used_cards[0]-1]
        #top_card = card_pile[len(card_pile)-1]
        # print(str(first_card.color) + str(first_card.number) + " " + str(top_card.color) + (top_card.number))
        if first_card.color == "-" or top_card[0].color == first_card.color or top_card[0].number == first_card.number:
            for i in used_cards:
                if not first_card.number == self.cards[i-1].number:
                    return False
            return True
        return False

    def draw_card(self, uno_cards, card_pile, num_of_cards, turn):
        for i in range(num_of_cards):
            if len(uno_cards) == 0:
                uno_cards = card_pile
                random.shuffle(uno_cards)
                card_pile = []
            self.cards.append(uno_cards[0])
            uno_cards.pop(0)
        print("Player" + str(turn + 1) + " drew " + str(num_of_cards) + " cards")
        return 0

    def display_cards(self):
        for i in range(len(self.cards)):
            print(str(i+1) + ": " + str(self.cards[i].color) + ", " + str(self.cards[i].number))
        print("")

        return 0

