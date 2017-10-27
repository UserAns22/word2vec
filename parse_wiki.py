import sys
import string
import re

wiki_file = './Wikipedia/WestburyLab.Wikipedia.Corpus.txt'
name = 'wikipedia'
out_dir = './data/'

with open(input_filename, 'r') as f:

    s = f.read()
    s = re.sub('  +', ' ', s)
    output_file = out_dir + name + '.txt'
    with open(output_file, 'w') as output:
        output.write(s)
        output.truncate()



