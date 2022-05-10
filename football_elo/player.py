import pandas as pd
from typing import List, Tuple

class PlayersDatabase:
    def __init__(self, path):
        self.players = pd.read_csv(path)

    def save(self, path):
        self.players.to_csv(path, index=False, float_format="%.1f")

    def add_player(self,
                   name: str,
                   rating: float = 2500.0,
                   games: int = 0,
                   wins: int = 0,
                   defeats: int = 0,
                   draws: int = 0,
                   winrate: float = 0.0):
        """
        Создание игрока
        Если рейтинг не указан - присваевается стандартный (наверно 2500)
        Если кол-во игр не указано - присваевается 0
        Если винрейт не указан - присваевается стандартный (0)
        """

        newplayer = {'name': name, 'rating': rating, 'games': games, 'wins': wins, 'defeats': defeats, 'draws': draws,
                     'winrate': winrate}
        self.players = self.players.append(newplayer, ignore_index=True)

    def remove_player(self, remove_name):
        '''
        Удаление игрока по имени
        на вход подается имя, которое указано в датафрейме
        '''
        lf = self.players.name.tolist()
        i = lf.index(remove_name)
        self.players = self.players.drop(labels=i, axis=0)

    def show_rating(self):
        rating_list = []
        srt = self.players.loc[self.players['games'] > 0]
        pl = srt.sort_values(['rating'], ascending=[False])
        players_list = pl.name.tolist()
        players_rating = pl.rating.tolist()

        for i in range(len(players_rating)):
            rating_list.append(str([i + 1]) + '.' + str(players_list[i]) + ' = ' + str(players_rating[i]))
        return '\n'.join(rating_list)

    def names_list(self):
        return self.players.name.tolist()
