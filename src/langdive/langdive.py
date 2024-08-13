import pandas as pd
import numpy as np
import seaborn as sb
import matplotlib.pyplot as plt
import lang2vec.lang2vec as l2v
import os
from statistics import mean

plt.rcParams['figure.figsize'] = [9, 6]

class LangDive:
    __min = 1
    __max = 13
    __increment = 1
    __typ_ind_binsize = 1 
    __processed_datasets = set(['teddi', 'xcopa', 'xquad', 'tydiqa', 'xnli', 'xtreme', 'xglue', 'mbert', 'bible', 'ud'])
    
    def __init__(self, min = 1, max = 13, increment = 1, typological_index_binsize = 1) -> None:
        self.__min = min
        self.__max = max
        self.__increment = increment
        self.__typ_ind_binsize = typological_index_binsize
        
    def __get_morphology_processed(self, path):
        if path not in self.__processed_datasets: 
            return pd.read_csv(path, sep = '\t', index_col = 0)
        else:
            path = path.lower()
            if path == 'teddi':
                path = 'data/wordlength_results/sample10000.tsv'
            elif path == 'xcopa':
                path = 'data/wordlength_results/xcopa-processed.10000.stats.tsv'
            elif path == 'xquad':
                path = 'data/wordlength_results/xquad-processed.10000.stats.tsv'
            elif path == 'tydiqa':
                path = 'data/wordlength_results/tydiqa-processed.10000.stats.tsv'
            elif path == 'xnli':
                path = 'data/wordlength_results/xnli-processed.10000.stats.tsv'
            elif path == 'xtreme':
                path = 'data/wordlength_results/xtreme-processed.10000.stats.tsv'
            elif path == 'xglue':
                path = 'data/wordlength_results/xglue-processed.10000.stats.tsv'
            elif path == 'mbert':
                path = 'data/wordlength_results/mbertwiki-processed.10000.stats.tsv'
            elif path == 'bible':
                path = 'data/wordlength_results/biblecorpus100-processed.10000.stats.tsv'
            elif path == 'ud':
                path = 'data/wordlength_results/ud-processed.10000.stats.tsv'
                
            current_dir = os.path.dirname(__file__)
            path = os.path.join(current_dir,path)
            return pd.read_csv(path, sep = '\t', index_col = 0)

    def __get_syntax_processed(self, path):
        if path not in self.__processed_datasets: 
            if path[-3] =='c': #checking if tsv or csv
                return pd.read_csv(path, index_col = 0)
            else:
                return pd.read_csv(path, sep = '\t', index_col = 0)
        else:
            current_dir = os.path.dirname(__file__)
            path = path.lower()
            if path == 'teddi':
                path = 'data/isomappings/teddi500.csv'
                path = os.path.join(current_dir,path)
                codes = pd.read_csv(path, index_col = 0)
                return codes
            elif path == 'xcopa':
                path = 'data/isomappings/xcopa-processed.10000.csv'
                path = os.path.join(current_dir,path)
                codes = pd.read_csv(path, index_col = 0)
                return codes
            elif path == 'xquad':
                path = 'data/isomappings/xquad-processed.10000.csv'
                path = os.path.join(current_dir,path)
                codes = pd.read_csv(path, index_col = 0)
                return codes
            elif path == 'tydiqa':
                path = 'data/isomappings/tydiqa-processed.10000.csv'
                path = os.path.join(current_dir,path)
                codes = pd.read_csv(path, index_col = 0)
                return codes
            elif path == 'xnli':
                path = 'data/isomappings/xnli-processed.10000.csv'
                path = os.path.join(current_dir,path)
                codes = pd.read_csv(path, index_col = 0)
                return codes
            elif path == 'xtreme':
                path = 'data/isomappings/xtreme-processed.10000.csv'
                path = os.path.join(current_dir,path)
                codes = pd.read_csv(path, index_col = 0)
                return codes
            elif path == 'xglue':
                path = 'data/isomappings/xglue-processed.10000.csv'
                path = os.path.join(current_dir,path)
                codes = pd.read_csv(path, index_col = 0)
                return codes
            elif path == 'mbert':
                path = 'data/isomappings/mbertwiki-processed.10000.csv'
                path = os.path.join(current_dir,path)
                codes = pd.read_csv(path, index_col = 0)
                codes.loc["armenian"].at["ISO_6393"] = "hy"
                codes.loc["vowiki-latest-pages-articles"].at["ISO_6393"] = "vol"
                return codes
            elif path == 'bible':
                path = 'data/isomappings/biblecorpus100-processed.10000.csv'
                path = os.path.join(current_dir,path)
                codes = pd.read_csv(path, index_col = 0)
                codes = codes.drop(["crp.txt"])
                codes.loc["jap.txt"].at["ISO_6393"] = "jpn"
                return codes
            elif path == 'ud':
                path = 'data/isomappings/ud-processed.tsv'
                path = os.path.join(current_dir,path)
                codes = pd.read_csv(path, sep='\t', index_col=0)
                codes.loc["UD_Western_Armenian-ArmTDP.txt"].at["ISO_6393"] = "hy"
                return codes
        
    def jaccard_syntax(self, dataset_path, reference_path, scaled = False):
        dataset_codes = self.__get_syntax_processed(dataset_path)
        reference_codes = self.__get_syntax_processed(reference_path)
        
        dataset_freqs = self.get_l2v(dataset_codes).sum().to_dict()
        reference_freqs= self.get_l2v(reference_codes).sum().to_dict()
        
        if scaled:
            dataset_freqs, reference_freqs= self.__scaler(dataset_freqs, reference_freqs)

        index = self.__jaccard_index(dataset_freqs,reference_freqs)[0].item()
        return index
            
    def jaccard_morphology(self, dataset_path, reference_path, plot = True, scaled = False):
        dataset = self.__get_morphology_processed(dataset_path)
        data_reg, data_freq = self.get_dict(dataset)
        
        reference= self.__get_morphology_processed(reference_path)
        ref_reg, ref_freq = self.get_dict(reference)
        
        if scaled: 
            data_freq, ref_freq=self.__scaler(data_freq, ref_freq)
            
        if plot:
            df_data_freq=pd.DataFrame.from_dict(data_freq, orient='index')
            df_ref_freq=pd.DataFrame.from_dict(ref_freq, orient='index')
            ref_name = self.__get_plot_name(reference_path)
            dataset_name = self.__get_plot_name(dataset_path)
            self.__draw_overlap_plot(df_ref_freq, df_data_freq, ref_name, dataset_name, ref_freq, data_freq)

        index = self.__jaccard_index(data_freq,ref_freq)[0].item()
        return index 

    def typological_index_syntactic_features(self, dataset_path):
        dataset = self.__get_syntax_processed(dataset_path)
        features = self.get_l2v(dataset)
        entropies = self.__get_entropy(features)
        typ_ind = mean(entropies)
        return typ_ind

    def typological_index_word_length(self, dataset_path):
        dataset = self.__get_morphology_processed(dataset_path)
        word_length_features = self.__get_wordlength_vectors(dataset)
        entropies = self.__get_entropy(word_length_features)
        typ_ind = mean(entropies)
        return typ_ind

    def __get_wordlength_vectors(self, dataset):
        #TODO aleksandra: why 11.2?? shoudl there be a min max incr?
        bins = np.arange(1, 11.2, self.__typ_ind_binsize) #[ 1. ,  1.1,  1.2,  1.3... ]
        langs = dataset.index.tolist()
        vectors_hash = {}
    
        for l in langs:    
            binary_vector= np.zeros(len(bins))
            wordlength=dataset.loc[l]['Avg_length']
            index=len(np.arange(1, wordlength, self.__typ_ind_binsize))
            binary_vector[index-1]=1  
            vectors_hash[l]= binary_vector
        
        return(pd.DataFrame.from_dict(vectors_hash).transpose())

    
    def get_l2v(self, dataset_codes):
        #list of iso codes to query the l2v vectors:
        codes = dataset_codes["ISO_6393"].str.lower().tolist()    
        features = l2v.get_features(codes, "syntax_knn")
        features_frame = pd.DataFrame.from_dict(features).transpose()
        return (features_frame)
    
    def __get_entropy(self, df): 
        entropies = []
        for index in range(len(df.columns)): 
            p = np.ones(2)
            freqs = df[index].to_numpy() 
            ones = len(freqs[freqs == 1])
            zeros = len(freqs[freqs == 0])
            p_ones = ones / len(freqs)
            p_zeros = zeros / len(freqs) 
            p[0] = p_ones
            p[1] = p_zeros
            p = p[p != 0] 
            H = -(p * np.log2(p)).sum()
            entropies.append(H)
        return(entropies) 
    
    def __get_plot_name(self, path):
        path = path.strip()
        if ".tsv" not in path:
            return path
        else:
            name = path.split('/')[-1]
            return name[:-4]
    
    def __draw_overlap_plot(self, df_ref_freq, df_data_freq, reference_name, dataset_name, ref_feq, data_freq):
        df_ref_freq.columns = [reference_name]
        df_data_freq.columns = [dataset_name]
        col1 = df_ref_freq  
        col2 = df_data_freq 
        fig, ax = plt.subplots()
        ax2 = ax.twinx()
        plot1 = col1.plot(kind = 'bar', ax = ax, width = self.__increment, align = "edge", alpha = 0.4, color = 'orange')
        plot2 = col2.plot(kind = 'bar', ax = ax2, width = self.__increment, align = "edge", alpha = 0.5, color = 'palegreen')
        positions, labels = self.__make_positions_and_labels()

        plt.setp(ax, xticks = positions, xticklabels = labels)
        ax.tick_params(labelrotation = 0, labelsize = 12)
        ax2.tick_params(labelsize = 12)
        ax.legend(fontsize = 14)
        ax2.legend([dataset_name], loc = ('upper left'), fontsize = 14)

        ax2.xaxis.set_visible(False)
        ax.set_ylim(top = 50)
        ax2.set_ylim(top = 50)
        ax.set_xlabel('Mean word length', fontsize = 14)

        jacc = self.__jaccard_index(ref_feq, data_freq)[0] 
        textstr= "J=" + str(round(jacc,3))
        plt.gcf().text(0.5, 0.8, textstr, fontsize = 14)
        plt.show() #TODO: aleksandra added for console testing
    
    def __make_positions_and_labels(self):
        positions = [0]
        i = self.__min
        while i < self.__max:
            positions.append(i)
            i = i + self.__increment
        labels = []
        i = self.__min
        while i <= self.__max:
            labels.append(i)
            i = i + self.__increment            
        return tuple(positions), tuple(labels)

    def __jaccard_index(self, data1, data2):
        union = dict()
        intersection = dict()
        intersectionvalues = []
        unionvalues = []
        for key in data1: 
            if data1[key] > data2[key]:
                union[key] = data1[key]
                unionvalues.append(union[key])
            else:
                union[key] = data2[key]
                unionvalues.append(union[key])
            if data1[key] != 0 and data2[key] != 0:
                if (data1[key] < data2[key]):
                    intersection[key] = data1[key]
                    intersectionvalues.append(intersection[key])
                else:
                    intersection[key] = data2[key]
                    intersectionvalues.append(intersection[key])
        jaccard = np.array(intersectionvalues).sum() / np.array(unionvalues).sum()     
        
        return(jaccard, union, intersection, unionvalues, intersectionvalues)
            
    def __scaler(self, dataset_freq, reference_freq):
        dataset_freq_num = np.array(list(dataset_freq.values())).sum() 
        reference_freq_num = np.array(list(reference_freq.values())).sum() 
        scaled=dict()
        
        if (dataset_freq_num > reference_freq_num):
            max = dataset_freq_num
            min = reference_freq_num
            c = max / min  
            for key in reference_freq:
                scaled[key] = reference_freq[key] * c 
            return(dataset_freq,scaled)
        else:
            max = reference_freq_num
            min = dataset_freq_num
            c = max / min
            for key in dataset_freq:
                scaled[key] = dataset_freq[key] * c 
            return(scaled,dataset_freq)
    
    def get_dict(self, sourcedata):
        bins = np.arange(self.__min, self.__max, self.__increment)
        data_regions = pd.DataFrame(columns=['Avg_length', 'Median_length', 'Char_types', 'Types','Tokens','TTR','H','region'])
        data_regions_freq = dict()
        for i in bins:
            aux = pd.DataFrame(sourcedata.loc[(sourcedata['Avg_length']>i) & (sourcedata['Avg_length']<(i+self.__increment))])
            region = str(i) + "-" + str(i + self.__increment)
            data_regions_freq[region] = len(aux)
            aux['region'] = region
            #added for future warning: The behavior of DataFrame concatenation with empty or all-NA entries is deprecated. 
            #In a future version, this will no longer exclude empty or all-NA columns when determining the result dtypes. 
            #To retain the old behavior, exclude the relevant entries before the concat operation.  
            #Aleksandra: it executes longer but makes sure the behaviour is kept for future pandas versions.
            if not aux.dropna().empty: 
                if data_regions.dropna().empty:
                    data_regions = aux
                else:
                    data_regions= pd.concat([data_regions, aux], axis=0)
        return (data_regions, data_regions_freq)
    

