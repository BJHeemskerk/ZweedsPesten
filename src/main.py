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
    probeer hogen kaarten te pakken
    """
    def play_move(self, game_phase, playable_cards, stack_of_cards):
        Tim_setup_values = {
            "2": 20,
            "3": 50,
            "4": 6,
            "5": 7,
            "6": 8,
            "7": 9,
            "8": 2,
            "9": 1,
            "10": 19,
            "J": 3,
            "Q": 4,
            "K": 5,
            "A": 18,
        }
        Tim_take_values = {
            "2": 20,
            "3": 20,
            "4": -25,
            "5": -10,
            "6": -5,
            "7": -5,
            "8": 5,
            "9": 10,
            "10": 20,
            "J": 15,
            "Q": 16,
            "K": 18,
            "A": 20,
        }

        Tim_play_values = {
            "2": 2,
            "3": 1,
            "4": 14,
            "5": 13,
            "6": 12,
            "7": 11,
            "8": 9,
            "9": 8,
            "10": 7,
            "J": 6,
            "Q": 5,
            "K": 4,
            "A": 3,
        }

        if game_phase == "choose_display_cards":
            move = sorted(playable_cards, key=lambda card: Tim_setup_values[card[1:]], reverse=True)[:3]
            return move
        
        elif game_phase == "main":
            if len(self.displayed_cards) > 2 and len(playable_cards) > 1 and len(stack_of_cards) > 0:
                playable_cards.remove("take")
                scores = [Tim_take_values[card[1:]] for card in stack_of_cards]
                average_score = sum(scores) / len(scores) 
                #print("average_score:", average_score)
                if average_score > 17:
                    return "take"
                else:
                    playable_cards.append("take")

                
            if "take" in playable_cards and len(playable_cards) > 1:
                playable_cards.remove("take")  

                move = sorted(playable_cards, key=lambda card: Tim_play_values[card[1:]], reverse=True)[:1]
                return move[0]
            
            else:
                return "take"


        elif game_phase == "double_card":
            playable_cards.remove("skip")
            scores = [Tim_play_values[card[1:]] for card in playable_cards]
            average_score = sum(scores) / len(scores)
            if average_score < 4:
                return "skip"
            else:
                return playable_cards[-1]
            
        elif game_phase == "free_card":
            move = sorted(playable_cards, key=lambda card: Tim_play_values[card[1:]], reverse=True)[:1]
            return move[0]

class Low(Player):
    """
    Speelt altijd de laagste mogelijk kaart
    """
    def play_move(self, game_phase, playable_cards, stack_of_cards):

        LOW_play_values = {
            "2": 12,
            "3": 14,
            "4": 2,
            "5": 3,
            "6": 4,
            "7": 5,
            "8": 6,
            "9": 7,
            "10": 13,
            "J": 8,
            "Q": 9,
            "K": 10,
            "A": 11,
        }

        if game_phase == "choose_display_cards":
            move = sorted(playable_cards, key=lambda card: LOW_play_values[card[1:]], reverse=True)[:3]
            return move
        
        if game_phase == "main":
            if len(playable_cards) > 1:
                if "take" in playable_cards:
                    playable_cards.remove("take") 
                    move = sorted(playable_cards, key=lambda card: LOW_play_values[card[1:]], reverse=True)[:1]
                    return move[0]  
            else:
                return "take"

        if game_phase == "double_card":
            playable_cards.remove("skip")
            move = sorted(playable_cards, key=lambda card: LOW_play_values[card[1:]], reverse=True)[:1]
            return move[0]
            
        else:
            move = sorted(playable_cards, key=lambda card: LOW_play_values[card[1:]], reverse=True)[:1]
            return move[0]      
        


class Jasper(Player):
    """
    lage kaarten vroeg kwijt te raken. 
    """
    """
    Speelt altijd de laagste mogelijk kaart
    """
    def play_move(self, game_phase, playable_cards, stack_of_cards):

        LOW_play_values = {
            "2": 12,
            "3": 14,
            "4": 2,
            "5": 3,
            "6": 4,
            "7": 5,
            "8": 6,
            "9": 7,
            "10": 13,
            "J": 8,
            "Q": 9,
            "K": 10,
            "A": 11,
        }

        if game_phase == "choose_display_cards":
            move = sorted(playable_cards, key=lambda card: LOW_play_values[card[1:]], reverse=True)[:3]
            return move
        
        if game_phase == "main":
            if len(playable_cards) > 1:
                if "take" in playable_cards:
                    playable_cards.remove("take") 
                    move = sorted(playable_cards, key=lambda card: LOW_play_values[card[1:]], reverse=False)[:1]
                    return move[0]  
            else:
                return "take"

        if game_phase == "double_card":
            playable_cards.remove("skip")
            move = sorted(playable_cards, key=lambda card: LOW_play_values[card[1:]], reverse=False)[:1]
            return move[0]
            
        else:
            move = sorted(playable_cards, key=lambda card: LOW_play_values[card[1:]], reverse=False)[:1]
            return move[0]      