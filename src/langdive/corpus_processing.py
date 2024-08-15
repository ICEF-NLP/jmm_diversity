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


def process_corpus(path_to_input_corpus_folder,  start_sample_size = 10000, end_sample_size = 10000, step_size = 1):
    mode = "tokens" #TODO aleksandra: does it need to have both modes?
    input_corpus = path_to_input_corpus_folder.split('/')[-1]
    print(input_corpus)
    output_dir = f"RESULTS_{input_corpus}_{mode}"
    os.makedirs(output_dir, exist_ok=True) 

    headers = ["File", "Avg_length", "Median_length", "Char_types", "Types", "Tokens", "TTR", "H"]

    for sample_size in range(start_sample_size, end_sample_size + step_size, step_size):
        output_file = os.path.join(output_dir, f"{input_corpus}.{sample_size}.stats.tsv").replace("\\","/")
        with open(output_file, "w") as f:
            f.write("\t".join(headers) + "\n")

        for filename in os.listdir(path_to_input_corpus_folder):
            filepath = os.path.join(path_to_input_corpus_folder, filename).replace("\\","/")

            print(f"Processing {filename}") #Information print

            with open(output_file, "a") as f:
                f.write(f"{filename}\t")

            if mode == "tokens":
                process_file(file_path= filepath, sample_size=sample_size,output_file = output_file)
            #TODO: check if types is needed
            #elif mode == "types":
                #print("Using measures_originaltext_types.py for types")
                #os.system(f"python3 measures_originaltext_types.py {filepath} {sample_size} >> {output_file}")  # Call script using os.system

    print("DONE. See results in", output_dir)


def process_file(file_path, sample_size, output_file):
    text_file = open(file_path, 'r', encoding="utf-8")
    sample_text = text_file.read()
	
    punctuation=["!",'"',"#","$","%","&","'","(",")","*","+",",","-",".","/",":",";","<","=",">","?","@","[","]","^","_","`","{","}","~","]","¿","»","«","“","”","¡","،"]
    for p in punctuation:
        sample_text = sample_text.replace(p, "")
	
    text = Text(sample_text)
	
    try:
        tokenized_words = text.words
    except:
        tokenized_words=sample_text.split()
	
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

    filename = file_path.split("/")[-1]
    index = output_file.rfind("/")
    print(output_file[:index]) 
    output_dir = output_file[:index] + '/freqs/'
    results = get_measures(words, output_dir=output_dir, filename= filename + ".freqs.tsv")
    with open(output_file, 'a') as f:
        f.write(str(avg)+"\t"+str(median)+"\t"+str(char_types)+"\t"+str(types)+"\t"+str(tokens)+"\t"+str(ttr)+"\t"+str(results)+ "\n")

def get_measures(voc, output_dir, filename):
    freq = defaultdict(int)
    os.makedirs(output_dir, exist_ok=True)
    print(output_dir)
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