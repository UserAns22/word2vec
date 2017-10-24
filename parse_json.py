import json
import sys
import string
import re

json_dir = './scrapy_spiders/'
name = sys.argv[1]
input_filename = json_dir + name + '.json'

with open(input_filename, 'r') as json_file:
    json_obj = json.load(json_file)

    s = ''
    for j in json_obj:
        s += j['text'].translate(str.maketrans( string.punctuation, " " * len(string.punctuation)))
    
    s = re.sub('  +', ' ', s)
    output_file = name + '.txt'
    with open(output_file, 'w') as output:
        output.write(s)
        output.truncate()



