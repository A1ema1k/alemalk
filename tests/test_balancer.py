from football_elo.balancer import knapsack_balance, multiple_teams_knapsack_balance
import pytest


def test_knapsack_balance():
    ratings = [10, 10, 5, 5, 2, 2, 3, 3, 4, 4]
    divisions = knapsack_balance(ratings, num_variants=3, precision=1.0)
    max_total = [max([sum([ratings[i] for i in team]) for team in division]) for division in divisions]
    min_total = [min([sum([ratings[i] for i in team]) for team in division]) for division in divisions]
    assert max_total == [24, 25, 26]
    assert min_total == [24, 23, 22]


def test_multiple_teams_knapsack_balance():
    ratings = [10, 10, 5, 5, 2, 2, 3, 3, 4, 4]
    divisions = multiple_teams_knapsack_balance(ratings, num_teams=3, num_variants=3, precision=1.0)
    max_total = [max([sum([ratings[i] for i in team]) for team in division]) for division in divisions]
    min_total = [min([sum([ratings[i] for i in team]) for team in division]) for division in divisions]
    assert min_total == [16, 15, 15]
    assert max_total == [16, 17, 18]
