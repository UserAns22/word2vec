import numpy as np
import gensim
from gensim.models import Word2Vec
import os.path
import sys

vec_source = './vectors/'
extension = '.w2v'
assert len(sys.argv) < 3, "INSUFFICIENT VECTORS"

vec1 = vec_source + 'breitbart' + extension
vec2 = vec_source + 'newyorker' + extension

def load(vec):
    model = Word2Vec.load(vec)
    kv = model.wv
    del model
    return kv
v1 = load(vec1)
v2 = load(vec2)

def create_embedding(syn0, vocab, index2word):
    kv = gensim.models.KeyedVectors()
    kv.syn0 = np.array(syn0)
    kv.vocab = vocab
    kv.index2word = index2word
    kv.init_sims(replace=True)
    return kv

def intersect_vocab(base, other):
    vout = dict()
    for word, v in other.items():
        if word in base:
            vout[word] = v
    return vout

def intersect_align(embed1, embed2):

    s1, s2 = set(embed1.index2word), set(embed2.index2word)
    common = list(s1.intersection(s2))
    newv1 = embed1[common]
    newv2 = embed2[common]
    v1 = intersect_vocab(embed2.vocab, embed1.vocab)
    v2 = intersect_vocab(embed1.vocab, embed2.vocab)
    return create_embedding(newv1, v1, common), create_embedding(newv2, v2, common)

def smart_align(base, other):
    in_base, in_other = intersect_align(base, other)
    base_vecs = in_base.syn0
    other_vecs = in_other.syn0
    matrix = other_vecs.T.dot(base_vecs)
    left_singular, right_singular = np.linalg.svd(matrix)
    ortho = left_singular.dot(right_singular)
    

