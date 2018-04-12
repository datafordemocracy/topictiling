# Topictiling
Repository that does topictiling on cable news for the data democracy project.

```
usage: makeCableNews.py [-h] [--makedata] [--LDA]
                        [--topictile TOPICTILE TOPICTILE]

This program has multiple functions:

Makedata: Prepares Data for LDA .
LDA: Does topic modeling and stores the values in folders.
Topictile: Performs topic tiling on the folder specified.

optional arguments:
  -h, --help            show this help message and exit
  --makedata            Prepares Data for LDA
  --LDA                 Does topic modeling and stores the values in folders
  --topictile TOPICTILE TOPICTILE
                        Performs topic tiling on the folder specified
```
## Content
The code is split into three sections:

 1. Data preparation
 2. Topic Modeling using Latent Dirichlet Allocation (LDA)
 3. Topic Tiling from Topic Models

### Data Preparation

Data fed into LDA should have the format as follows

> [M]  
> [document1]  
> [document2]  
> ...  
> [documentM]

in which the first line is the total number for documents [M]. Each line after that is one document. [documenti] is the ith document of the dataset that consists of a list of Ni words/terms.

> [documenti] = [wordi1] [wordi2] ... [wordiNi]

in which all [wordij] (i=1..M, j=1..Ni) are text strings and they are separated by the blank character.

#### Running the code:
```
python3 makeCableNews.py --makedata
```
This will parse all text files in the path specified in the program and format it accordingly. The file is stored as **example.txt**

### Topic Modeling using Latent Dirichlet Allocation (LDA)
The input file from the previous step is passed to the topic modelling program. Topic modelling is an unsupervised approach. This code runs for topics starting from 50 to 700 and stores them in the format **num_topics_[number]** folders.
#### Running the code:
```
python3 makeCableNews.py --LDA
```
### Topic Tiling from Topic Models
This section performs topictiling on the features obtained from topic models done in the previous step. Fix the number of topics that is deemed appropriate. Topic Tiling reads the input file contained in the folder **files_to_segment**. The code also stores the output file in a folder called **output**. Topic tiling requires two positional arguments

 - num_topics_[number] folder
 - name of input file contained in files_to_segment

#### Running the code
```
python3 makeCableNews.py --topictile num_topics_50 input_text
```
