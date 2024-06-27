import utils
import argparse
import json

def parse_args():
    
    parser = argparse.ArgumentParser(description="Evaluate Model output and obtain exemplars (from training)")

    parser.add_argument("--data_fp", type=str, default=None, help="Which dataset")
   
    
    parser.add_argument(
        "--outfp",
        type=str,
        default=None,
        help="fp to save the exemplar pairs.",
    )
    

    parser.add_argument(
        "--theta",
        type=float,
        default=0.1,
        help="the margin of the solve rate difference",
    )

    parser.add_argument(
        "--max_N",
        type=int,
        default=1,
        help="number of exemplars for in-context paraphrasing, often 4 or 8",
    )

    args = parser.parse_args()

    return args
            

if __name__ == "__main__":
    
    args = parse_args()

    qb_solved = utils.data_loader(args.data_fp, print_info=False)

    exemplars_lst = utils.get_exemplars(qb_solved, theta = args.theta, N = args.max_N)

    if args.outfn is not None:

        for pair in exemplars_lst:
            print(pair)
    else:
        
        print(f'Exemplars writing to file...{args.outfn}')

        with open(args.outfn, 'w') as f:
            json.dump(exemplars_lst, f, indent=4) 
    