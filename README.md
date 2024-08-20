
# LangDive

LangDive is a library for measuring the diversity score between different linguistic datasets. 



**Repository for the article [A Measure for Transparent Comparison of Linguistic Diversity in Multilingual NLP Data Sets](https://arxiv.org/abs/2403.03909) (Findings of NAACL 2024)**


## Installation


*not on pypi yet so ignore this*
```bash
  pip install langdive 
```

for install from testPyPI
```bash
   pip install -i https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple langdive-test
```

### OS specific instructions

This library has PyICU as one of its dependencies, installation instructions for it and any other necessary libraries during the testing phase will be added here.

#### Windows

You can find wheels for Windows for the pyICU [here](https://github.com/cgohlke/pyicu-build). Download the wheel for your python version and install it within your environment. Run the pip install afterwards.

#### MacOS

The easiest way to set PyICU on a Mac is to first install [Homebrew](https://brew.sh/). Then, run the following commands:

```
# install libicu (keg-only)
brew install pkg-config icu4c

# let setup.py discover keg-only icu4c via pkg-config
export PATH="/usr/local/opt/icu4c/bin:/usr/local/opt/icu4c/sbin:$PATH"
export PKG_CONFIG_PATH="$PKG_CONFIG_PATH:/usr/local/opt/icu4c/lib/pkgconfig"
```

Finally, the PyICU package will be automatically installed by pip during the installation of langdive.

#### Ubuntu

PyICU installation instructions can be found [here](https://pypi.org/project/PyICU/)

During the testing phase, for showing plots make sure to have PyQt6 installed.

## Processed Datasets

There is several aready processed datasets with a sample_size of 10000. 

They are given here in the following format: 
name in the library - name of the dataset : number of languages

- ```ud``` - Universal Dependencies (UD): 106 languages. [project's website](https://universaldependencies.org/)

- ```bible``` - Bible 100: 102 languages. [project's website](https://github.com/christos-c/bible-corpus/tree/master)

- ```mbert``` - mBERT:  97 languages. [project's website](https://github.com/google-research/bert/blob/master/multilingual.md) 

- ```xtreme``` - XTREME:  40 languages. [project's website](https://sites.research.google/xtreme)

- ```xglue``` -  XGLUE:  19 languages.   [project's website](https://microsoft.github.io/XGLUE/)

- ```xnli``` - XNLI:  15 languages. [project's website](https://github.com/facebookresearch/XNLI)

- ```xcopa``` - XCOPA:  11 languages. [project's website](https://github.com/cambridgeltl/xcopa)

- ```tydiqa``` - TyDiQA: 11 languages. [project website](https://github.com/google-research-datasets/tydiqa)

- ```xquad``` -  XQuAD:   12 languages. [project's website](https://github.com/deepmind/xquad)

- ```teddi``` - TeDDi sample: 86  languages. [project's website]()


## Usage/Examples


```python
from langdive import process_corpus
from langdive import LangDive

process_corpus("C:/Users/Name/corpus_name_folder" )

lang = LangDive()
lang.jaccard_morphology("path_to_newly_processed_corpus", "teddi", True, True)
```

process_corpus will make folders for processing named after the folder of the corpus in the workspace folder (RESULTS_sample_size_name).

lang = LangDive() creates the library class with the default arguments

lang.jaccard_morphology will calculate the diversity index based on the word length features. The first argument is the stats.tsv file from the newly created RESULTS_sample_size_name, the second argument is the already processed TeDDi dataset from the library. Third and fourth argument represent that the values should be scaled and the plot should be shown.
## API



#### process_corpus

```
process_corpus(path_to_input_corpus_folder, is_ISO6393 = False, start_sample_size = 10000, end_sample_size = 10000, step_size = 1)
```
Creates a results folder with the processed dataset.

The folder titled RESULTS_corpus_folder_name_tokens will be in the working directory with a subfolder titled freqs and a file titled dataset_sample_size.stats.tsv. The file mentioned contains measures for each file in a new line. The folder freqs contains files titled filename.freqs.tsv for each file in the corpus with a pair word frequency in the file in each line.

Input notes:

The dataset name is the name of the final folder in the path to the corpus. 

Variables:

*```path_to_input_corpus_folder```* - path to the input corpus. Doesn't have to be in the working directory.

*```is_ISO6393```* - whether the names of the files in the dataset correspond to the ISO6393 language standard

*```start_sample_size, end_sample_size, step_size```* - defines processing in terms of how many words from each language file will be taken.
Example: for values 1, 5, 1, there will be 5 result sets each with 1,2,3,4 and 5 words respectively

#### process_file

```
process_file(file_path, sample_size, output_file,is_ISO6393)
```
Does the same thing as process_corpus but for a single file.

Variables:

*```file_path```* - path to the file to be processed

*```sample_size```* - number of words to be taken 

*```output_file```* - name of the output file where the results will be stored, the freq folder will be in the same directory as the output file

*```is_ISO6393```* - whether the name of the file corresponds to the ISO6393 code of the language


### LangDive

The class for working with the processed datasets. 
The constructor, methods and already processed datasets will be documented next.


#### constructor
```
LangDive(min = 1, max = 13, increment = 1, typological_index_binsize = 1)
```
*```min, max, increment```* - controlling bin sizes in word length algorithms (will change the graphs too). Defaults are determined experimentally

*```typological_index_binsize```* - controlling bin size for typological indexes. 



#### jaccard_morphology
```
jaccard_morphology( dataset_path, reference_path, plot = True, scaled = False)
```

*```dataset_path, reference_path```* - path to the dataset.sample_size.stats.tsv file for analysis. One of the already processed datasets can be used by using its name in the library.

*```plot```* - boolean that determines whether a plot will be shown

*```scaled```* - boolean that determines whether or not the datasets will be scaled. Each dataset is normalized indepedently.

Returns the Jaccard score calculated by comparing the distributions of the mean word length

#### jaccard_syntax

```
jaccard_syntax(dataset_path, reference_path, plot = True, scaled = False)
```
*```dataset_path, reference_path```* - path to the dataset file for analysis. One of the already processed datasets can be used by using its name in the library.

*```plot```* - boolean that determines whether a plot will be shown

*```scaled```* - boolean that determines whether or not the datasets will be scaled. Each dataset is normalized indepedently.

Returns the Jaccard score which is calculated by using: the syntactic features available in lang2vec and the number of times each feature was observed in the dataset.
#### typological_index_syntactic_features

```
typological_index_syntactic_features(dataset_path)
```
*```dataset_path```* - expects a csv file with pairs: filename (in the dataset), ISO 639-3. One of the already processed datasets can be used 

Returns the typological index using the syntactic features (similarly to jaccard_syntax). The value ranges from 0 to 1 and values closer to 1 indicate higher diversity.

#### typological_index_word_length

```
typological_index_word_length(dataset_path)
```
*```dataset_path```* - path to the dataset. One of the already processed datasets can be used 

Returns the typological index adapted to use mean word length for calculations.

#### get_l2v
```
get_l2v(dataset_codes)
```
*```dataset_codes```* - expects a csv file with pairs filename(in the dataset), ISO 639-3

Returns the features extracted 

#### get_dict

```
get_dict(sourcedata)
```
*```sourcedata```* - pandas dataframe of the processed dataset

Returns a pair of values dataframe with bins and a dictionary(region:number of languages) based on the sourcedata
## Acknowledgements

 - [Polyglot ](https://github.com/aboSamoor/polyglot) Part of this project (polyglot_tokenizer file) has been taken from the polyglot project. The reason for this is difficulty with installation on Windows and MacOS. If the library gets updated, this file will be removed.



## License

[GNU GPL 3](https://choosealicense.com/licenses/gpl-3.0/)

