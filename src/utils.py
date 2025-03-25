"""
In dit python script staat de code die is gebruikt om
het spel zweeds pesten om te toveren van een tabletop
card game naar een python based simulatie.
"""

# Importeren van gebruikte libraries
import random
import matplotlib.pyplot as plt
import pandas as pd
from main import Player, Tim, Low

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
    def __init__(self, players):
        player_types = {
        #    "busse": Busse,
        "tim": Tim,
        "low": Low
        }

        self.players = [player_types.get(name, Player)(name) for name in players]
        self.stack_of_cards = []
        self.winners = []
        self.placements = {}

        self.score_map = {0: 3, 1: 2, 2: 1}

    def create_deck(self):
        ranks = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
        suits = ["♠", "♥", "♦", "♣"]

        return [f"{suit}{rank}" for rank in ranks for suit in suits]

    def draw_card(self, deck, hand):
        if deck:
            hand.append(deck.pop())

    def starting_hand(self):
        for player in self.players:
            for _ in range(3):
                self.draw_card(self.deck, player.hidden_cards)
            for _ in range(6):
                self.draw_card(self.deck, player.hand_cards)

    def valid_cards(self, hand, top_card):
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
        return all(len(cards) == 0 for cards in [player.hand_cards, player.displayed_cards, player.hidden_cards])
        
    def possible_moves(self, player):
        if len(player.hand_cards) > 0:
            available_cards = player.hand_cards
            origin = "hand"

        elif len(player.displayed_cards) > 0:
            available_cards = player.displayed_cards
            origin = "displayed"

        else:
            #card_to_play = player.hidden_cards[-1]
            #print(player.hidden_cards[-1])
            #print(player.hidden_cards)
            available_cards = [player.hidden_cards[-1]]
            #available_cards.append(player.hidden_cards[-1])
            #print(card_to_play)
            #print(available_cards)
            #player.hand_cards.append(player.hidden_cards[-1])
            #print(player.hidden_cards)
            #player.hidden_cards.remove(player.hidden_cards[-1])
            origin = "hidden"
                       
        if len(self.stack_of_cards) > 0:
            top_card = self.stack_of_cards[-1]
            playable_cards = self.valid_cards(available_cards, top_card)
            playable_cards.append("take")
        else:
            playable_cards = available_cards.copy()

        return playable_cards, origin

    def possible_available_cards(self, player):
        if len(player.hand_cards) > 0:
            available_cards = player.hand_cards
            origin = "hand"

        elif len(player.displayed_cards) > 0:
            available_cards = player.displayed_cards
            origin = "displayed"

        return available_cards, origin
    
    def filter_list(self, lst, x):
        return [item for item in lst if x in item[1:]]
    
    def check_4(self):
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
    
    def game_loop(self, verbose=1):
        """
        Runs a single game of Zweeds Pesten.
        
        verbosity:
            0 - Silent (no prints)
            1 - Winners only
            2 - Full verbose (detailed game state)
        """
        game_phase = "choose_display_cards"
        self.winners = []

        self.deck = self.create_deck()
        random.shuffle(self.deck)
        self.starting_hand()

        for player in self.players:
            playable_cards = player.hand_cards
            player.displayed_cards = player.play_move(game_phase, playable_cards,self.stack_of_cards)
            for card in player.displayed_cards:
                player.hand_cards.remove(card)

        if verbose == 2:
            print("\n------------ Starting Game ------------")
            for player in self.players:
                print(f"{player.name}:")
                print(f"Hand:       {player.hand_cards}")
                print(f"Displayed:  {player.displayed_cards}")
                print(f"Hidden:     {player.hidden_cards}")
                print("-----------------------------------------")

        while len(self.winners) + 1 < len(self.players):
            for player in self.players:
                if self.check_win(player):
                    if player.name not in self.winners:
                        if verbose >= 1:
                            print(f"\n{player.name} has won the game!")
                        self.winners.append(player.name)
                        break
                    continue

                if len(self.winners) + 1 == len(self.players):
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

        if verbose >= 1:
            print("\nGame over! Winners in order:", self.winners)

    
    def simulate_games(self, sims, verbose=0):
        self.placements = {}
        for i in range(sims):
            self.game_loop(verbose=verbose)
            self.placements[f"Game {i + 1}"] = self.winners
            if verbose >= 1:
                print("Game:", i)
        
        self.display_points(self.placements)

    def display_points(self, placements):
        data = pd.DataFrame(placements).T

        player_scores = {}

        for _, game_results in data.iterrows():
            for position, player in enumerate(game_results):
                player_scores[player] = player_scores.get(player, 0) + self.score_map[position]

        self.points = pd.Series(player_scores).sort_values(ascending=False)

        count_placements = {
                    "1st" : data[0].value_counts(),
                    "2nd" : data[1].value_counts(),
                    "3rd" : data[2].value_counts()
                }

        self.medals = pd.DataFrame(count_placements).fillna(0)

        fig, ax1 = plt.subplots(figsize=(10, 6))

        self.points.plot(kind="bar", color="black", alpha=0.6)
        ax1.set_xlabel("Players", rotation=90)
        ax1.set_ylabel("Total Score", color="blue")
        ax1.tick_params(axis="y", labelcolor="blue")

        ax2 = ax1.twinx()

        self.medals.loc[self.points.index].plot(kind="bar", ax=ax2, width=0.3, color=["gold", "silver", "brown"])
        ax2.set_ylabel("Number of Times in Position", color="black")
        ax2.tick_params(axis="y", labelcolor="black")

        plt.title("Total Points & Medals Breakdown")

        ax2.get_legend().remove()

        plt.show()