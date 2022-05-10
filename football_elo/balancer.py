from typing import List, Tuple


class SearchToken:
    def __init__(self, parent, current_sum, value_index):
        self.parent = parent
        self.current_sum = current_sum
        self.value_index = value_index

    def backtrace(self):
        list_a = []
        list_b = []
        cur = self
        while cur.parent is not None:
            if cur.current_sum == cur.parent.current_sum:
                list_b.append(cur.value_index)
            else:
                list_a.append(cur.value_index)
            cur = cur.parent

        return list_a, list_b


def knapsack_balance(ratings: List[float],
                     num_variants: int = 1,
                     precision: float = 1.0) -> Tuple[List[int], List[int]]:
    """
    Разбивает список чисел примерно на две равные группы с точностью precision.
    Большая точность требует больших вычислений

    Args:
        ratings: список чисел для разбиения
        num_variants: количество вариантов лучших разбиений
        precision: максимальная желаемая разница между идеальной разницей сумм
                   и вычисленной этой процедурой

    Returns:
        Два списка: индексы первой группы и второй группы соответственно
    """

    single_value_precision_reverse = len(ratings) * precision / 2

    values = [round(x * single_value_precision_reverse) for x in ratings]

    tokens = {0: SearchToken(None, 0, -1)}

    for i, value in enumerate(values):
        new_tokens = dict()
        for accumulated_sum, token in tokens.items():
            if accumulated_sum not in new_tokens:
                new_tokens[accumulated_sum] = SearchToken(token, accumulated_sum, i)
            if accumulated_sum + value not in new_tokens:
                new_tokens[accumulated_sum + value] = SearchToken(token, accumulated_sum + value, i)

        tokens = new_tokens

    desired_sum = sum(values) // 2
    # leaving only variants with value more than desired sum to remove permutation duplicates
    tokens = list(sorted(tokens.items(), key=lambda x: x[0] - desired_sum if x[0] >= desired_sum else float('inf')))
    # secondary variants will be suboptimal
    return [token.backtrace() for s, token in tokens[:num_variants]]


class MultipleTeamsSearchToken:
    def __init__(self, parent, accumulated_sums, value_index):
        self.parent = parent
        self.accumulated_sums = accumulated_sums
        self.value_index = value_index

    def backtrace(self):
        piles = [[] for _ in self.accumulated_sums]
        cur = self
        while cur.parent is not None:
            for i, s in enumerate(cur.accumulated_sums):
                if s != cur.parent.accumulated_sums[i]:
                    piles[i].append(cur.value_index)
                    break
            cur = cur.parent

        return piles


def multiple_teams_knapsack_balance(ratings: List[float],
                                    num_teams: int = 3,
                                    num_variants: int = 1,
                                    precision: float = 1.0,
                                    max_entries_per_iteration=100000):
    single_value_precision_reverse = len(ratings) * precision / 2

    values = [round(x * single_value_precision_reverse) for x in ratings]

    # Distance funcitons
    distance = lambda x: max(x) - min(x)

    zeros = [0 for _ in range(num_teams)]
    zeros_tuple = tuple(zeros)
    tokens = [(zeros_tuple, MultipleTeamsSearchToken(None, [0 for _ in range(num_teams)], -1))]

    for value in ratings:
        new_tokens = dict()

        for state, token in tokens:
            for i in range(num_teams):
                next_state = [s for s in token.accumulated_sums]
                next_state[i] += ratings[token.value_index + 1]
                next_state = tuple(next_state)
                next_state_sorted = tuple(sorted(next_state))
                next_dist = distance(next_state)

                if next_state_sorted not in new_tokens:
                    new_tokens[next_state_sorted] = MultipleTeamsSearchToken(token, next_state, token.value_index + 1)

        # removing permutations
        tokens = []
        for state, token in new_tokens.items():
            sorted_state = tuple(sorted(state))
            if sorted_state == state or sorted_state not in new_tokens:
                tokens.append((state, token))

        tokens = list(sorted(tokens, key=lambda x: distance(x[0])))[:max_entries_per_iteration]
        # print(len(tokens), [s for s, t in tokens[:10]])

    # print(tokens[0][0], tokens[0][1].backtrace())
    return [token.backtrace() for s, token in tokens[:num_variants]]
