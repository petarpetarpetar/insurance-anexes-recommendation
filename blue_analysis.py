import pandas as pd
#import pprint

BLUE_THREASHHOLD = 0.9
num_blue = 25
num_grey = 111
        
def get_anexes_prob_blue(curr_blue: list[int], all_blue: list[list[int]]):
    result = [0 for _ in range(num_grey)]
    for i, greys in enumerate(all_blue):
        for j, val in enumerate(greys):
            if curr_blue[i] == 1:
                result[j] += val
            else:
                result[j] += 1-val
    result = [r/num_blue for r in result]

    scalar = 1 / max(result)
    result = [r * scalar for r in result]

    return result


# obradjuje podatke za testiranje, rezultat ove funkcije treba funkciji calculateBlueForTest
def calculate_blue_data() -> list[list[int]]:
    dfs = pd.read_excel("./dataset/train.xlsx")

    matrix = [[0 for _ in range(num_grey)] for _ in range(num_blue)]
    count_blues = [0 for _ in range(num_blue)]

    for row in dfs.to_dict('records'):
        for i, blue in enumerate(list(row.values())[9:34]):
            if blue == 1:
                count_blues[i] += 1
                for j, grey in enumerate(list(row.values())[34:]):
                    matrix[i][j] += grey
            
    result = [[0 for _ in range(num_grey)] for _ in range(num_blue)]
    for i, row in enumerate(matrix):
        for j, val in enumerate(row):
            if count_blues[i] == 0:
                matrix[i][j] = 0
                continue
            result[i][j] = val / count_blues[i]
    return result
