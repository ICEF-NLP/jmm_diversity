
# Langdive

Langdive is a library for measuring the diversity score between different linguistic datasets. 



**Repository for the article [A Measure for Transparent Comparison of Linguistic Diversity in Multilingual NLP Data Sets](https://arxiv.org/abs/2403.03909) (Findings of NAACL 2024)**


## Installation


```bash
  pip install langdive 
```

Windows: dependency on pyICU, corresponding wheels can be found at https://github.com/cgohlke/pyicu-build . Install the wheel locally and run the pip install afterwards


for install from testPyPI
```bash
   pip install -i https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple langdive-test
```
## Documentation


```
process_corpus(path_to_input_corpus_folder,  start_sample_size = 10000, end_sample_size = 10000, step_size = 1)
```
Creates a results folder with the processed dataset.

The folder titled RESULTS_corpus_folder_name_tokens will be in the working directory with a subfolder titled freqs and a file titled dataset_sample_size.stats.tsv. The file mentioned contains measures for each file in a new line. The folder freqs contains files titled filename.freqs.tsv for each file in the corpus with a pair word frequency in the file in each line.

Input notes:

The dataset name is the name of the final folder in the path to the corpus. 

Variables:

*path_to_input_corpus_folder* - path to the input corpus. Doesn't have to be in the working directory.

*start_sample_size, end_sample_size, step_size* - defines processing in terms of how many words from each language file will be taken.
Example: for values 1, 5, 1, there will be 5 result sets each with 1,2,3,4 and 5 words respectively

```
process_file(file_path, sample_size, output_file)
```
Does the same thing for as process_corpus but for a single file.

Variables:

*file_path* - path to the file to be processed

*sample_size* - number of words to be taken 

*output_file* - name of the output file where the results will be stored, the freq folder will be in the same directory as the output file

```
Langdive
```

The class for working with the processed datasets. 
The constructor, methods and already processed datasets will be documented next.


```
Langdive(min = 1, max = 13, increment = 1, typological_index_binsize = 1)
```


There is several aready processed datasets with a sample_size of 10000. Format (name : number of languages : name in library)
- Universal Dependencies (UD): 106 languages - ud. [project's website](https://universaldependencies.org/)

- Bible 100: 102 languages - bible. [project's website](https://github.com/christos-c/bible-corpus/tree/master)

- mBERT:  97 languages - mbert. [project's website](https://github.com/google-research/bert/blob/master/multilingual.md) 

- XTREME:  40 languages - xtreme. [project's website](https://sites.research.google/xtreme)

- XGLUE:  19 languages - xglue.   [project's website](https://microsoft.github.io/XGLUE/)

- XNLI:  15 languages - xnli. [project's website](https://github.com/facebookresearch/XNLI)

- XCOPA:  11 languages - xcopa. [project's website](https://github.com/cambridgeltl/xcopa)

- TyDiQA: 11 languages - tydiqua. [project website](https://github.com/google-research-datasets/tydiqa)

- XQuAD:   12 languages - xquad. [project's website](https://github.com/deepmind/xquad)

- TeDDi sample: 86  languages - teddi. [project's website]()


```
jaccard_morphology( dataset_path, reference_path, plot = True, scaled = False)
```

*dataset_path, reference_path* - path to the dataset.sample_size.stats.tsv file for analysis. One of the already processed datasets can be used by using its name in the library.

*plot* - boolean that determines whether a plot will be shown

*scaled* - boolean that determines whether or not the datasets will be scaled. Each dataset is normalized indepedently.

Returns the Jaccard score calculated by comparing the distributions of the mean word length

```
jaccard_syntax(dataset_path, reference_path, scaled = False)
```
*dataset_path, reference_path* - path to the dataset file for analysis. One of the already processed datasets can be used by using its name in the library.

*scaled* - boolean that determines whether or not the datasets will be scaled. Each dataset is normalized indepedently.

Returns the Jaccard score calculated by using syntactic features available in lang2vec and the number of times each feature was observed in the dataset.

```
typological_index_syntactic_features(dataset_path)
```
*dataset_path* - expects a csv file with pairs filename(in the dataset), ISO 639-9. One of the already processed datasets can be used 

Returns the typological index using the syntactic features (similarly to jaccard_syntax). The value ranges from 0 to 1 and values closer to 1 indicate higher diversity.

```
typological_index_word_length(dataset_path)
```
*dataset_path* - path to the dataset. One of the already processed datasets can be used 

Returns the typological index adapted to use mean word length for calculations.
```
get_l2v(dataset_codes)
```
*dataset_codes* - expects a csv file with pairs filename(in the dataset), ISO 639-9 

Returns the features extracted 

```
get_dict(sourcedata)
```
*sourcedata* - pandas dataframe of the processed dataset

returns a pair of values dataframe with bins and a dictionary(region:number of languages) based on the sourcedata
## Usage/Examples


```python
from langdive import process_corpus
from langdive import Langdive

process_corpus("C:/Users/Name/corpus_name_folder" )

lang = Langdive()
jacc_mm = lang.jaccard_morphology("path_to_newly_processed_corpus", "teddi", True, True)
```

process_corpus will make folders for processing named after the folder of the corpus in the workspace folder (RESULTS_sample_size_name).

lang = Langdive() creates the library class with the default arguments

lang.jaccard_morphology will calculate the diversity index based on the word length features. The first argument is the stats.tsv file from the newly created RESULTS_sample_size_name, the second argument is the already processed Teddi dataset from the library. Third and fourth argument represent that the values should be scaled and the plot should be shown.
## Acknowledgements

 - [Polyglot ](https://github.com/aboSamoor/polyglot) Part of this project (polyglot_tokenizer file) has been taken from the polyglot project. The reason for this is difficulty with installation on Windows and MacOS



## License

[GNU GPL 3](https://choosealicense.com/licenses/gpl-3.0/)

