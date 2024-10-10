import pandas as pd
from pydantic import conint

from helper import *
from data_loader import *

# sys.path.append('./')
from model.models import *

from utils.data import load_HMCDA_data
from utils.tools import index_generator, parse_minibatch_HMCDA

ent_set, rel_set = OrderedSet(), OrderedSet()
c = 0
df_train = pd.DataFrame(columns=['source', 'rel', 'object'])
for split in ['train', 'test', 'valid']:
    with open('./data/{}/dataset1/{}.txt'.format('KGRACDA', split)) as file:
        for _, line in enumerate( file):
            sub, rel, obj = map(str.lower, line.strip().split('\t'))
            df_train.loc[_] = sub, rel, obj
            c+=1

            # ent_set.add(sub)
            # rel_set.add(rel)
            # ent_set.add(obj)
## train, test, valid

dft = pd.DataFrame(columns=['source', 'rel', 'object'])
train_mirna = pd.DataFrame(columns=['mirna'])
for _, i in enumerate(df_train['rel']):
    a =  df_train['rel'][_].split('-')
    if 'mirna' in a:
       #print(df_train.iloc[_])
       if a[0] == 'mirna':
           train_mirna.loc[_] = df_train['source'][_]
       else:
           train_mirna.loc[_] = df_train['object'][_]

dft = pd.DataFrame(columns=['source', 'rel', 'object'])
train_circ = pd.DataFrame(columns=['circ'])
for _, i in enumerate(df_train['rel']):
    a =  df_train['rel'][_].split('-')
    if 'circ' in a:
       #print(df_train.iloc[_])
       if a[0] == 'circ':
           train_circ.loc[_] = df_train['source'][_]
       else:
           train_circ.loc[_] = df_train['object'][_]


dft = pd.DataFrame(columns=['source', 'rel', 'object'])
train_lncrna= pd.DataFrame(columns=['lncrna'])
for _, i in enumerate(df_train['rel']):
    a =  df_train['rel'][_].split('-')
    if 'lncrna' in a:
       #print(df_train.iloc[_])
       if a[0] == 'lncrna':
           train_lncrna.loc[_] = df_train['source'][_]
       else:
           train_lncrna.loc[_] = df_train['object'][_]

#############################################################################

##  circRNA, miRNA, LncRNA 를 train dataset에서 추출을 하였음

'''

train의 데이터에 무너가 학습에 활용될 데이터를 추가하는것 

기존의 TRAIN의 CIRC, MIRNA, LNC 까지 모두 추출하였으며 

그것에 맞는 seq데이터를 만들어야함 그러면 추출할 데이터의 id-value 형식으로 데이터가 만들어져있어야 매칭해서 추출할수 있음

circ, mirna 의 seq는 찾았지만 lnc 는 아직 못찾음 


'''


## circRNA
from Bio import SeqIO
circ_file = 'human_hg19_circRNAs_putative_spliced_sequence'
with open('./data/{}/{}.fa'.format('circBase', circ_file)) as handle:
    record=  SeqIO.to_dict(SeqIO.parse(handle, 'fasta'))
    # for key, value in record.items():
        #print(key, value)
circ_seq= pd.DataFrame(columns=['circ', 'seq'])
for k in record.keys():
    id = k.split('|')[0]
    circ_seq.loc[i] = [train_circ['circ']]


index = []
for k, v in record.items():
    id = k.split('|')[0]
    if id in train_circ['circ'].values:
        index.append(np.where(train_circ['circ'].values == id)[0])


# mir_file = 'miRNA.dat'
# with open('./data/{}/{}'.format('mirBase', mir_file), 'r', encoding='utf-8') as file:
#     for line in file.readline():
#         #print(line)

## circRNA



## MirRNA

#mir_hair_file = 'hairpin.fa'
mir_mat_file = 'mature.fa'

# import re
# txt = re.compile('hsa-mir*')
#
# ## mature == miRNA
# c= 0
# matched_dic = {}
# with open('./data/{}/{}'.format('mirBase', mir_mat_file)) as handle:
#     record1=  SeqIO.to_dict(SeqIO.parse(handle, 'fasta'))
#     for key, value in record1.items():
#         #print(key, value)
#         if re.search(txt, str(key)):
#             matched_dic[key] = value
#             c+=1
#             print(key)
# print(c)
## mature == miRNA

##matchned mirna id , seq -> matched_dic



## hairpin == pre_mirna
# with open('./data/{}/{}'.format('mirBase', mir_hair_file)) as handle:
#     record2=  SeqIO.to_dict(SeqIO.parse(handle, 'fasta'))
#     for key, value in record2.items():
#         print(key, value)
#
# hair = ''
# for k,v in record2.items():
#     hair+=str(k+',')
#
# for i in hair.split(','):
#     if re.search(txt, i):
#         print(i)
## hairpin == pre_mirna

