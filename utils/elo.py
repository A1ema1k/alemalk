from typing import List, Tuple

def knapsack_balance(ratings: List[float],
                     precision: float = 1.0) -> Tuple[List[int], List[int]]:
    """
    Разбивает список чисел примерно на две равные группы с точностью precision.
    Большая точность требует больших вычислений
    
    Args:
        ratings: список чисел для разбиения
        precision: максимальная желаемая разница между идеальной разницей сумм
                   и вычисленной этой процедурой
        
    Returns:
        Два списка: индексы первой группы и второй группы соответственно
    """
    
    single_value_precision_reverse = len(ratings) * precision / 2
    
    values = [round(x * single_value_precision_reverse) for x in ratings]
    
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
    best_token = None
    best_diff = float('inf')
    for accumulated_sum, token in tokens.items():
        if best_diff > abs(accumulated_sum - desired_sum):
            best_token = token
            best_diff = abs(accumulated_sum - desired_sum)
            
    return best_token.backtrace()
    