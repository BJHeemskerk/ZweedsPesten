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
    """ 
    Deze class definieert een speler met diens attributen, zoals naam en hand en de acties die de speler kan ondernemen tijdens diens beurt.
    
    Attributen:
        name (str): Naam van de speler.
        hidden_cards (list): De gesloten kaarten.
        displayed_cards (list): De kaarten die open liggen.
        hand_cards (list): De kaarten in de hand van de speler. 
    """



    
    def __init__(self, name):
        self.name = name
        self.hidden_cards = []
        self.displayed_cards = []
        self.hand_cards = []

    def remove_card(self, card, origin):
        """
        Deze method geeft aan dat een kaart uit de hand, die open ligt, of die gesloten ligt kan worden gebruikt / weggaat uit de inventory van de
        speler.

        Parameters:
        card: De kaart waar een speler een actie mee zal ondernemen.
        origin: Of de kaart uit de hand, van de kaarten die open liggen of van de kaarten die gesloten liggen komt.
        """
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
        """
        Deze method kiest willekeurig of 3 kaarten, of 1 kaart en stopt ze in  move. 

        Parameters:
        game_phase (str):
        playable_cards(list): De kaarten die mogen worden gespeeld.
        stack_of_cards(list):  Huidige speelstapel, maar wordt niet gebruikt in deze method.

        Return: 
        move(str): 
        """
        
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
        """
        Een functie die de strategie van Busse behandelt.

        Params:
        ----------
        hand : list
            De kaarten die valide zijn om te spelen
        
        game_phase : str
            De huidige fase van de game

        Returns:
        ----------
        move : str
            Een string die de kaart(en) bevat die gespeeld
            gaan worden op basis van de strategie
        """
        # De speciale kaarten die altijd speelbaar zijn
        special_cards = ["10", "2", "3"]

        # Strippen van de opties om de kaart waarden en suits uit elkaar te halen
        hand_stripped = [(card[0], card[1:]) for card in hand if card not in {"take", "skip"}]

        # List comprehension om speciale kaarten van normale kaarten te scheiden
        special = [card for card in hand_stripped if card[1] in special_cards]
        normal = [card for card in hand_stripped if card[1] not in special_cards]

        # Game Phase: Display Cards
        # Kiest de drie beste kaarten als display (speciale kaarten eerst)
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

        # Behandelen van skip en take indien dit de enige opties zijn
        if not special and not normal:
            if "skip" in hand:
                return "skip"
            else:
                return "take"

        # Behandelt de normale kaarten logic (laagste kaart opleggen)
        if normal:
            lowest_normal = min(
                normal,
                key=lambda card: CARD_VALUES[card[1]]
            )
            return "".join(lowest_normal)

        # Behandelt de speciale kaarten logic (eerst 10, dan 2 en 3 als laatste)
        return "".join(
            min(special, key=lambda card: special_cards.index(card[1]))
        )

    def play_move(self, game_phase, playable_cards, stack_of_cards):
        """
        Speelt de move gebaseerd op de game phase en strategie

        Params:
        ----------
        game_phase : str
            Een string die de game phase omschrijft
        
        playable_cards : list
            Een list die de legale moves bevat
        
        Stack_of_cards : list
            Lijst met de kaarten die op de stapel liggen,
            ongebruikt in deze strategie

        Returns:
        ----------
        De move die gespeeld wordt door de speler
        """
        # Behandel game phase display cards
        if game_phase == "choose_display_cards":
            return self.select_card(playable_cards, game_phase)
        else:
            # Behandel take action en normale zetten
            if "take" in playable_cards and len(playable_cards) > 1:
                playable_cards.remove("take")

            return self.select_card(playable_cards, game_phase)


class LowNoon(Player):
    """
    Strategie informatie:
    ----------
    Deze strategie speelt vaak de laagst mogelijke kaart beschikbaar.

    Bij de choose_display_cards fase prioriseert de strategie
    kaarten als de 2, 3 en 10 over hoge kaarten.
    """
    def select_card(self, hand, game_phase):
        """
        Een functie die de strategie van Busse behandelt.

        Params:
        ----------
        hand : list
            De kaarten die valide zijn om te spelen
        
        game_phase : str
            De huidige fase van de game

        Returns:
        ----------
        move : str
            Een string die de kaart(en) bevat die gespeeld
            gaan worden op basis van de strategie
        """
        # De speciale kaarten die altijd speelbaar zijn
        special_cards = ["10", "2", "3"]

        # Strippen van de opties om de kaart waarden en suits uit elkaar te halen
        hand_stripped = [(card[0], card[1:]) for card in hand if card not in {"take", "skip"}]

        # List comprehension om speciale kaarten van normale kaarten te scheiden
        special = [card for card in hand_stripped if card[1] in special_cards]
        normal = [card for card in hand_stripped if card[1] not in special_cards]

        # Game Phase: Display Cards
        # Kiest de drie beste kaarten als display (speciale kaarten eerst)
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

        # Behandelen van skip en take indien dit de enige opties zijn
        if not special and not normal:
            if "skip" in hand:
                return "skip"
            else:
                return "take"

        # Behandelt de normale kaarten logic (laagste kaart opleggen met 70%)
        choose_lowest = random.random() < 0.7
        complete_deviation = random.random() < 0.2  # 20% kans om compleet af te wijken
        
        if complete_deviation:
            return "".join(random.choice(hand_stripped))
        
        if normal:
            chosen_card = min(normal, key=lambda card: CARD_VALUES[card[1]]) if choose_lowest \
                          else max(normal, key=lambda card: CARD_VALUES[card[1]])
            return "".join(chosen_card)

        return "".join(min(special, key=lambda card: special_cards.index(card[1])))


    def play_move(self, game_phase, playable_cards, stack_of_cards):
        """
        Speelt de move gebaseerd op de game phase en strategie

        Params:
        ----------
        game_phase : str
            Een string die de game phase omschrijft
        
        playable_cards : list
            Een list die de legale moves bevat
        
        Stack_of_cards : list
            Lijst met de kaarten die op de stapel liggen,
            ongebruikt in deze strategie

        Returns:
        ----------
        De move die gespeeld wordt door de speler
        """
        # Behandel game phase display cards
        if game_phase == "choose_display_cards":
            return self.select_card(playable_cards, game_phase)
        else:
            # Behandel take action en normale zetten
            if "take" in playable_cards and len(playable_cards) > 1:
                playable_cards.remove("take")

            return self.select_card(playable_cards, game_phase)


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
            if len(playable_cards) > 0:
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
        
class Justice_and_Terror(Player):
    """

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
    
        Tim_play_values = {
            "2": 20,
            "3": 1,
            "4": 14,
            "5": 13,
            "6": 12,
            "7": 11,
            "8": 9,
            "9": 8,
            "10": 2,
            "J": 6,
            "Q": 5,
            "K": 4,
            "A": 3,
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
            scores = [Tim_play_values[card[1:]] for card in playable_cards]
            average_score = sum(scores) / len(scores)
            #print(playable_cards, average_score)
            if average_score < 4:
                return "skip"
            else:
                return playable_cards[-1]
            
        else:
            move = sorted(playable_cards, key=lambda card: LOW_play_values[card[1:]], reverse=False)[:1]
            return move[0]  

class Natasja(Player):
    """
    Strategie spelerstype Natasja:
    - Bij de open kaarten ligt er maximaal 1 keer een 3, waarna de hoogste kaarten (A, K, Q etc) worden gekozen.
    - Speelt normaalgesproken de laagste kaarten, maar wijkt hier eenmaal vanaf: 
    - Wanneer er 3 tot en met 7 kaarten op tafel liggen en het gemiddelde van CARD_VALUE is 8 of hoger pakt de speler de stapel (take)
    - Vervolgens, als er 5 of meer kaarten op tafel liggen en het gemiddelde van CARD_VALUE is 7.5 of lager, dan wordt er een Q, of anders een K,
       of anders een A opgelegd. Zo loopt een volgende speler een groot risico om een grotere stapel te moeten pakken en heeft de speler
       een grotere kans om hogere kaarten in handen te hebben.
    - Speciale kaarten worden in volgorde 2 → 10 → 3 gespeeld. 

    <Nog aanvullen: Parameters>
    """
    
    def __init__(self, name):
        super().__init__(name)
        self.has_used_q_strategy = False
        self.has_taken_stack = False
        self.has_displayed_3 = False

        self.CARD_VALUES = {
                "2": 15,
                "3": 20,
                "4": 4,
                "5": 5,
                "6": 6,
                "7": 7,
                "8": 8,
                "9": 9,
                "10": 16,
                "J": 11,
                "Q": 12,
                "K": 13,
                "A": 14
            }

    def calculate_stack_average(self, stack, exclude_specials=False):
        """Bereken gemiddelde waarde van aflegstapel, negeer speciale kaarten
        Nog aanvullen: Parameters, return. Ook bij alle andere methods van deze class.
        """
        if not stack:
            return 0
            
        total = 0
        count = 0
        
        for card in stack:
            value = card[1:] 
            if exclude_specials and value in ["2", "3", "10"]:
                continue
                
            card_value = self.CARD_VALUES.get(value, 0)
            if isinstance(card_value, int):
                total += card_value
                count += 1
                
        return total / count if count > 0 else 0

    def select_card(self, hand, game_phase, stack_of_cards, origin):
        """Gewone strategie en speciale Q-strategie"""
        clean_hand = [card for card in hand if card not in {"take", "skip"}]
        
        # Game Phase: Display Cards
        if game_phase == "choose_display_cards":
            display_cards = []
            remaining_cards = clean_hand.copy()
            
            # Maximaal maar eenmaal een 3 bij de open kaarten
            threes = [card for card in remaining_cards if card[1:] == "3"]
            if threes and not self.has_displayed_3:
                display_cards.append(threes[0])
                remaining_cards.remove(threes[0])
                self.has_displayed_3 = True

            # Daarna de hoogste kaarten die open liggen
            remaining_cards.sort(
                key=lambda card: self.CARD_VALUES.get(card[1:], 0),
                reverse=True
            )
            display_cards.extend(remaining_cards[:3 - len(display_cards)])
            return display_cards[:3]  # Ensure exactly 3 cards

        # Als de hand is uitgespeeld, speel dan eerst een 3 bij displayed kaarten.
        if origin == "displayed":
            threes = [card for card in clean_hand if card[1:] == "3"]
            if threes:
                return threes[0]

        # Game Phase: Main
        special_order = ["2", "10", "3"]  # Prioriteitsvolgorde
        specials = [card for card in clean_hand if card[1:] in special_order]
        normals = [card for card in clean_hand if card[1:] not in special_order]
        
        # Speciale strategie: maximaal 1 keer take (als er de optie is voor take en voor niet take)
        if (not self.has_taken_stack and 
            3 <= len(stack_of_cards) <= 7 and 
            self.calculate_stack_average(stack_of_cards) > 8 and 
            "take" in hand):
            self.has_taken_stack = True
            return "take"
            
        # Q-strategie (eenmalig)
        if (not self.has_used_q_strategy and 
            len(stack_of_cards) >= 3 and 
            self.calculate_stack_average(stack_of_cards, exclude_specials=True) < 8):
            
            for value in ["Q", "K", "A"]:
                high_cards = [card for card in normals if card[1:] == value]
                if high_cards:
                    self.has_used_q_strategy = True
                    return high_cards[0]
        
        for special_type in special_order:
            specials_of_type = [card for card in specials if card[1:] == special_type]
            if specials_of_type:
                return specials_of_type[0]
        
        if normals:
            return min(
                normals,
                key=lambda card: self.CARD_VALUES.get(card[1:], float('inf'))
            )
            
        if "skip" in hand:
            return "skip"
        return "take" if "take" in hand else None

    def play_move(self, game_phase, playable_cards, stack_of_cards):
        """Pas de strategie toe op basis van game fase"""
        if game_phase == "choose_display_cards":
            return self.select_card(playable_cards, game_phase, stack_of_cards, None)
        else:
            if "take" in playable_cards and len(playable_cards) > 1:
                playable_cards.remove("take")
            if len(self.hand_cards) > 0:
                origin = "hand"
            elif len(self.displayed_cards) > 0:
                origin = "displayed"
            else:
                origin = "hidden"
                
            return self.select_card(playable_cards, game_phase, stack_of_cards, origin)