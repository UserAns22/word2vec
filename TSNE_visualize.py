from gensim.models import Word2Vec
import numpy as np

from sklearn.manifold import TSNE
import matplotlib.pyplot as plt
#from sklearn.decomposition import IncrementalPCA

import string
import sys, warnings

warnings.filterwarnings('ignore', '.*Unicode.*')

plot_dir = './plots/'

def normalize(vals):
    min_val = float(min(vals))
    max_val = float(max(vals))
    output = []
    for val in vals:
        if val < 0:
            val /= (-1 * min_val)
        elif val > 0:
            val /= max_val
        output.append(val)
    return output

def is_valid(word):
    inv = string.punctuation + string.digits 
    if any(c in inv for c in word):
        return False
    return True

def sort_wvc(wvc, max_count = None, max_words = None):
    inv_count = lambda w: -1 * w[2]
    if max_count:
        lst = sorted([w for w in wvc if is_valid(w[0]) and w[2] < max_count], key=inv_count)
    else:
        lst = sorted([w for w in wvc if is_valid(w[0]) and w[2]], key=inv_count)
    if max_words:
        lst = lst[:max_words]
    return lst

def visualize(kv, name, plot_dir=plot_dir, max_count = 250000):
    
    wvc  = []#word vector count
    for word in kv.vocab:
        wvc.append([word, kv[word], kv.vocab[word].count]) 

    dim = len(wvc[0][1])
    sorted_wvc = list(zip(*sort_wvc(wvc, max_count)))

    #debugging purposes
    #return sorted_wvc
#def blah(vectors, labels):
    
    vectors = np.asarray(sorted_wvc[1], dtype=np.float32)
    labels =  np.asarray(sorted_wvc[0]) 


    print('- found ' + str(len(labels)) + ' entities x ' + str(len(vectors[0])) + ' dimensions')
    # print('reducing dimensions')
    # ipca = IncrementalPCA(n_components = dimensions)
    # vectors = ipca.fit_transform(vectors)
    
    # vectors = np.asarray(vectors)
    
    tsne = TSNE(verbose = 2, n_components = 2, n_iter=50000)
    plot = 500
    
    low_dim = tsne.fit_transform(vectors[:plot]) 
    labels = labels[:plot]
    #Visualize
    
    filename = plot_dir + '{} TSNE.png'.format(name)
    plt.figure(figsize=(18,18))
    for i, label in enumerate(labels):
        x,y = low_dim[i,:]
        plt.scatter(x,y)
        plt.annotate(label, xy = (x,y), xytext = (5,2), textcoords='offset points', ha='right', va = 'bottom')
        
    plt.savefig(filename)
    plt.show()

if __name__ == "__main__":
    vector_dir = './vectors/'
    name = sys.argv[1]
    in_name = vector_dir +  name  + '.w2v'
    extension = '.png'
    full_model = Word2Vec.load(in_name)
    kv = full_model.wv
    del full_model
    visualize(kv, name)
