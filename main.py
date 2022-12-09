import sys
import random
import connect

from card import Card

COLOURS = ['red', 'purple', 'green']
SHAPES = ['oval', 'squiggle', 'diamond']
NUMBERS = [1, 2, 3]
SHADING = ['solid', 'striped', 'outline']


# runs a set with friends game simulation
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

    counter = 0
    while len(deck) >= 0:
        # finds a set in dealt cards
        found_set = find_set(dealt)

        if not found_set and len(deck) == 0:
            break

        if found_set:
            counter += 1

            # remove the 3 cards from set
            card_id = {card.uid for card in found_set}
            dealt = [card for card in dealt if card.uid not in card_id]

        if len(deck) != 0:
            # deal 3 extra cards
            for i in range(3):
                dealt.append(deck.pop())
    print("Final Cards Left:")
    print()
    for c in dealt:
        print(c)
    print()
    print("GAME ENDED!")
    print("Sets found:", counter)


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
    # check colour
    unique_set = {card.colour for card in card_set}
    if len(unique_set) != 1 and len(unique_set) != 3:
        return False

    # check shape
    unique_set = {card.shape for card in card_set}
    if len(unique_set) != 1 and len(unique_set) != 3:
        return False

    # check number
    unique_set = {card.number for card in card_set}
    if len(unique_set) != 1 and len(unique_set) != 3:
        return False

    # check shading
    unique_set = {card.shading for card in card_set}
    if len(unique_set) != 1 and len(unique_set) != 3:
        return False

    return True


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


def main():
    # init_game()
    connect.link_to_game()
    sys.exit(0)


if __name__ == "__main__":
    main()
