import numpy as np
import gensim
import os.path
import sys

vec_source = './vectors/'
extension = '.w2v'
assert len(sys.argv) < 3, "INSUFFICIENT VECTORS"i

vec1 = vec_source sys.argv[1] + extension
vec2 = vec_source sys.argv[2] + extension


