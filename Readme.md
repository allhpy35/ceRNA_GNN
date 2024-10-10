
### Dataset:

- KGRACDA dataset2 train.txt , test.txt , valid.txt
- 
### Training model:
```shell
python run.py -score_func transe -opn sub -gamma 9 -hid_drop 0.1 -init_dim 200 -epoch 100
2024-10-05 11:15:19,303 - [INFO] - Loading best model, Evaluating on Test data
2024-10-05 11:15:19,407 - [INFO] - [Test, Tail_Batch Step 0]	testrun_05_10_2024_11:14:40
2024-10-05 11:15:19,719 - [INFO] - [Test, Head_Batch Step 0]	testrun_05_10_2024_11:14:40
2024-10-05 11:15:19,909 - [INFO] - [Epoch 34 test]: MRR: Tail : 0.00395, Head : 0.00817, Avg : 0.00606

2024-10-05 11:17:24,977 - [INFO] - Loading best model, Evaluating on Test data
2024-10-05 11:17:25,455 - [INFO] - [Test, Tail_Batch Step 0]	testrun_05_10_2024_11:16:46
2024-10-05 11:17:25,735 - [INFO] - [Test, Head_Batch Step 0]	testrun_05_10_2024_11:16:46
2024-10-05 11:17:25,843 - [INFO] - [Epoch 34 test]: MRR: Tail : 0.00433, Head : 0.00844, Avg : 0.00639


아래의 명령어는 ICLR_compgcn 에 있던 명령어
  ```shell
  ##### with TransE Score Function
  # CompGCN (Composition: Subtraction)
  python run.py -score_func transe -opn sub -gamma 9 -hid_drop 0.1 -init_dim 200
  
  # CompGCN (Composition: Multiplication)
  python run.py -score_func transe -opn mult -gamma 9 -hid_drop 0.2 -init_dim 200
  
  # CompGCN (Composition: Circular Correlation)
  python run.py -score_func transe -opn corr -gamma 40 -hid_drop 0.1 -init_dim 200
  
  ##### with DistMult Score Function
  # CompGCN (Composition: Subtraction)
  python run.py -score_func distmult -opn sub -gcn_dim 150 -gcn_layer 2 
  
  # CompGCN (Composition: Multiplication)
  python run.py -score_func distmult -opn mult -gcn_dim 150 -gcn_layer 2 
  
  # CompGCN (Composition: Circular Correlation)
  python run.py -score_func distmult -opn corr -gcn_dim 150 -gcn_layer 2 
  
  ##### with ConvE Score Function
  # CompGCN (Composition: Subtraction)
  python run.py -score_func conve -opn sub -ker_sz 5
  
  # CompGCN (Composition: Multiplication)
  python run.py -score_func conve -opn mult
  
  # CompGCN (Composition: Circular Correlation)
  python run.py -score_func conve -opn corr
  
  ##### Overall BEST:
  python run.py -name best_model -score_func conve -opn corr 
  ```

  - `-score_func` denotes the link prediction score score function 
  - `-opn` is the composition operation used in **CompGCN**. It can take the following values:
    - `sub` for subtraction operation:  Φ(e_s, e_r) = e_s - e_r
    - `mult` for multiplication operation:  Φ(e_s, e_r) = e_s * e_r
    - `corr` for circular-correlation: Φ(e_s, e_r) = e_s ★ e_r
  - `-name` is some name given for the run (used for storing model parameters)
  - `-model` is name of the model `compgcn'.
  - `-gpu` for specifying the GPU to use
  - Rest of the arguments can be listed using `python run.py -h`
### Citation:
Please cite the following paper if you use this code in your work.
```bibtex
@inproceedings{
    vashishth2020compositionbased,
    title={Composition-based Multi-Relational Graph Convolutional Networks},
    author={Shikhar Vashishth and Soumya Sanyal and Vikram Nitin and Partha Talukdar},
    booktitle={International Conference on Learning Representations},
    year={2020},
    url={https://openreview.net/forum?id=BylA_C4tPr}
}
```
For any clarification, comments, or suggestions please create an issue or contact [Shikhar](http://shikhar-vashishth.github.io).
