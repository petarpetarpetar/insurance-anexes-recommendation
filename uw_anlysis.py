import pandas as pd

def get_anexes_prob_uw(uw, LOOKUP):
    return LOOKUP[uw]
    
def calc_uw_anex_freq():
    dfs = pd.read_excel("./dataset/train.xlsx")

    uws = []

    training_table = dfs.to_dict('records')

    for row in dfs.to_dict('records'):

        if row['UnderwriterTeam'] not in uws:
            #print(row['UnderwriterTeam'])
            uws.append(row['UnderwriterTeam'])

    uw_anex_freq = {}
    for uw in uws:
        for row in training_table:
            if row['UnderwriterTeam'] == uw:
                if uw not in uw_anex_freq.keys():
                    uw_anex_freq[uw] = list(row.values())[34:]
                else:
                    for i in range(0,len(uw_anex_freq[uw])):
                        uw_anex_freq[uw][i] += list(row.values())[34:][i]

    for key, values in uw_anex_freq.items():
        kolicina = [x['UnderwriterTeam'] for x in training_table].count(key)
        uw_anex_freq[key] = [x/kolicina for x in values]

    return uw_anex_freq