from football_elo.player import PlayersDatabase
import pytest


@pytest.fixture()
def test_player_database():
    return PlayersDatabase("data/test_players.csv")


def test_player(test_player_database):
    assert len(test_player_database.players) == 2


def test_add_player(test_player_database):
    test_player_database.add_player("Саша")
    print(test_player_database.players)
    assert len(test_player_database.players) == 3


def test_remove_player(test_player_database):
    test_player_database.remove_player('Петя')
    assert len(test_player_database.players) == 1
