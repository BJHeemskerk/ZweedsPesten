"""
In dit python script staat de code die is gebruikt om
het spel zweeds pesten om te toveren van een tabletop
card game naar een python based simulatie.
"""

# Importeren van gebruikte libraries
import random
import matplotlib.pyplot as plt
import pandas as pd
from itertools import combinations, permutations
from IPython.display import display
import numpy as np
import seaborn as sns
from collections import defaultdict
import matplotlib.colors as mcolors
from main import Player, Tim, Low, Jasper, Busse, Justice_and_Terror, Natasja, HighNoon



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


class ZweedsPesten():
    """ 
    Deze class definieert een ronde van het spel Zweeds Pesten, als object.
    
    Attributen:
        players (list): De namen van de speler-objecten
        stack_of_cards (list): De aftrekstapel
        winners (str): De naam van de speler die heeft gewonnen: goud, zilver, brons.
        placements (dict): Een dictionary die de eindpositie van de players aangeeft
        deck(list): Een lijst met te gebruiken kaarten in het spel.
        score_map (dict): Een mapping die eindposities vertaalt naar score. Door meerdere potjes te spelen kan er een uiteindelijke winnaar worden bepaald.
    """



    
    def __init__(self, players):
        """
        Constructor waarin players, stack_of_cards, winners en placements worden geinitialiserd en de score_map wordt toegewenzen in het ZweedsPesten-object.

        Parameters:
        self (ZweedsPesten): Het huidige ZweedsPesten-object.
        players (list): De lijst met spelers.

        """

        
        player_types = {
            "busse": Busse,
            "tim": Tim,
            "low": Low,
            "jasper" : Jasper,
            "justice_and_terror": Justice_and_Terror,
            "natasja": Natasja,
            "high_noon": HighNoon
        }

        self.players = [player_types.get(name, Player)(name) for name in players]
        self.stack_of_cards = []
        self.winners = []
        self.placements = {}

        self.score_map = {0: 3, 1: 2, 2: 1}

    def get_player_instance(self, name):
        """
        Een getter voor player_type objects van het Player object.

        Attributes:
        name (str): Naam van de gewenste strategie (zoals "tim" of "busse"). 

        Return:
        Player (object): Haalt een speler op als de strategienaam bekend is (zoals "tim" of "busse"). Als de spelernaam niet in de lijst voorkomt wordt er een 
        standaard Player aangemaakt en die krijgt dan de ingevoerde naam. 

        """
        player_types = {
            "busse": Busse,
            "tim": Tim,
            "low": Low,
            "jasper" : Jasper,
            "justice_and_terror": Justice_and_Terror,
            "natasja": Natasja,
            "high_noon": HighNoon
        }

        return player_types.get(name, Player)(name)

    def create_deck(self):
        """
        Creeert een kaartspel

        Return:
        anoniem object (list): list met een kleur voor elk cijfer/plaatje van de kaarten in het formaat <kleur><waarde>

        
        """
        ranks = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
        suits = ["♠", "♥", "♦", "♣"]

        return [f"{suit}{rank}" for rank in ranks for suit in suits]

    def draw_card(self, deck, hand):
        """
        Trekt 1 kaart van de stapel zolang er nog kaarten zijn. 

        Parameters:
        deck (list): De stapel kaarten waarvan getrokken kan worden.
        hand (list): Kaarten in de hand.
        
        """
        if deck:
            hand.append(deck.pop())

    def starting_hand(self, selected_players):
        for player in selected_players:
            for _ in range(3):
                self.draw_card(self.deck, player.hidden_cards)
            for _ in range(6):
                self.draw_card(self.deck, player.hand_cards)

    def valid_cards(self, hand, top_card):
        """
        Bepaalt welke kaarten mogen worden gespeeld.

        Parameters:
        hand (list): De kaarten in de hand
        top_card (str): De laatste kaart die is gelegd.

        Return:
        

        """
        top_card_value = CARD_VALUES[top_card[1:]]

        valid_cards = []

        if top_card_value == "ten":
            try: 
                index = -1
                while top_card[1:] == "10":
                    top_card = self.stack_of_cards[index]
                    index -= 1
                    top_card_value= CARD_VALUES[top_card[1:]]

            except IndexError:
                top_card_value = 1

        if top_card_value == "two":
            top_card_value = 2

        for card in hand:
            card_value = CARD_VALUES[card[1:]]

            if isinstance(card_value, str):
                valid_cards.append(card)
            elif top_card_value == 7 and card_value < 7:
                valid_cards.append(card)
            elif top_card_value != 7 and card_value >= top_card_value:
                valid_cards.append(card)

        return valid_cards
    
    def check_win(self, player):
        """
        Kijkt of de speler heeft gewonnen, wat het geval is als diens hand leeg is, hij geen open en geen gesloten kaarten meer voor zich heeft liggen.

        Parameters:
        player (Player): controleert of de hand van de speler leeg is

        Return:
        True / False (boolean): Heeft de speler gewonnen of niet.?

        
        
        """
        return all(len(cards) == 0 for cards in [player.hand_cards, player.displayed_cards, player.hidden_cards])
        
    def possible_moves(self, player):
        """
        Geeft aan welke zetten de speler kan doen. Eerst moet de speler al zijn kaarten uitspelen, daarna de kaarten die open liggen en daarna de
        kaarten die gesloten liggen. Ook kan een speler altijd voor "take" kiezen, wat inhoudt dat de speler een kaart van de aftrekstapel mag pakken.

        Parameters:
        player (Player): Om te controleren of de speler nog kaarten in zijn hand heeft. 

        Return:
        playable_cards: De speelbare kaarten in de hand van de speler plus de optie voor "take". 
        origin (str): Of de kaart uit de hand kwam, van de open kaarten of van de gesloten kaarten.

        """
        if len(player.hand_cards) > 0:
            available_cards = player.hand_cards
            origin = "hand"

        elif len(player.displayed_cards) > 0:
            available_cards = player.displayed_cards
            origin = "displayed"

        else:
            available_cards = [player.hidden_cards[-1]]
            origin = "hidden"
                       
        if len(self.stack_of_cards) > 0:
            top_card = self.stack_of_cards[-1]
            playable_cards = self.valid_cards(available_cards, top_card)
            playable_cards.append("take")
        else:
            playable_cards = available_cards.copy()

        return playable_cards, origin

    def possible_available_cards(self, player):
        """
        Geeft de kaarten aan die een speler ter beschikking eheft.

        Parameter:
        player (Player): om te kijken of een speler nog kaarten heeft.

        Return:
        available_cards (list): De kaarten in de hand van de speler.
        origin (str): Waar de kaarten vandaan kwamen (hand of open kaart)
        """
        if len(player.hand_cards) > 0:
            available_cards = player.hand_cards
            origin = "hand"

        elif len(player.displayed_cards) > 0:
            available_cards = player.displayed_cards
            origin = "displayed"

        return available_cards, origin
    
    def filter_list(self, lst, x):
        """
        Kijkt of een kaart het cijfer / het plaatje heeft dat is opgegeven bij x. 

        Parameter
        lst (list): Lijst van kaarten in gewoon formaat (<kleur><waarde>)
        x (str): De naam van een plaatje (J/Q/K/A) of een cijfer (2 tot en met 9)
        
        return:
        (list): Lijst met kaarten die voldoen aan waarde x.
        
        """

        return [item for item in lst if x in item[1:]]
    
    def check_4(self):
        """
        Kijkt of er sprake is van vier dezelfde plaatjes / cijfers achterelkaar op de oplegstapel. Een tien die ertussen is gekomen
        telt niet mee. 
        """
        
        lst = [x[1:] for x in self.stack_of_cards[-4:]]

        if len(set(lst)) == 1:
            if len(lst) < 4:
                return False
            return True
        
        elif "10" in set(lst) and len(set(lst)) == 2:
            filtered_lst = [x[1:] for x in reversed(self.stack_of_cards) if x[1:] != "10"]
            if len(filtered_lst) < 4:
                return False
            return len(set(filtered_lst[:4])) == 1
        
        else:
            return False
    
    def game_loop(self, verbose=1, selected_players=None):
        """
        Runt een ronde Zweeds Pesten, waarbij alle fases van het spel, de beurten van de spelers en speciale effecten van kaarten voorbijkomen.
        
        verbosity:
            0 - Silent (no prints)
            1 - Winners only
            2 - Full verbose (detailed game state)
        """
        if selected_players is None:
            selected_players = self.players[:4]

        game_phase = "choose_display_cards"
        self.winners = []

        self.deck = self.create_deck()
        random.shuffle(self.deck)
        self.starting_hand(selected_players)

        for player in selected_players:
            playable_cards = player.hand_cards
            player.displayed_cards = player.play_move(game_phase, playable_cards,self.stack_of_cards)
            for card in player.displayed_cards:
                player.hand_cards.remove(card)

        if verbose == 2:
            print("\n------------ Starting Game ------------")
            for player in selected_players:
                print(f"{player.name}:")
                print(f"Hand:       {player.hand_cards}")
                print(f"Displayed:  {player.displayed_cards}")
                print(f"Hidden:     {player.hidden_cards}")
                print("-----------------------------------------")
        len_game = 0
        while len(self.winners) + 1 < len(selected_players):
            while len_game != 250:
                for player in selected_players:
                    if self.check_win(player):
                        if player.name not in self.winners:
                            if verbose >= 1:
                                print(f"\n{player.name} has won the game!")
                            self.winners.append(player.name)
                            break
                        continue

                    if len(self.winners) + 1 == len(selected_players):

                        if verbose >= 1:
                            print(f"\n{player.name} is the last remaining player. No further turns needed.")
                        break

                    game_phase = "main"
                    playable_cards, origin = self.possible_moves(player)

                    if verbose == 2:
                        print(f"\n{player.name}'s turn")
                        print(f"Top of stack:   {self.stack_of_cards[-1] if self.stack_of_cards else 'Empty'}")
                        print(f"Hand:       {player.hand_cards}")
                        print(f"Displayed:  {player.displayed_cards}")
                        print(f"Hidden:     {player.hidden_cards}")

                        print(f"\nPlayable cards: {playable_cards}")

                    move = player.play_move(game_phase, playable_cards, self.stack_of_cards)

                    if move == "take":
                        if verbose == 2:
                            print(f"{player.name} takes the stack ({len(self.stack_of_cards)} cards).")
                        player.hand_cards.extend(self.stack_of_cards)
                        self.stack_of_cards.clear()
                    else:
                        if verbose == 2:
                            print(f"{player.name} plays {move} from {origin}.")
                        self.stack_of_cards.append(move)
                        player.remove_card(move, origin)

                    special_cards_repeat = True
                    while special_cards_repeat and not self.check_win(player):
                        special_cards_repeat = False

                        if move[1:] == "3":
                            self.stack_of_cards.clear()
                            if verbose == 2:
                                print(f"{player.name} played a 3 - Stack cleared!")
                            if not self.check_win(player):
                                special_cards_repeat = True
                                game_phase = "free_card"
                                playable_cards, origin = self.possible_moves(player)
                                if verbose == 2:
                                    print(f"Top of stack:   {self.stack_of_cards[-1] if self.stack_of_cards else 'Empty'}")
                                    print(f"Playable cards: {playable_cards}")
                                move = player.play_move(game_phase, playable_cards, self.stack_of_cards)
                                self.stack_of_cards.append(move)
                                player.remove_card(move, origin)

                        if len(player.hand_cards) + len(player.displayed_cards) > 0:
                            available_cards, origin = self.possible_available_cards(player)
                            card_values = [card[1:] for card in available_cards]

                            if move[1:] in card_values:
                                special_cards_repeat = True
                                while move[1:] in card_values and len(player.hand_cards) + len(player.displayed_cards) > 0 and not self.check_win(player):
                                    playable_cards = self.filter_list(available_cards, move[1:])
                                    playable_cards.append("skip")

                                    if verbose == 2:
                                        print(f"{player.name} can play a double card ({move[1:]}).")

                                    game_phase = "double_card"
                                    move = player.play_move(game_phase, playable_cards, self.stack_of_cards)

                                    if move == "skip":
                                        if verbose == 2:
                                            print(f"{player.name} skipped playing a double card.")
                                        break
                                    else:
                                        if verbose == 2:
                                            print(f"{player.name} plays {move} from {origin}.")
                                        self.stack_of_cards.append(move)
                                        player.remove_card(move, origin)

                                        if len(player.hand_cards) + len(player.displayed_cards) > 0:
                                            available_cards, origin = self.possible_available_cards(player)
                                            card_values = [card[1:] for card in available_cards]

                        if self.check_4():
                            special_cards_repeat = True
                            self.stack_of_cards.clear()
                            if verbose == 2:
                                print(f"Four of a kind detected - Stack cleared!")
                            game_phase = "free_card"
                            playable_cards, origin = self.possible_moves(player)
                            move = player.play_move(game_phase, playable_cards, self.stack_of_cards)
                            self.stack_of_cards.append(move)
                            player.remove_card(move, origin)

                        while len(player.hand_cards) < 3 and len(self.deck) > 0:
                            drawn_card = self.deck.pop()
                            player.hand_cards.append(drawn_card)
                            if verbose == 2:
                                print(f"{player.name} draws a card: {drawn_card}")

                    if self.check_win(player):
                        if verbose >= 1:
                            print(f"{player.name} has won the game!")
                        self.winners.append(player.name)

                len_game += 1
            if len_game == 250:
                while len(self.winners) < 3:
                    self.winners.append(None)
                break

        if verbose >= 1:
            print("\nGame over! Winners in order:", self.winners)

    def simulate_games(self, sims, verbose=0):
        """
        Deze code simuleert meerdere potjes Zweeds Pesten voor alle mogelijke volgordes van spelers, houdt bij wie er wint en laat uiteindelijk de volgorde  
        waarin de spelers het potje hebben gespeeld en de resultaten bij in self.placements (dict).

        Parameters:
        sims (int): Aantal simulatierondes
        verbose = 0 (int): Er wordt niks geprint

        """
        self.placements = {}

        # Maken van de tabel
        self.performance_data = pd.DataFrame(
            index=[
                player.name for player in self.players
            ]
        )
        self.performance_data["Aantal Games"] = {player: 0 for player in self.performance_data.index}

        # Maken van alle namen combinaties
        player_names = [player.name for player in self.players]
        group_combinations = list(combinations(player_names, 4))

        # Maken van permutaties van elke combinatie
        all_permutations = []
        for group in group_combinations:
            all_permutations.extend(permutations(group))

        # Maken van dict voor berekening dominantie
        self.dominance_data = {}

        for perm in all_permutations:
            if verbose >= 2:
                print(f"\nSimulating with player order: {perm}")  

            for i in range(sims):
                # Maak een nieuwe game met deze permutatie van spelers
                selected_players = [self.get_player_instance(name) for name in perm]
                self.game_loop(verbose=verbose, selected_players=selected_players)
                self.placements[f"Game {i + 1} (Order: {perm})"] = self.winners

                # Ophalen van de beste speler bij elke permutatie
                if perm not in self.dominance_data:
                    self.dominance_data[perm] = []
                self.dominance_data[perm].append(self.winners[0])

                # Optellen aantal games per speler
                for player_name in perm:
                    self.performance_data.loc[player_name, "Aantal Games"] += 1

                if verbose >= 1:
                    print("Game:", i)

        # Uitprinten en tonen resultaten
        print("Algemene performance in nummers:")
        display(self.performance_table(self.placements))

        print("Overwinningen vanaf verschillende startplekken:")
        self.wins_per_start()
        plt.show()

        print("Punten en Podium verdeling:")
        self.display_points()
        plt.show()

        print("Performance per speler per combinatie van spelers:")
        self.combination_results()
        plt.show()

    def display_points(self):
        """
        Berekent de totale scores, toont hoe vaak ze in de top 3 zijn gekomen en visualiseert de resultaten door middel van een staafdiagram.
        """
        fig, ax1 = plt.subplots(figsize=(25, 6))

        self.points.plot(kind="bar", color="black", alpha=0.6)
        ax1.set_xlabel("Players")
        ax1.tick_params(axis="x", rotation=0)
        ax1.set_ylabel("Totale Punten (zwarte bar)", color="blue")
        ax1.tick_params(axis="y", labelcolor="blue")

        ax2 = ax1.twinx()

        valid_players = [p for p in self.points.index if p in self.medals.index and p is not None]

        self.medals.loc[valid_players].plot(kind="bar", ax=ax2, width=0.3, color=["gold", "silver", "brown"])
        ax2.set_ylabel("Aantal keren 1st/2nd/3rd (goud/zilver/brons)", color="black")
        ax2.tick_params(axis="y", labelcolor="black")

        plt.title("Totale punten en podiums")

        ax2.get_legend().remove()
        
    def performance_table(self, placements):
        """
        Deze method toont de performance van elke speler op basis van meerdere
        statistieken en zorgt voor een numeriek overzicht van de performance.
        
        Parameters:
        placements (dict): Dictionary met game-uitslagen in vorm {"Game X (Order:...)": [winnaar1, winnaar2,...]}
        """
        # Aanmaken dataframe op basis van placements
        data = pd.DataFrame(placements).T

        # Aanmaken player scores dict
        player_scores = {}

        # Vullen van de player scores
        for _, game_results in data.iterrows():
            for position, player in enumerate(game_results):
                player_scores[player] = player_scores.get(player, 0) + self.score_map[position]

        # Toewijzen van de punten aan een pandas Series
        self.points = pd.Series(
                            {
                                k: v
                                for k, v
                                in player_scores.items()
                                if k is not None
                            }
                        ).dropna().sort_values(ascending=False)

        # Optellen van 1ste, 2de en 3de plekken
        count_placements = {
                    "1st" : data[0].value_counts(),
                    "2nd" : data[1].value_counts(),
                    "3rd" : data[2].value_counts()
                }

        # Telling als dataframe opstellen
        self.medals = pd.DataFrame(count_placements).fillna(0)

        # Tonen totaal aantal punten
        self.performance_data["Aantal Punten"] = [
            self.points[player]
            for player in self.performance_data.index
        ]

        # Aantal keren eerste
        self.performance_data["1st"] = [
            int(self.medals.loc[player, "1st"])
            for player in self.performance_data.index
        ]

        # Aantal keren tweede
        self.performance_data["2nd"] = [
            int(self.medals.loc[player, "2nd"])
            for player in self.performance_data.index
        ]

        # Aantal keren derde
        self.performance_data["3rd"] = [
            int(self.medals.loc[player, "3rd"])
            for player in self.performance_data.index
        ]

        # Aantal keren laatste / niet geëindigd
        self.performance_data["DNF"] = [
            self.performance_data.loc[player, "Aantal Games"] -
            self.performance_data.loc[player, "1st"] -
            self.performance_data.loc[player, "2nd"] -
            self.performance_data.loc[player, "3rd"]
            for player in self.performance_data.index
        ]
        
        # Berekenen de ratio eerste plekken
        self.performance_data["1st Ratio"] = [
            str(
                round(
                    self.performance_data.loc[player, "1st"] /
                    self.performance_data.loc[player, "Aantal Games"] *
                    100,
                    2
                    )
                ) + "%"
            for player in self.performance_data.index
        ]

        # Berekenen de ratio tweede plekken
        self.performance_data["2nd Ratio"] = [
            str(
                round(
                    self.performance_data.loc[player, "2nd"] /
                    self.performance_data.loc[player, "Aantal Games"] *
                    100,
                    2
                    )
                ) + "%"
            for player in self.performance_data.index
        ]

        # Berekenen de ratio derde plekken
        self.performance_data["3rd Ratio"] = [
            str(
                round(
                    self.performance_data.loc[player, "3rd"] /
                    self.performance_data.loc[player, "Aantal Games"] *
                    100,
                    2
                    )
                ) + "%"
            for player in self.performance_data.index
        ]

        # Berekenen DNF ratio
        self.performance_data["DNF Ratio"] = [
            str(
                round(
                    self.performance_data.loc[player, "DNF"] /
                    self.performance_data.loc[player, "Aantal Games"] *
                    100,
                    2
                    )
                ) + "%"
            for player in self.performance_data.index
        ]

        # Gemiddelde eindpositie
        self.performance_data["Gem Eindpositie"] = [
            round(
                (
                    1 * self.performance_data.loc[player, "1st"] +
                    2 * self.performance_data.loc[player, "2nd"] +
                    3 * self.performance_data.loc[player, "3rd"] +
                    4 * self.performance_data.loc[player, "DNF"]
                ) / self.performance_data.loc[player, "Aantal Games"],
                2
            )
            for player in self.performance_data.index
        ]

        # Gemiddelde punten per game
        self.performance_data["Gem punten per game"] = [
            round(
                self.performance_data.loc[player, "Aantal Punten"] /
                self.performance_data.loc[player, "Aantal Games"],
                2
            )
            for player in self.performance_data.index
        ]

        return self.performance_data
    
    def combination_results(self):
        """
        Deze functie berekent en toont de winpercentages en aantal overwinningen
        van spelers per combinatie van spelers.

        Het maakt gebruik van twee heatmaps om de resultaten visueel weer te geven:
        1. Winpercentages per combinatie van spelers.
        2. Overwinningen per combinatie van spelers.
        """
        # Normaliseren van de combinaties van spelers (volgorde maakt niet uit)
        normalized_data = defaultdict(list)
        for comb, winners in self.dominance_data.items():
            sorted_comb = tuple(sorted(comb))
            normalized_data[sorted_comb].extend(winners)

        # Aantal overwinningen per speler per unieke combinatie
        players = set(player for comb in normalized_data.keys() for player in comb)
        win_counts = {comb: {player: 0 for player in players} for comb in normalized_data.keys()}

        for comb, winners in normalized_data.items():
            for winner in winners:
                if winner is not None:
                    win_counts[comb][winner] += 1

        # Winpercentages berekenen
        percentages = {}
        for comb, counts in win_counts.items():
            total_games = sum(counts.values())
            percentages[comb] = {player: (count / total_games) * 100 for player, count in counts.items()}

        # Zet winpercentages om naar DataFrame
        percent_df = pd.DataFrame(percentages).T.fillna(0)

        # Zet overwinningen on naar DataFrame
        win_df = pd.DataFrame(win_counts).T.fillna(0)

        # Versimpelen as-labels combinaties
        comb_labels = {comb: f"C{i+1}" for i, comb in enumerate(percent_df.index)}
        percent_df.index = [comb_labels[comb] for comb in percent_df.index]
        win_df.index = [comb_labels[comb] for comb in win_df.index]

        # Color map voor duidelijkheid
        cmap = mcolors.LinearSegmentedColormap.from_list(
            "black_red_green",
                [
                    (0, 'black'),
                    (0.1 * 10 ** -1000000000000, 'lightblue'),
                    (1, 'orange')
                ]
            )

        # PLotten van de heatmaps op 1 subplot
        fig, axes = plt.subplots(1, 2, figsize=(25, 8))

        # Eerste heatmap: Winpercentages
        sns.heatmap(percent_df, annot=True, cmap=cmap, cbar_kws={'label': 'Win Percentage (%)'}, annot_kws={"color": "black", "size": 12}, fmt='.2f', ax=axes[0])
        axes[0].set_title('Winstpercentage per player per combinatie', fontsize=16)
        axes[0].set_xlabel('Players', fontsize=14)
        axes[0].set_ylabel('Combination', fontsize=14)

        # Tweede heatmap: Overwinningen
        sns.heatmap(win_df, annot=True, cmap=cmap, cbar_kws={'label': 'Win Count'}, annot_kws={"color": "black", "size": 12}, fmt='g', ax=axes[1])
        axes[1].set_title('Overwinningen per player per combinatie', fontsize=16)
        axes[1].set_xlabel('Players', fontsize=14)

        # Aanpassen layout en y-as labels rechter heatmap
        axes[1].set_ylabel('') 
        axes[1].set_yticks([])
        axes[0].set_yticklabels(axes[0].get_yticklabels(), rotation=0, fontsize=12)
        plt.tight_layout()

        # Legenda combinaties (y-as) toevoegen
        fig.text(1, 1, "Combination Key Mapping:", fontsize=14, verticalalignment='top')
        for i, (comb, label) in enumerate(comb_labels.items()):
            fig.text(1, 0.97 - (i + 1) * 0.04, f"{label}: {comb}", fontsize=12)

    def wins_per_start(self):
        """
        Deze functie maakt een staafdiagram dat het aantal overwinningen per speler per startplek toont. 
        De startplek wordt bepaald door de volgorde van de spelers in de key van de 'dominance_data'.
        """
        # Bijhouden winst per startplek
        win_counts_per_start = defaultdict(lambda: defaultdict(int))
        for comb, winners in self.dominance_data.items():
            for i, winner in enumerate(winners):
                if winner is not None:
                    starting_position = comb.index(winner) + 1
                    win_counts_per_start[starting_position][winner] += 1

        # Maak een DataFrame van de win_counts_per_startplek
        win_df = pd.DataFrame(win_counts_per_start).T.fillna(0).astype(int)

        # Sorteren kolommen op overwinningen
        win_df = win_df.apply(lambda row: row.sort_values(ascending=False), axis=1)

        # Color-map aanmaken
        colors = plt.cm.Dark2.colors

        # Plotten van de barplot
        ax = win_df.plot(kind='bar', stacked=False, figsize=(25, 6), color=colors[:len(win_df.columns)])
        ax.set_title('Aantal Overwinningen per Speler per Startplek', fontsize=16)
        ax.set_xlabel('Startplek', fontsize=14)
        ax.set_ylabel('Aantal Overwinningen', fontsize=14)
        ax.set_xticklabels(ax.get_xticklabels(), rotation=0)
        ax.legend(title='Speler', bbox_to_anchor=(1.05, 1), loc='upper left')

        # Toon de plot
        plt.tight_layout()
