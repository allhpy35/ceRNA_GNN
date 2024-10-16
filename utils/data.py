import networkx as nx
import numpy as np
import scipy
import pickle

# prefix
def load_IMDB_data(prefix='data/preprocessed/IMDB_processed'):
    G00 = nx.read_adjlist(prefix + '/0/0-1-0.adjlist', create_using=nx.MultiDiGraph)
    G01 = nx.read_adjlist(prefix + '/0/0-2-0.adjlist', create_using=nx.MultiDiGraph)
    G10 = nx.read_adjlist(prefix + '/1/1-0-1.adjlist', create_using=nx.MultiDiGraph)
    G11 = nx.read_adjlist(prefix + '/1/1-0-2-0-1.adjlist', create_using=nx.MultiDiGraph)
    G20 = nx.read_adjlist(prefix + '/2/2-0-2.adjlist', create_using=nx.MultiDiGraph)
    G21 = nx.read_adjlist(prefix + '/2/2-0-1-0-2.adjlist', create_using=nx.MultiDiGraph)
    idx00 = np.load(prefix + '/0/0-1-0_idx.npy')
    idx01 = np.load(prefix + '/0/0-2-0_idx.npy')
    idx10 = np.load(prefix + '/1/1-0-1_idx.npy')
    idx11 = np.load(prefix + '/1/1-0-2-0-1_idx.npy')
    idx20 = np.load(prefix + '/2/2-0-2_idx.npy')
    idx21 = np.load(prefix + '/2/2-0-1-0-2_idx.npy')
    features_0 = scipy.sparse.load_npz(prefix + '/features_0.npz')
    features_1 = scipy.sparse.load_npz(prefix + '/features_1.npz')
    features_2 = scipy.sparse.load_npz(prefix + '/features_2.npz')
    adjM = scipy.sparse.load_npz(prefix + '/adjM.npz')
    type_mask = np.load(prefix + '/node_types.npy')
    labels = np.load(prefix + '/labels.npy')
    train_val_test_idx = np.load(prefix + '/train_val_test_idx.npz')
    return [[G00, G01], [G10, G11], [G20, G21]], \
           [[idx00, idx01], [idx10, idx11], [idx20, idx21]], \
           [features_0, features_1, features_2],\
           adjM, \
           type_mask,\
           labels,\
           train_val_test_idx



def load_HMCDA_data(prefix='data/preprocessed/HMCDA_processed'):
    in_file = open(prefix + '/0/0-1-0.adjlist', 'r')
    adjlist00 = [line.strip() for line in in_file]
    adjlist00 = adjlist00
    in_file.close()

    # in_file = open(prefix + '/0/0-2-1-2-0.adjlist', 'r')
    # adjlist01 = [line.strip() for line in in_file]
    # adjlist01 = adjlist01
    # in_file.close()

    in_file = open(prefix + '/0/0-2-0.adjlist', 'r')
    adjlist02 = [line.strip() for line in in_file]
    adjlist02 = adjlist02
    in_file.close()

    in_file = open(prefix + '/1/1-0-1.adjlist', 'r')
    adjlist10 = [line.strip() for line in in_file]
    adjlist10 = adjlist10
    in_file.close()

    in_file = open(prefix + '/1/1-2-1.adjlist', 'r')
    adjlist11 = [line.strip() for line in in_file]
    adjlist11 = adjlist11
    in_file.close()

    in_file = open(prefix + '/1/1-1.adjlist', 'r')
    adjlist12 = [line.strip() for line in in_file]
    adjlist12 = adjlist12
    in_file.close()

    ## READ idx file
    in_file = open(prefix + '/0/0-1-0_idx.pickle', 'rb')
    idx00 = pickle.load(in_file)
    in_file.close()

    # in_file = open(prefix + '/0/0-2-1-2-0_idx.pickle', 'rb')
    # idx01 = pickle.load(in_file)
    # in_file.close()

    in_file = open(prefix + '/0/0-2-0_idx.pickle', 'rb')
    idx02 = pickle.load(in_file)
    in_file.close()

    in_file = open(prefix + '/1/1-0-1_idx.pickle', 'rb')
    idx10 = pickle.load(in_file)
    in_file.close()

    in_file = open(prefix + '/1/1-2-1_idx.pickle', 'rb')
    idx11 = pickle.load(in_file)
    in_file.close()

    in_file = open(prefix + '/1/1-1_idx.pickle', 'rb')
    idx12 = pickle.load(in_file)
    in_file.close()


    ## npz, npy의 차이점은?
    adjM = scipy.sparse.load_npz(prefix + '/adjM.npz')
    type_mask = np.load(prefix + '/node_types.npy')
    train_val_test_pos_circrna_disease = np.load(prefix + '/train_val_test_pos_circrna_disease.npz')
    train_val_test_neg_circrna_disease = np.load(prefix + '/train_val_test_neg_circrna_disease.npz')

    ## 2차원 adjlist, 2차원 idx, adjM, type_mask(c,mi,d total), train_val_test_circrna_disease, train_val_test_neg
    ## 총 6개의 파일이 나오게 됨
    return [[adjlist00,adjlist02],[adjlist10,adjlist11,adjlist12]],\
           [[idx00,idx02], [idx10,idx11,idx12]],\
           adjM, type_mask, train_val_test_pos_circrna_disease, train_val_test_neg_circrna_disease


# load skipgram-format embeddings, treat missing node embeddings as zero vectors
def load_skipgram_embedding(path, num_embeddings):
    count = 0
    with open(path, 'r') as infile:
        ## map(function, iterable) return 되는 데이터의 형식은 정해져있지 않음,
        _, dim = list(map(int, infile.readline().strip().split(' ')))
        embeddings = np.zeros((num_embeddings, dim)) ## np.zeros(shape, dtype) 괄호가 하나더 있음으로, (num_embedding=row, dim=col) 임
        for line in infile.readlines():
            count += 1
            line = line.strip().split(' ')
            embeddings[int(line[0])] = np.array(list(map(float, line[1:]))) # 가로 1행인데 모든 열을 포함하여, 즉 가로줄 하나를 float로 변형
    print('{} out of {} nodes have non-zero embeddings'.format(count, num_embeddings))
    return embeddings


# load metapath2vec embeddings
def load_metapath2vec_embedding(path, type_list, num_embeddings_list, offset_list):
    count = 0
    with open(path, 'r') as infile:
        _, dim = list(map(int, infile.readline().strip().split(' ')))
        embeddings_dict = {type: np.zeros((num_embeddings, dim)) for type, num_embeddings in zip(type_list, num_embeddings_list)}
        offset_dict = {type: offset for type, offset in zip(type_list, offset_list)}
        for line in infile.readlines():
            line = line.strip().split(' ')
            # drop </s> token
            if line[0] == '</s>':
                continue
            count += 1
            embeddings_dict[line[0][0]][int(line[0][1:]) - offset_dict[line[0][0]]] = np.array(list(map(float, line[1:])))
    print('{} node embeddings loaded'.format(count))
    return embeddings_dict


def load_glove_vectors(dim=50):
    print('Loading GloVe pretrained word vectors')
    file_paths = {
        50: 'data/wordvec/GloVe/glove.6B.50d.txt',
        100: 'data/wordvec/GloVe/glove.6B.100d.txt',
        200: 'data/wordvec/GloVe/glove.6B.200d.txt',
        300: 'data/wordvec/GloVe/glove.6B.300d.txt'
    }
    f = open(file_paths[dim], 'r', encoding='utf-8')
    wordvecs = {}
    for line in f.readlines():
        splitLine = line.split()
        word = splitLine[0]
        embedding = np.array([float(val) for val in splitLine[1:]])
        wordvecs[word] = embedding
    print('Done.', len(wordvecs), 'words loaded!')
    return wordvecs
