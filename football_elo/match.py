import pandas as pd
from enum import Enum
from typing import List, Tuple
from .balancer import knapsack_balance
from .player import PlayersDatabase


class MatchResult(Enum):
    WIN = 1  # First team wins
    DRAW = 2  # Match ended in a draw
    LOSE = 3  # Second team wins


class Match:
    def __init__(self):
        self.players = []
        self.teams = None
        self.result = None

    @staticmethod
    def load_from_player_list(players_list: List[str], player_database: PlayersDatabase) -> List[float]:
        """
        Собираем в один датафрейм всех участников матча
        Передаем имя игрока (должно быть уникальным)
        Передаем Дата-Фрейм команды
        Добавляется по одному игроку
        """
        players_set = set(players_list)
        result = Match()
        result.players = []
        for idx, row in player_database.players.iterrows():
            # print(row)
            if row['name'] in players_set:
                result.players.append(row)
        return result

    def balance_teams(self):
        ratings = [player.rating for player in self.players]
        team_a, team_b = knapsack_balance(ratings)[0]
        self.teams = team_a, team_b
        return [self.players[idx] for idx in team_a], [self.players[idx] for idx in team_b]

    def set_result(self, match_result: str):
        if match_result.lower() == "win":
            self.result = MatchResult.WIN
        elif match_result.lower() == "draw":
            self.result = MatchResult.DRAW
        elif match_result.lower() == "lose":
            self.result = MatchResult.LOSE
        else:
            raise ValueError(f"Match result must be in {{win, draw, lose}}")

    def update_database(self, player_database):
        """
        Вычисляется ожидаемое количество очков
        если на вход параметра winner приходит 0 - ничья
        если приходит 1 - Победила команда А
        если приходит 2 - Победила команда B
        """
        if self.teams is None or self.result is None:
            raise ValueError(f"Call balance_teams and set_result before updating the database")

        K = 50
        rating_team_a = sum([self.players[idx].rating for idx in self.teams[0]])
        rating_team_b = sum([self.players[idx].rating for idx in self.teams[1]])
        Ea = 1 / (1 + 10 ** ((rating_team_b - rating_team_a) / 2000))
        #  пул людей 19 человек. 22771.0 к  24721.0.
        #  Шанс на победу команды A = 0.9042201443696141
        #  Шанс на победу команды Б = 0.09577985563038598
        #  Команда А получает = 45 очков
        #  Команда Бё получает = -5 очков

        if self.result == MatchResult.WIN:
            score1 = 1.0
            score2 = 0.0
        elif self.result == MatchResult.LOSE:
            score1 = 0.0
            score2 = 1.0
        elif self.result == MatchResult.DRAW:
            score1 = 1 - Ea
            score2 = Ea

        Ra = rating_team_a + K * (score1 - Ea)
        Rb = rating_team_b + K * (score2 - Ea)

        team_a_mmr = round(Ra - rating_team_a)
        team_b_mmr = round(Rb - rating_team_b)

        player_idx_a = [self.players[idx].name for idx in self.teams[0]]
        player_idx_b = [self.players[idx].name for idx in self.teams[1]]
        players_all = player_idx_a + player_idx_b

        for player_idx in player_idx_a:
            player_database.players.at[player_idx, "rating"] += team_a_mmr
            player_database.players.at[player_idx, "games"] += 1
            if self.result == MatchResult.WIN:
                player_database.players.at[player_idx, "wins"] += 1
            elif self.result == MatchResult.LOSE:
                player_database.players.at[player_idx, "defeats"] += 1
            elif self.result == MatchResult.DRAW:  # Ничья
                player_database.players.at[player_idx, "draws"] += 1

        for player_idx in player_idx_b:
            player_database.players.at[player_idx, "rating"] += team_b_mmr
            player_database.players.at[player_idx, "games"] += 1
            if self.result == MatchResult.LOSE:
                player_database.players.at[player_idx, "wins"] += 1
            elif self.result == MatchResult.WIN:
                player_database.players.at[player_idx, "defeats"] += 1
            elif self.result == MatchResult.DRAW:  # Ничья
                player_database.players.at[player_idx, "draws"] += 1

        for player_idx in players_all:
            player_database.players.at[player_idx, "winrate"] = player_database.players.at[player_idx, "wins"] / \
                                                                max(1.0, player_database.players.at[
                                                                    player_idx, "games"]) * 100

        print('Шанс на победу команды A =', 1 - Ea)
        print('Шанс на победу команды Б =', Ea)
        print('Команда 1 получает =', team_a_mmr, 'очков')
        print('Команда 2 получает =', team_b_mmr, 'очков')
