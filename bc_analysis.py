import pandas as pd

def get_anexes_prob_bc(bc, LOOKUP):
    try:
        return LOOKUP[bc]
    except KeyError:
        return [0.5]*110
    
def calc_bc_anex_freq():
    dfs = pd.read_excel("./dataset/train.xlsx")

    bcs = []

    training_table = dfs.to_dict('records')

    for row in dfs.to_dict('records'):

        if row['BusinessClassification'] not in bcs:
            #print(row['BusinessClassification'])
            bcs.append(row['BusinessClassification'])

    bc_anex_freq = {}
    for bc in bcs:
        for row in training_table:
            if row['BusinessClassification'] == bc:
                if bc not in bc_anex_freq.keys():
                    bc_anex_freq[bc] = list(row.values())[34:]
                else:
                    for i in range(0,len(bc_anex_freq[bc])):
                        bc_anex_freq[bc][i] += list(row.values())[34:][i]

    for key, values in bc_anex_freq.items():
        kolicina = [x['BusinessClassification'] for x in training_table].count(key)
        bc_anex_freq[key] = [x/kolicina for x in values]

    return bc_anex_freq