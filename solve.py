import datetime
import inferencers
import utils
import timeit
import argparse
import json

def parse_args():
    
    parser = argparse.ArgumentParser(description="Run SC and SCoP")

    parser.add_argument("--data_fp", type=str, default=None, help="Which dataset")
   
    parser.add_argument("--model_card",
                        type=str,
                        default='gpt-3.5-turbo',
                        help="Model card using")


    parser.add_argument(
        "--SCN",
        type=int,
        default=4,
        help="Number of sampling path.",
    )

    parser.add_argument(
        "--K",
        type=int,
        default=2,
        help="Number of paraphrases per original problem p.",
    )
    
    parser.add_argument(
        "--outfp",
        type=str,
        default=None,
        help="fp to save the results.",
    )
    
    args = parser.parse_args()

    return args


def solve_dataset(qbank,
                  inferencer = None,
                  ice_exemplars_for_solving = "",
                  ice_exemplars_for_paraphrase = "",
                  SCN=4,
                  K=2,
                  paraphrase_instruct="{in_context_examples}Paraphrase the following math word problem:\n{question}",
                  reasoning_template="{in_context_examples}Question: {question}{options}\nLet's think step by step.",
                  outfn = None,
                 ):
    
    '''
    ice_exemplars: in-context examples
    
    SCN: # of sampling paths
    K: # of paraphrases
    '''
    for pid, problem in enumerate(qbank):

            options = '\nAnswer Choices: ' + ' '.join(problem['options']) if problem['options'] else ''
            
            

            print(f'Solving Original ID = {pid} for {SCN} times:')
            print(problem['question'])
            
            input_prompt = reasoning_template.format(in_context_examples = ice_exemplars_for_solving, 
                                                     question = problem['question'],
                                                     options = options)
            
            
            
            problem['solutions_original'] = [inferencer(input_prompt) for i in range(SCN)]
            
            print()
            
            paraphrase_prompt = paraphrase_instruct.format(in_context_examples = ice_exemplars_for_paraphrase, 
                                                     question = problem['question'])
            
            print(f'Generating {K} paraphrases for Original ID = {pid}:')
            
            problem['paraphrased_questions'] = [inferencer(paraphrase_prompt) for i in range(K)]
            
            print()
            
            # finally solve para....each SCN//K
            
            for ind, candi_q in enumerate(problem['paraphrased_questions']):
                
                input_prompt = reasoning_template.format(in_context_examples = ice_exemplars_for_solving, 
                                                     question = candi_q,
                                                     options = options)
                
                print(f'Solving the {ind}-th paraphrases for Original ID = {pid} for {SCN//K} times')
                solutions_per_para = [inferencer(input_prompt) for i in range(SCN//K)]
                
                problem.setdefault('solutions_paraphrased',[]).append(solutions_per_para)
                
            print('\n\n')
                
    if outfn is not None:
        print(f'Results writing to file...{outfn}')
        with open(outfn, 'w') as f:
            json.dump(qbank, f, indent=4)
            

if __name__ == "__main__":
    
    args = parse_args()

    qb = utils.data_loader(args.data_fp, print_info=False)

        
    start = timeit.default_timer()


    solve_dataset(
        qb,
        inferencer = inferencers.openai_chat_gen,
        SCN=args.SCN,
        K=args.K,
        outfn=args.outfp)


    stop = timeit.default_timer()
    
    print('Done..')
    print(
        f'Done. Total Time: {stop - start: .4f}s, {(stop - start)/3600: .4f} h..'
    )
    hpr, (g_acc, h_acc), (g_acc_tar, h_acc_tar) = utils.evaluate(qb)
    
    print(f'Hard Problem Ratio: {hpr}\nacc (SC): {g_acc}({h_acc})\nacc (SCoP): {g_acc_tar}({h_acc_tar})')
          
    print("Finished at:", datetime.datetime.now())