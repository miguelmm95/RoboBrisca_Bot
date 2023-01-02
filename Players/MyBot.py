import math
import numpy as np

from Game.ForwardModel import ForwardModel
from Players.MyHeuristic import MyHeuristic
from Players.Player import Player
from Game.Common import is_better_card


def get_tier(card):
    if card.card_number == 1 or card.card_number == 3:
        return 2
    if card.card_number == 10 or card.card_number == 11 or card.card_number == 12:
        return 1
    else:
        return 0


class MyBot(Player):
    def __init__(self):
        self.forward_model = ForwardModel()
        self.heuristic = MyHeuristic()

    def think(self, obs, budget):
        list_actions = obs.get_list_actions()
        best_value = -math.inf
        best_action = None

        for action in list_actions:
            new_obs = obs.clone()
            turn = new_obs.playing_cards.len()
            played_cards = obs.playing_cards            ##Las cartas de antes de jugar
            playing_card = action
            value = self.forward_model.play(new_obs, action, self.heuristic)

            if value >= best_value:
                best_action = action
                best_value = value

            if turn == 0:
                print("TURNO 0")
                if get_tier(playing_card.get_card()) == 0 and playing_card.get_card().card_type is not obs.trump_card.card_type:
                    best_action = playing_card
            elif turn == 1:
                print("TURNO 1")
                card_playing_against = played_cards.get_card(0)
                if is_better_card(playing_card.get_card(), played_cards.get_card(0), obs.trump_card, obs.playing_cards.get_card(0)):
                    if best_action is not None:
                        if best_action.get_card().get_value() > playing_card.get_card().get_value():
                            best_action = playing_card
                    else:
                        best_action = playing_card
            elif turn == 2:
                print("TURNO 2")
                print("TEST" + str(played_cards))
                partner_card = played_cards.get_card(0)
                prev_card = played_cards.get_card(1)
                partner_win = is_better_card(partner_card, prev_card, obs.trump_card, obs.playing_cards.get_card(0))
                if partner_win:
                    if get_tier(playing_card.get_card()) == 0 and playing_card.get_card().card_type is not obs.trump_card.card_type:
                        best_action = action
                else:
                    if is_better_card(playing_card.get_card(), prev_card, obs.trump_card, obs.playing_cards.get_card(0)):
                        if best_action is not None:
                            if best_action.get_card().get_value() > playing_card.get_card().get_value():
                                best_action = playing_card
                        else:
                            best_action = playing_card
            elif turn == 3:
                print("TURNO 3")
                rival_card_1 = played_cards.get_card(0)
                rival_card_2 = played_cards.get_card(2)
                partner_card = played_cards.get_card(1)
                rivals_best_card = None
                if is_better_card(partner_card, rival_card_1, obs.trump_card, obs.playing_cards.get_card(0)):
                    if is_better_card(partner_card, rival_card_2, obs.trump_card, obs.playing_cards.get_card(0)):
                        if (get_tier(playing_card.get_card()) == 0 or get_tier(playing_card.get_card()) == 1) and playing_card.get_card().get_type \
                                is not obs.trump_card.card_type:
                            best_action = playing_card
                    else:
                        if is_better_card(playing_card.get_card(), rival_card_2, obs.trump_card, obs.playing_cards.get_card(0)):
                            if best_action is not None:
                                if best_action.get_card().get_value() < playing_card.get_card().get_value():
                                    best_action = playing_card
                            else:
                                best_action = playing_card
                else:
                    if is_better_card(rival_card_1, rival_card_2, obs.trump_card, obs.playing_cards.get_card(0)):
                        rivals_best_card = rival_card_1
                    else:
                        rivals_best_card = rival_card_2

                    if is_better_card(playing_card.get_card(), rivals_best_card, obs.trump_card, obs.playing_cards.get_card(0)):
                        if best_action is not None:
                            if best_action.get_card().get_value() < playing_card.get_card().get_value():
                                best_action = playing_card
                        else:
                            best_action = playing_card

        return best_action

    def __str__(self):
        return "MyBot"
