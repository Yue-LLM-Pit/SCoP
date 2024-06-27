# Paraphrase and Solve: Exploring and Exploiting the Impact of Surface Form on Mathematical Reasoning in Large Language Models

![Task](images/motivation.jpg)

The repository contains the code of the paper:
> **Paraphrase and Solve: Exploring and Exploiting the Impact of Surface Form on Mathematical Reasoning in Large Language Models (NAACL'2024)** 
> [[Paper]](https://aclanthology.org/2024.naacl-long.153/) [[OpenReview]](https://openreview.net/forum?id=lnPP2TO3jW7) <br>
> Yue Zhou, Yada Zhu, Diego Antognini, Yoon Kim, and Yang Zhang <br>

> [!NOTE]
> The repository is currently being edited.

## Requirement
## Run
Example of solving a dataset
```shell
python3 explore.py --data_fp data/sample.txt --SCN 4 --K 2 --outfp 'res.txt'
```
Example of obtaining exemplars for in-context paraphrasing
```shell
python3 get_exemplars.py --data_fp res.txt --theta 0.1 --max_N 1 --outfp 'exemplars.txt'
```

## Cite
