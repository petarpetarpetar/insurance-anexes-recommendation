import pandas as pd
from bc_analysis import calc_bc_anex_freq, get_anexes_prob_bc
from blue_analysis import calculate_blue_data, get_anexes_prob_blue #TODO: RENAME DATA -> FREQ
from uw_anlysis import calc_uw_anex_freq, get_anexes_prob_uw 

def code_difference(code1, code2):
    return int(code1.split(' ')[0])-int(code2.split(' ')[0])
    
def combine(a,b,c):
    return (a*KA+b*KB+c*KC)/(KA+KB+KC)

BC_ANEX_FREQ = calc_bc_anex_freq() # {"BC":[0.0-1.0]*111}
BLUE_ANEX_FREQ = calculate_blue_data()
UW_ANEX_FREQ = calc_uw_anex_freq()
THRESHOLD = 0.4
KA = 5
KB = 5
KC = 7



global_true_positive = 0
global_true_negative = 0
global_false_positive = 0
global_false_negative = 0

test_dfs = pd.read_excel('./dataset/test.xlsx')
test_table = test_dfs.to_dict('records')

cnt = 0

for row in test_table:
    cnt += 1
    anexes_based_on_bc = get_anexes_prob_bc(row['BusinessClassification'], BC_ANEX_FREQ)
    anexes_based_on_uw = get_anexes_prob_uw(row['UnderwriterTeam'], UW_ANEX_FREQ)
    anexes_based_on_blue = get_anexes_prob_blue(list(row.values())[9:34], BLUE_ANEX_FREQ)
    # print(anexes_based_on_bc)
    # print(anexes_based_on_uw)
    
    final_anexes = []

    for i in range(0, 110):
        final_anexes.append(combine(anexes_based_on_bc[i], anexes_based_on_uw[i], anexes_based_on_blue[i])) #TODO: FINETUNE
        #print(f"{anexes_based_on_uw[i]}\n{anexes_based_on_bc[i]}\n{anexes_based_on_blue[i]}\n={final_anexes[i]}\n\n")

    ground_truth = list(row.values())[35:]
    for i in range(0, len(final_anexes)):
        if final_anexes[i] >= THRESHOLD:
            final_anexes[i] = 1
        else:
            final_anexes[i] = 0

    # print(len(ground_truth))
    # print(len(final_anexes))
    true_positive = 0
    true_negative = 0
    false_positive = 0
    false_negative = 0
    for i in range(0, len(final_anexes)):
        if ground_truth[i] == 1 and final_anexes[i] == 0:
            false_negative += 1
        
        elif ground_truth[i] == 1 and final_anexes[i] == 1:
            true_positive += 1

        elif ground_truth[i] == 0 and final_anexes[i] == 0:
            true_negative += 1
        
        else:
            false_positive += 1
    
    print(f"Test case #{cnt}")
    print(f"TP: {true_positive:<10} TN: {true_negative:>10}")
    print(f"FP: {false_positive:<10} FN: {false_negative:>10}")

    global_false_negative += false_negative
    global_false_positive += false_positive
    global_true_negative += true_negative
    global_true_positive += true_positive

print("##########################################")
print("----------------TEST RESULTS--------------")
print(f"$THRESHOLD = {THRESHOLD}")
print(f"$KA = {KA}")
print(f"$KB = {KB}")
print(f"$KC = {KC}")
print(f"total test cases #{cnt}")
print(f"total TP: {global_true_positive:<15}| total TN: {global_true_negative:>15}")
print(f"total FP: {global_false_positive:<15}| total FN: {global_false_negative:>15}")
print(f"RECALL: {global_true_positive / (global_true_positive+global_false_negative)}")
print(f"PRECISION: {true_positive / (true_positive + false_positive)}")
print("##########################################")
