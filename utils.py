import json
import math
import re
import numpy as np

def data_loader(rel_fp, print_info=True):

    with open(rel_fp) as file:
        qb = json.load(file)

    print('=' * 40)
    print('Data Stats:')
    print(f'Dataset: {rel_fp}, \n# Datapoints: {len(qb)}, \nKeys: {qb[0].keys()}')
    print('=' * 40)

    if print_info:

        print('Example:')
        for k, v in qb[0].items():
            print(f'{k} -> {v}')
            print('-' * 40)
        print('=' * 40)
    return qb


def compute_entropy(items):
    total_count = len(items)
    item_counts = {}

    # Count the occurrences of each item
    for item in items:
        if item in item_counts:
            item_counts[item] += 1
        else:
            item_counts[item] = 1

    entropy = 0.0

    # Calculate the entropy
    for count in item_counts.values():
        probability = count / total_count
        entropy -= probability * math.log2(probability)

    return round(entropy, 4)


def find_last_capital_letter(text):
    pattern = r'[A-E](?=\))|[A-E](?!.*[A-E])'
    matches = re.findall(pattern, text)
    if matches:
        return matches[-1]
    else:
        return 'Error'

def find_last_integer(text):

    matches = re.findall(r'\d+', text)
    if matches:
        return int(matches[-1])
    else:
        return None

def get_voted(answers):

    return max(set(answers), key=answers.count)


def analyzer(correct, solutions):

    if type(correct) == int:
        ans_extractor = find_last_integer
    else:
        ans_extractor = find_last_capital_letter

    answers = [ans_extractor(sol) for sol in solutions]

    N = len(answers)
    c = 0
    for a in answers:
        if a == correct:
            c += 1
    sr = round(c / N, 4)
    voted = get_voted(answers)

    return answers, sr, voted


def evaluate(qbank):
    
    for q in qbank:
        
        _, sr, voted = analyzer(q['correct'], q['solutions_original'])
            
        q['SC'] = 1 if voted == q['correct'] else 0
        
        q['is_hard'] = 1 if sr <= 0.5 else 0 
        
        para_solution_pool = sum(q['solutions_paraphrased'], []) # flatten nested lists of solutions
        
        _, _, voted_tar = analyzer(q['correct'], para_solution_pool)
        
        q['SCoP'] = 1 if voted_tar == q['correct'] else 0
                 
            
    qb_hard = [q for q in qbank if q['is_hard'] == 1]
    hpr = len(qb_hard)/len(qbank)

    g_acc = np.mean([q['SC'] for q in qbank])
    h_acc = np.mean([q['SC'] for q in qb_hard])
    
    g_acc_tar = np.mean([q['SCoP'] for q in qbank])
    h_acc_tar = np.mean([q['SCoP'] for q in qb_hard])  
    
    return hpr, (g_acc, h_acc), (g_acc_tar, h_acc_tar)


def get_exemplars(qbank, theta = 0.1, N = 1):

    '''theta: the margin of solve rate difference'''

    res = []

    for q in qbank:
        
        _, sr_o, _ = analyzer(q['correct'], q['solutions_original'])

        for para_id, para_kth_solutions in enumerate(q['solutions_paraphrased']):
        
            _, sr_p, _ = analyzer(q['correct'], para_kth_solutions)

            if sr_p >= sr_o + theta:

                res.append((q['question'], q['paraphrased_questions'][para_id]))

                break
        
        if len(res) >= N: break
    
    return res
