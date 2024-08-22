###Input: A textfile and size of the sample (if 0 it will take de whole text)
###Output: It prints a line containing the following measures for the input text: mean word length, median word length, char types, word types, word tokens, TTR, H
##To run this over a whole corpus (many files in a folder) use the *.sh scripts
#######################################################################################################################33
from __future__ import division
from collections import defaultdict, Counter

import numpy as np
import os
import random
import statistics

from .polyglot_tokenizer import Text
from segments import Tokenizer


def process_corpus(path_to_input_corpus_folder, is_ISO6393 = False, output_dir = "default", start_sample_size = 10000, end_sample_size = 10000, step_size = 1):

    input_corpus = path_to_input_corpus_folder.split('/')[-1]
    print(f"Processing {input_corpus} corpus") #Information print
    
    output_dir = set_output_dir(output_dir, input_corpus)
    
    headers = ["File", "Avg_length", "Median_length", "Char_types", "Types", "Tokens", "TTR", "H", "ISO_6393"]

    for sample_size in range(start_sample_size, end_sample_size + step_size, step_size):
        output_file = os.path.join(output_dir, f"{input_corpus}.{sample_size}.stats.tsv").replace("\\","/")
        with open(output_file, "w") as f:
            f.write("\t".join(headers) + "\n")

        for filename in os.listdir(path_to_input_corpus_folder):
            filepath = os.path.join(path_to_input_corpus_folder, filename).replace("\\","/")
            print(f"Processing {filename}") #Information print
            process_file(file_path= filepath, is_ISO6393 = is_ISO6393, output_file = output_file, sample_size=sample_size)

    print("DONE. See results in", output_dir)

def set_output_dir(output_dir, input_corpus):
    if output_dir == "default":
        output_dir =f"RESULTS_{input_corpus}"
    else:
        output_dir_str = f"/RESULTS_{input_corpus}"
        output_dir = output_dir.replace("\\","/") + output_dir_str
    os.makedirs(output_dir, exist_ok=True) 
    return output_dir

def process_file(file_path,  is_ISO6393, output_file, sample_size=10000) :
    filename = file_path.split("/")[-1]
    ISO_6393 = ""
    if is_ISO6393:
        ISO_6393 = filename.split(".")[0].lower()

    strings_clean = get_clean_strings(file_path, sample_size)
    words = Counter(strings_clean)
    types = len(set(strings_clean))
    tokens = len(strings_clean)
    ttr = types / tokens

    total = 0
    char_freq = {}
    sizes = []
    tokenizer = Tokenizer()
    for word in strings_clean:
        char_tokenized = tokenizer(word).split()
        size = len(char_tokenized)
        total = total + size
        sizes.append(size)
        for i in char_tokenized:
                if i in char_freq:
                    char_freq[i] += 1
                else:
                    char_freq[i] = 1

    avg = total / tokens
    char_types = len(char_freq)
    median = statistics.median(sizes)

    index = output_file.rfind("/")
    output_dir = output_file[:index] + '/freqs/'
    entropy = get_measures(words, output_dir=output_dir, filename= filename + ".freqs.tsv")
    
    if not os.path.isfile(output_file):
        with open(output_file, 'a') as f:
            headers = ["File", "Avg_length", "Median_length", "Char_types", "Types", "Tokens", "TTR", "H", "ISO_6393"]
            f.write("\t".join(headers) + "\n")

    with open(output_file, 'a') as f:
        f.write(str(filename) + "\t" + str(avg)+"\t"+str(median)+"\t"+str(char_types)+"\t"+str(types)+"\t"+str(tokens)+"\t"+str(ttr)+"\t"+str(entropy)+ "\t" + str(ISO_6393) +"\n")

def get_clean_strings(file_path, sample_size):
    text_file = open(file_path, 'r', encoding="utf-8")
    sample_text = text_file.read()
	
    punctuation=["!",'"',"#","$","%","&","'","(",")","*","+",",","-",".","/",":",";","<","=",">","?","@","[","]","^","_","`","{","}","~","]","¿","»","«","“","”","¡","،"]
    for p in punctuation:
        sample_text = sample_text.replace(p, "")
	
    text = Text(sample_text)
	
    try:
        tokenized_words = text.words
    except:
        tokenized_words = sample_text.split()
	
    strings_clean_aux=[]
    for word in tokenized_words:
        if len(word) == 1 and word.isalnum() == False:
            continue
        strings_clean_aux.append(word.lower())
	
    text_size = len(strings_clean_aux)
    if text_size <= sample_size:
        sample_size = text_size
		
    strings_clean=[]
    max_number = text_size - sample_size
    if sample_size == 0: 
        strings_clean = strings_clean_aux
    else:
        n = random.randint(0, max_number)
        strings_clean = strings_clean_aux[n : (n + sample_size)]

    return strings_clean 

def get_measures(voc, output_dir, filename):
    freq = defaultdict(int)
    os.makedirs(output_dir, exist_ok=True)
    file = open(output_dir + filename, 'w', encoding="utf-8")
    for key, value in sorted(voc.items(), key = lambda item: item[1], reverse=True):
        if key != "":
            freq[key] += value
            freq_pair = str(key) + '\t' + str(value) + '\n'
            file.write(freq_pair)
    freq = np.array(list(freq.values()))
    p = freq / freq.sum()
    H = - (p * np.log2(p)).sum()
    return H