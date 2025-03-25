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
    Strategie informatie:
    ----------
    Deze strategie kijkt naar de bovenste kaart van de stack
    en speelt vervolgens de laagst beschikbare valid card.

    Bij de choose_display_cards fase prioriseert de strategie
    kaarten als de 2, 3 en 10 over hoge kaarten.
    """
    def select_card(self, hand, game_phase):
        special_cards = ["10", "2", "3"]

        hand_stripped = [(card[0], card[1:]) for card in hand if card not in {"take", "skip"}]

        special = [card for card in hand_stripped if card[1] in special_cards]
        normal = [card for card in hand_stripped if card[1] not in special_cards]

        if game_phase == "choose_display_cards":
            amount_chosen = 0
            chosen_display_cards = []
            while amount_chosen != 3:
                if special:
                    card = max(
                        special,
                        key=lambda card: special_cards.index(card[1])
                    )
                    full_card = "".join(card)
                    chosen_display_cards.append(full_card)
                    special.remove(card)
                else:
                    card = max(
                        normal,
                        key=lambda card: CARD_VALUES[card[1]]
                    )
                    full_card = "".join(card)
                    chosen_display_cards.append(full_card)
                    normal.remove(card)

                amount_chosen += 1
            return chosen_display_cards

        if not special and not normal:
            if "skip" in hand:
                return "skip"
            else:
                return "take"

        if normal:
            lowest_normal = min(
                normal,
                key=lambda card: CARD_VALUES[card[1]]
            )
            return "".join(lowest_normal)

        return "".join(
            min(special, key=lambda card: special_cards.index(card[1]))
        )

    def play_move(self, game_phase, playable_cards, stack_of_cards):
        if game_phase == "choose_display_cards":
            return self.select_card(playable_cards, game_phase)
        else:
            if "take" in playable_cards and len(playable_cards) > 1:
                playable_cards.remove("take")

            return self.select_card(playable_cards, game_phase)


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
