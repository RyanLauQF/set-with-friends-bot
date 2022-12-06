import random

COLOURS = ["red", "purple", "green"]
SHAPES = ["oval", "squiggle", "diamond"]
NUMBERS = [1, 2, 3]
SHADING = ["solid", "striped", "outline"]


class Card:
    def __init__(self, colour, shape, number, shading, id):
        self.colour = colour
        self.shape = shape
        self.number = number
        self.shading = shading
        self.id = id

    def print_card(self):
        print(self.colour, self.shape, self.number, self.shading)


def find_set(dealt):
    combinations = generate_all_sets([], [], 0, dealt, len(dealt))
    # go through each combination and find the sets
    for card_set in combinations:
        if is_set(card_set):
            return card_set


""" 
    # input is a set of 3 cards
    # check if they are a set
    Set Rules:
        all same or all different for every category
"""


def is_set(card_set):
    colour_condition = False
    shape_condition = False
    num_condition = False
    shade_condition = False

    # check colour
    unique_set = {card.colour for card in card_set}
    if len(unique_set) == 1 or len(unique_set) == 3:
        colour_condition = True

    # check shape
    unique_set = {card.shape for card in card_set}
    if len(unique_set) == 1 or len(unique_set) == 3:
        shape_condition = True

    # check number
    unique_set = {card.number for card in card_set}
    if len(unique_set) == 1 or len(unique_set) == 3:
        num_condition = True

    # check shading
    unique_set = {card.shading for card in card_set}
    if len(unique_set) == 1 or len(unique_set) == 3:
        shade_condition = True

    return colour_condition and shape_condition and num_condition and shade_condition


# generates all possible combinations of sets that have been dealt
def generate_all_sets(combinations, curr_set, index, dealt_cards, length):
    if len(curr_set) == 3:
        combinations.append(curr_set.copy())
        return combinations

    for i in range(index, length):
        curr_set.append(dealt_cards[i])
        generate_all_sets(combinations, curr_set, i + 1, dealt_cards, length)
        curr_set.pop()

    return combinations


def init_game():
    deck = []
    unique_id = 0
    for colour in COLOURS:
        for shape in SHAPES:
            for num in NUMBERS:
                for shade in SHADING:
                    deck.append(Card(colour, shape, num, shade, unique_id))
                    unique_id += 1

    # random.seed(10)
    random.shuffle(deck)

    # deal 12 cards
    dealt = []

    for i in range(12):
        dealt.append(deck.pop())

    # print()
    # # prints all dealt cards
    # for c in dealt:
    #     c.print_card()
    # print()
    counter = 0
    while len(deck) >= 0:
        # finds a set in dealt cards
        found_set = find_set(dealt)

        if not found_set and len(deck) == 0:
            break

        if found_set:
            counter += 1
            # for c in found_set:
            #     c.print_card()
            # print()

            # remove the 3 cards from set
            card_id = {card.id for card in found_set}
            dealt = [card for card in dealt if card.id not in card_id]

        if len(deck) != 0:
            # deal 3 extra cards
            for i in range(3):
                dealt.append(deck.pop())
    print("Final Cards Left:")
    print()
    for c in dealt:
        c.print_card()
    print()
    print("GAME ENDED!")
    print("Sets found:", counter)


def main():
    init_game()


if __name__ == "__main__":
    main()
