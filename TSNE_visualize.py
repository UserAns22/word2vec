from gensim.models import Word2Vec
import numpy as np

from sklearn.manifold import TSNE
import matplotlib.pyplot as plt
from sklearn.decomposition import IncrementalPCA
import sys, warnings

vector_dir = './vectors/'
plot_dir = './plots/'
name = sys.argv[1]
in_name = vector_dir +  name  + '.w2v'
extension = '.png'
full_model = Word2Vec.load(in_name)
model = full_model.wv
del full_model

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

warnings.filterwarnings('ignore', '.*Unicode.*')

vectors = []
labels = []
for word in model.vocab:
    vectors.append(model[word])
    labels.append(word)

print('- found ' + str(len(labels)) + ' entities x ' + str(len(vectors[0])) + ' dimensions')
vectors = np.asarray(vectors)
labels =  np.asarray(labels)

# print('reducing dimensions')
# ipca = IncrementalPCA(n_components = dimensions)
# vectors = ipca.fit_transform(vectors)

# vectors = np.asarray(vectors)

tsne = TSNE(verbose = 2, n_components = 2, n_iter=50000)
compute = 5000

print('here we go')
low_dim = tsne.fit_transform(vectors[:compute]) 
print('we did it')
plot = 500
labels = labels[:plot]
#Visualize

filename = plot_dir + '{} TSNE.png'.format(name)
plt.figure(figsize=(24,13.5))
for i, label in enumerate(labels):
    x,y = low_dim[i,:]
    plt.scatter(x,y)
    plt.annotate(label, xy = (x,y), xytext = (5,2), textcoords='offset points', ha='right', va = 'bottom')
    

plt.show()
plt.savefig(filename)
print('whew')
