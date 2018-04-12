# /usr/local/bin/python

import argparse
import glob
import datefinder
import re
import nltk
import string
import os
import shutil
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from string import punctuation
import subprocess
from argparse import RawTextHelpFormatter
path = "/Users/gautam/Box Sync/presidency_project/cablenews/data/*/*.txt"

def makedata():
    final_data = {}
    count=0
    stop_words = stopwords.words('english')
    porter = PorterStemmer()
    file = open("example.txt",'w')
    file.write(str(len(glob.glob(path)))+'\n')
    for filename in glob.glob(path):
        files = open(filename)
        text_files = files.read()
        text_files = text_files.lower()
        files.close()
        tokens = word_tokenize(text_files)
        table = str.maketrans('', '', string.punctuation)
        stripped = [w.translate(table) for w in tokens]
        words = [word for word in stripped if word.isalpha()]
        words = [word for word in words if word not in stop_words]
        words = [porter.stem(word) for word in words]
        sentence = ' '.join(word for word in words)
        file.write(sentence+'\n')
    file.close()
def lda():
    for i in range(50,700,10):
        print (subprocess.call(['sudo','java','-mx512M','-cp','bin:lib/args4j-2.0.6.jar','jgibblda.LDA','-est','-alpha', str(50/i),'-beta', str(0.1),'-ntopics', str(i),'-niters', str(1000),'-savestep',str(1000),'-dir','.','-dfile','example.txt']))
        folder_name = 'num_topics_'+str(i)
        os.mkdir(folder_name);
        files = glob.glob('model-*')
        for j in files:
            shutil.move(j, folder_name)
        shutil.move('wordmap.txt',folder_name)
        print("Completed model with topics: "+i)
if __name__== "__main__":
    FUNCTION_MAP = {'makedata' : makedata,
                'LDA' : lda }
    parser = argparse.ArgumentParser(description="This program has multiple functions: \n\nMakedata: Prepares Data for LDA.\nLDA: Does topic modeling and stores the values in folders. \nTopictile: Performs topic tiling on the folder specified.",formatter_class=RawTextHelpFormatter)
    parser.add_argument('command', choices=FUNCTION_MAP.keys())
    args = parser.parse_args()
    func = FUNCTION_MAP[args.command]
    func()
