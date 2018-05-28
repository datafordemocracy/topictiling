# /usr/local/bin/python
"""
Author : Gautam Somappa
The program processes data/implements LDA/performs topictiling on cable news for the data democracy project.
"""

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
path = "/Users/gautam/Box Sync/presidency_project/cablenews/data/*/*.txt" # Change the path to the folder in your system

def makedata():
    '''
    This function reads files specified in path and formats it so it can be used by LDA.
    '''
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

def lda(min,max):
    '''
    Given the min number of topics and max number of topics, this will perform LDA and store the parameters 
    in folders with the name num_topic_<<topic number>>
    '''
    for i in range(min,max,10):
        print (subprocess.call(['sudo','java','-Xmx2048m','-cp','bin:lib/args4j-2.0.6.jar','jgibblda.LDA','-est','-alpha', str(50/i),'-beta', str(0.1),'-ntopics', str(i),'-niters', str(1000),'-savestep',str(1000),'-dir','.','-dfile','example.txt']))
        folder_name = 'num_topics_'+str(i)
        os.mkdir(folder_name);
        files = glob.glob('model-*')
        for j in files:
            shutil.move(j, folder_name)
        shutil.move('wordmap.txt',folder_name)
        print("Completed model with topics: "+str(i))

def topictile(num_topics,input_file):
    '''
    perform topictiling on just one file and store the output in a folder called 'output'
    '''
    if not os.path.exists('output'):
        os.mkdir('output');
    print(subprocess.call(['sh','topictiling.sh','-ri','5','-tmd',num_topics,'-tmn','model-final','-fp',input_file+'.txt','-fd','files_to_segment','-out','output/'+num_topics+'.txt']))

def topictileBatch(num_topics,pathToStore):
    '''
    perform topictiling on all files in a folder and store the results in a folder called 'output_<<Topic Number>>'
    '''
    output_folder = 'output_'+num_topics
    if not os.path.exists(output_folder):
        os.mkdir(output_folder);
    for example in os.listdir(pathToStore):
        print(example)
        print(subprocess.call(['sh','topictiling.sh','-ri','5','-tmd',num_topics,'-tmn','model-final','-fp',example,'-fd',pathToStore,'-out',output_folder+"/"+example]))

def ldaTrainAgain(topictileModel,niter):
    '''
    Retrain your parameters: This function requires the model to be retrained and the number of interations.
    '''
    print (subprocess.call(['sudo','java','-Xmx2048m','-cp','bin:lib/args4j-2.0.6.jar','jgibblda.LDA','-estc','-dir',topictileModel,'-model','model-final','-niters',niter]))
    print("Training completed")


if __name__== "__main__":
    parser = argparse.ArgumentParser(description="This program has multiple functions: \n\nMakedata: Prepares Data for LDA .\nLDA: Does topic modeling and stores the values in folders. \nTopictile: Performs topic tiling on the folder specified.",formatter_class=RawTextHelpFormatter)
    parser.add_argument("--makedata", help="Prepares Data for LDA",action="store_true")
    parser.add_argument("--LDA",nargs=2, help="Does topic modeling and stores the values in folders",action="store_true")
    parser.add_argument("--topictile",nargs=2, help="Performs topic tiling on the folder specified")
    parser.add_argument("--topictilebatch",nargs=2, help="Performs topic tiling on the folder specified")
    parser.add_argument("--ldaTrainAgain",nargs=2, help="Performs topic modeling on pre-trained model")
    args = parser.parse_args()
    if args.makedata:
        makedata()
    if args.LDA:
        lda(args.LDA[0],args.LDA[1])
    if args.topictile:
        topictile(args.topictile[0],args.topictile[1])
    if args.topictilebatch:
        topictileBatch(args.topictilebatch[0],args.topictilebatch[1])
    if args.ldaTrainAgain:
        ldaTrainAgain(args.ldaTrainAgain[0],args.ldaTrainAgain[1])

