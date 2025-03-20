"""
Dit is een script waarbij alle spelers en
de bijbehorende strategieen zich bevinden
"""

import random

CARD_VALUES = {
                "2": "two",
                "3": 20,
                "4": 4,
                "5": 5,
                "6": 6,
                "7": 7,
                "8": 8,
                "9": 9,
                "10": "ten",
                "J": 11,
                "Q": 12,
                "K": 13,
                "A": 14
            }


class Player():
    def __init__(self, name):
        self.name = name
        self.hidden_cards = []
        self.displayed_cards = []
        self.hand_cards = []

    def remove_card(self, card, origin):
        if origin == "hand":
            self.hand_cards.remove(card)
        elif origin == "displayed":
            self.displayed_cards.remove(card)
        elif origin == "hidden":
            if card in self.hidden_cards:
                self.hidden_cards.remove(card)
            else:
                self.hand_cards.remove(card)

    def play_move(self, game_phase, playable_cards, stack_of_cards):
        """Default strategy (random choice)."""
        move = []

        if game_phase == "choose_display_cards":
            move = random.sample(playable_cards, 3)
            return move
        else:
            if "take" in playable_cards and len(playable_cards) > 1:
                playable_cards.remove("take")

            move = random.choice(playable_cards) if playable_cards else "take"
            return move


class Busse(Player):
    """
    Speelt altijd de hoogst mogelijke kaart
    """
    def play_move(self, game_phase, playable_cards, stack_of_cards):
        if game_phase == "choose_display_cards":
            move = sorted(playable_cards, key=lambda card: CARD_VALUES[card[1:]], reverse=True)[:3]
            return move
        else:
            if "take" in playable_cards and len(playable_cards) > 1:
                playable_cards.remove("take")

            move = max(playable_cards, key=lambda card: CARD_VALUES[card[1:]]) if playable_cards else "take"
            return move


class Tim(Player):
    """
    Speelt altijd de hoogst mogelijke kaart
    """
    def play_move(self, game_phase, playable_cards, stack_of_cards):
        if game_phase == "choose_display_cards":
            move = sorted(playable_cards, key=lambda card: CARD_VALUES[card[1:]], reverse=True)[:3]
            return move
        else:
            if "take" in playable_cards and len(playable_cards) > 1:
                playable_cards.remove("take")

            move = max(playable_cards, key=lambda card: CARD_VALUES[card[1:]]) if playable_cards else "take"
            return move
