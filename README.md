# LangDive

LangDive is a PyPi-hosted library for measuring the level of linguistic diversity in multilingual NLP datasets.

The measures implemented here have been proposed and described in the following NAACL 2024 paper: **[A Measure for Transparent Comparison of Linguistic Diversity in Multilingual NLP Data Sets](https://aclanthology.org/2024.findings-naacl.213.pdf)**

## Installation

The library can be installed directly with ``pip``—there is no need to clone the github repository to use LangDive.

The library requires an environment with Python version 3.10 or higher. 

```bash
  pip install langdive 
```

### OS specific instructions

In order to use the multilingual Polyglot-based tokenization (https://github.com/aboSamoor/polyglot), PyICU is one of LangDive's dependencies. Its installation procedure is OS-specific.

#### Windows

You can find wheels for Windows for the PyICU [here](https://github.com/cgohlke/pyicu-build). Download the wheel for your Python version and install it within your environment. Run the pip install afterwards.

#### MacOS

The easiest way to set PyICU on a Mac is to first install [Homebrew](https://brew.sh/). Then, run the following commands (https://gitlab.pyicu.org/main/pyicu#installing-pyicu):

```
# install libicu (keg-only)
brew install pkg-config icu4c

# let setup.py discover keg-only icu4c via pkg-config
export PATH="$(brew --prefix)/opt/icu4c/bin:$(brew --prefix)/opt/icu4c/sbin:$PATH"
export PKG_CONFIG_PATH="$PKG_CONFIG_PATH:$(brew --prefix)/opt/icu4c/lib/pkgconfig"
```

In case the above does not work, MacOS users can also try the commands below:

```
# install libicu (keg-only)
brew install pkg-config icu4c

# let setup.py discover keg-only icu4c via pkg-config
export PATH="/usr/local/opt/icu4c/bin:/usr/local/opt/icu4c/sbin:$PATH"
export PKG_CONFIG_PATH="$PKG_CONFIG_PATH:/usr/local/opt/icu4c/lib/pkgconfig"
```

Finally, the PyICU package will be automatically installed by pip during the installation of LangDive. 

#### Ubuntu

PyICU installation instructions can be found [here](https://pypi.org/project/PyICU/)

In addition, make sure to have PyQt6 installed to ensure proper functioning of plots.

## Included Datasets

The library includes several datasets that have already been processed with a sample_size of 10000. These datasets can all be used as references in the diversity calculations.

They are listed here in the following format: 
```library_id``` - **name of the dataset** : number of languages

- ```ud``` - **[Universal Dependencies (UD)](https://universaldependencies.org/)**: 106 languages

- ```bible``` - **[Bible 100](https://github.com/christos-c/bible-corpus/tree/master)**: 102 languages

- ```mbert``` - **[mBERT](https://github.com/google-research/bert/blob/master/multilingual.md)**: 97 languages

- ```xtreme``` - **[XTREME](https://sites.research.google/xtreme)**: 40 languages

- ```xglue``` -  **[XGLUE](https://microsoft.github.io/XGLUE/)**: 19 languages

- ```xnli``` - **[XNLI](https://github.com/facebookresearch/XNLI)**: 15 languages

- ```xcopa``` - **[XCOPA](https://github.com/cambridgeltl/xcopa)**: 11 languages

- ```tydiqa``` - **[TyDiQA](https://github.com/google-research-datasets/tydiqa)**: 11 languages

- ```xquad``` -  **[XQuAD](https://github.com/deepmind/xquad)**: 12 languages

- ```teddi``` - **[TeDDi sample](https://github.com/MorphDiv/TeDDi_sample)**: 86  languages

## Using LangDive

LangDive can be used to calculate corpus diversity measures in two different ways. Given a directory of text files (a corpus) following any naming convention, the library can be used to calcute the a Jaccard similarity index by comparing the distributions of the mean word length between a newly processed corpus and the selected built-in reference corpus, as below:

### Usage Example: jaccard_morphology()

```python
from langdive import process_corpus
from langdive import LangDive

#Process corpus
process_corpus("C:/Users/Name/corpus_folder_name" )

# Create a LangDive Object
lang = LangDive()
#Calculate Jaccard index by comparing to the TeDDi corpus
lang.jaccard_morphology("./RESULTS_corpus_folder_name/corpus_folder_name.10000.stats.tsv", "teddi", plot=True, scaled=True)
```

In this example, the provided corpus files are first processed to calculate the measurements and statistics necessary for other library functions.

Afterwards, the library class (``LangDive``) is instantiated with the default arguments and used to calculate the Jaccard similarity index. This calculation is performed using scaled values, and both distributions are also shown side-by-side on a plot.

Alternatively, LangDive can be used to calculate the diversity of a corpus based on 103 syntactic features of the languages in the corpus. For this diversity calculation, all text files in the corpus directory must be named with the following convention: ```iso6393.txt```. For instance, a text file in English should be named ```eng.txt```. The diversity index would then be calculated with a different method :


### Usage Example: jaccard_syntax()

```python
from langdive import process_corpus
from langdive import LangDive

#Process corpus; pass is_ISO6393 to indicate naming convention
process_corpus("C:/Users/Name/corpus_folder_name", isISO6393 = True)

# Create a LangDive Object
lang = LangDive()
#Calculate Jaccard index by comparing to the TeDDi corpus
lang.jaccard_syntax("./RESULTS_corpus_folder_name/corpus_folder_name.10000.stats.tsv", "teddi", plot=True, scaled=True)
```

The output is again a Jaccard similarity index between the input corpus and the reference corpus, this time based on the component languages' syntactic features in each of the corpora. 

### Input Corpora

Regardless of the naming convention used, input corpora should be utf-8 encoded *text files* with no sub-directories and only one file per language. Using other file formats (i.e., XML or tsv) will result in unexpected behavior. 

## Detailed API Documentation

#### process_corpus

```
process_corpus(input_folder_path, is_ISO6393 = False, output_folder_path = "default", sample_size_array = [10000])
```
Creates a results folder containing various measurements and statistics calculated based on the provided input corpus. The input corpus folder should contain textual files encoded in UTF-8. If the user wishes to utilize all functions of this library, it is necessary to ensure all corpus file names (without the file extension) are equal to their respective ISO-6393 language codes, and that the *is_ISO6393* argument is set to True. If these conditions are not met, only the measures based on mean word length can be used, while those relying on syntactic features will report an error.

The created folder "RESULTS_corpus_folder_name" will be placed in the chosen output directory with one or more subfolders "freqs_sample_size" and one or more "corpus_folder_name.sample_size.stats.tsv" files. These files contain various measures for each corpus file, one line per file. Their number depends on the number of different sampling size settings, as defined by the *sample_size_array* function arguments. The "freqs_sample_size" subfolders contain word frequency count files for each file in the corpus folder, calculated for every sampling size setting.

*```input_folder_path```* - Absolute or relative path to the input corpus folder

*```is_ISO6393```* - Boolean indicating whether the names of the input corpus files (without the file extension) correspond to the ISO-6393 language code standard

*```output_folder_path```* - Absolute or relative path to the output folder. The default setting will place the outputs in the current working directory

*```sample_size_array```* - The size of the text sample to be taken from each language file, measured in tokens. Each sample represents a contiguous section of text, with a randomly chosen starting point, containing the selected number of tokens. 
For example, for sample_size_array = [10000, 20000], there will be 2 result sets: one using samples of 10000 tokens per corpus file, and another using samples of 20000 tokens per corpus file.

#### process_file

```
process_file(input_file_path, is_ISO6393, output_file_path, sample_size=10000)
```
Does the same thing as process_corpus but for a single file.

*```input_file_path```* - absolute or relative path to the input corpus file

*```is_ISO6393```* - boolean indicating whether the name of the input corpus file (without the file extension) corresponds to the ISO6393 language code standard

*```output_file_path```* - absolute or relative path to the output file where the results will be stored; the freq folder will be placed in the same directory as the output file

*```sample_size```* - the size of the text sample to be taken, measured in tokens


### LangDive

The class for working with the processed datasets. 

#### constructor
```
LangDive(min = 1, max = 13, increment = 1, typological_index_binsize = 1)
```
*```min, max, increment```* - controls the bin sizes to be used in the Jaccard measure based on mean word length (will also affect the result plots). The stated default values have been determined experimentally.

*```typological_index_binsize```* - controls the bin size for the typological indexes

#### jaccard_morphology
```
jaccard_morphology(dataset_path, reference_path, plot = True, scaled = False)
```

Returns the Jaccard score calculated by comparing the distributions of the mean word length between the given and the reference dataset.

*```dataset_path, reference_path```* - absolute or relative path to the processed corpus TSV file. One of the included datasets that has already been processed can be used by stating its ```library_id```.

*```plot```* - boolean that determines whether a plot will be shown. These plots overlay the distributions of the test and reference corpora in terms of the calculated text statistic.  

*```scaled```* - boolean that determines whether the datasets should be scaled. Each dataset is normalized indepedently.

#### jaccard_syntax

```
jaccard_syntax(dataset_path, reference_path, plot = True, scaled = False)
```

Returns the Jaccard score calculated by comparing the values of 103 syntactic features from lang2vec between the given and the reference dataset. *Requires is_ISO6393=True in process_corpus/process_file*.

*```dataset_path, reference_path```* - absolute or relative path to the processed corpus TSV file. One of the included datasets that has already been processed can be used by stating its ```library_id```.

*```plot```* - boolean that determines whether a plot will be shown

*```scaled```* - boolean that determines whether the datasets should be scaled. Each dataset is normalized indepedently.

#### typological_index_syntactic_features

```
typological_index_syntactic_features(dataset_path)
```

Returns the typological index that uses the 103 syntactic features from lang2vec. The value ranges from 0 to 1 and values closer to 1 indicate higher diversity. *Requires is_ISO6393=True in process_corpus/process_file*.

*```dataset_path```* - absolute or relative path to the processed corpus TSV file. One of the included datasets that has already been processed can be used by stating its `library_id`.

#### typological_index_word_length

```
typological_index_word_length(dataset_path)
```

Returns the typological index adapted to use mean word length for calculations.

*```dataset_path```* - absolute or relative path to the processed corpus TSV file. One of the included datasets that has already been processed can be used by stating its ```library_id```.

#### get_l2v

```
get_l2v(dataset_df)
```

Returns the values of 103 syntactic features from lang2vec for the given set of languages. *Requires is_ISO6393=True in process_corpus/process_file*.

*```dataset_df```* - pandas dataframe of a processed dataset, containing an `ISO_6393` column

#### get_dict

```
get_dict(dataset_df)
```

Returns a dataframe containing pairs of bins and dictionaries (region:number of languages) based on the provided processed dataset (measures)

*```dataset_df```* - pandas dataframe of a processed dataset

## Acknowledgements

 - [Polyglot](https://github.com/aboSamoor/polyglot) - A part of the *langdive* library (the polyglot_tokenizer file) has been taken from the Polyglot project. The reason for this is difficulty with installation on Windows and MacOS. If the library gets updated, this file will be removed.

## Authors and maintainers
This library has been developed and is maintained by the following members of the Natural Language Processing group at the [Innovation Center of the School of Electrical Engineering in Belgrade](https://www.ic.etf.bg.ac.rs/):
- [Aleksandra Todorović](mailto:aleksandra.todorovic@ic.etf.bg.ac.rs)
- [Dr. Vuk Batanović](mailto:vuk.batanovic@ic.etf.bg.ac.rs)

This effort was made possible thanks to collaboration and consultations with [Dr. Tanja Samardžić](mailto:tanja.samardzic@uzh.ch), University of Zurich.

## License

[GNU GPL 3](https://choosealicense.com/licenses/gpl-3.0/)
