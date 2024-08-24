import pandas as pd
import numpy as np
import seaborn as sb
import matplotlib.pyplot as plt
import lang2vec.lang2vec as l2v
import os
import sys
from statistics import mean

plt.rcParams['figure.figsize'] = [9, 6]

class LangDive:
    __min = 1
    __max = 13
    __increment = 1
    __typ_ind_binsize = 1 
    __l2v_syn_features = 103
    __processed_datasets = set(['teddi', 'xcopa', 'xquad', 'tydiqa', 'xnli', 'xtreme', 'xglue', 'mbert', 'bible', 'ud'])
    
    def __init__(self, min = 1, max = 13, increment = 1, typological_index_binsize = 1) -> None:
        self.__min = min
        self.__max = max
        self.__increment = increment
        self.__typ_ind_binsize = typological_index_binsize

        
    def __get_dataset(self, path):
        path = path.replace("\\", "/")
        if path.lower() in self.__processed_datasets: 
            path = f"data/{path.lower()}.10000.stats.tsv"            
            current_dir = os.path.dirname(__file__)
            path = os.path.join(current_dir,path)
            return pd.read_csv(path, sep = '\t')
        else:
            if path[-3] =='c': #checking if tsv or csv
                return pd.read_csv(path)
            else:
                return pd.read_csv(path, sep = '\t')
            

    def jaccard_syntax(self, dataset_path, reference_path, plot = True, scaled = False):    
        dataset_codes = self.__get_dataset(dataset_path)
        dataset_freqs = self.get_l2v(dataset_codes).sum().to_dict()
        
        reference_codes = self.__get_dataset(reference_path)
        reference_freqs = self.get_l2v(reference_codes).sum().to_dict()            

        self.__l2v_syn_features = max(len(dataset_freqs), len(reference_freqs))
        
        if scaled:
            dataset_freqs, reference_freqs = self.__scaler(dataset_freqs, reference_freqs)

        if plot:
            df_data_freq = pd.DataFrame.from_dict(dataset_freqs, orient='index')
            df_ref_freq = pd.DataFrame.from_dict(reference_freqs, orient='index')
            ref_name = self.__get_plot_name(reference_path)
            dataset_name = self.__get_plot_name(dataset_path)
            self.__draw_overlap_plot(df_ref_freq, df_data_freq, ref_name, dataset_name, reference_freqs, dataset_freqs, False)

        index = self.__jaccard_index(dataset_freqs,reference_freqs)[0]
        return index
            
    def jaccard_morphology(self, dataset_path, reference_path, plot = True, scaled = False):
        dataset = self.__get_dataset(dataset_path)
        data_reg, data_freq = self.get_dict(dataset)
        
        reference= self.__get_dataset(reference_path)
        ref_reg, ref_freq = self.get_dict(reference)
        
        if scaled: 
            data_freq, ref_freq=self.__scaler(data_freq, ref_freq)

        if plot:
            df_data_freq = pd.DataFrame.from_dict(data_freq, orient='index')
            df_ref_freq = pd.DataFrame.from_dict(ref_freq, orient='index')
            ref_name = self.__get_plot_name(reference_path)
            dataset_name = self.__get_plot_name(dataset_path)
            self.__draw_overlap_plot(df_ref_freq, df_data_freq, ref_name, dataset_name, ref_freq, data_freq, True)

        index = self.__jaccard_index(data_freq,ref_freq)[0]
        return index 

    def typological_index_syntactic_features(self, dataset_path):
        dataset_codes = self.__get_dataset(dataset_path)
        features_frame = self.get_l2v(dataset_codes)
        entropies = self.__get_entropy(features_frame)
        typ_ind = mean(entropies)
        return float(typ_ind)

    def typological_index_word_length(self, dataset_path):
        dataset = self.__get_dataset(dataset_path)
        word_length_features = self.__get_wordlength_vectors(dataset)
        entropies = self.__get_entropy(word_length_features)
        typ_ind = mean(entropies)
        return float(typ_ind)

    def __get_wordlength_vectors(self, dataset):
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
    
    def get_l2v(self, dataset_df):
        #list of iso codes to query the l2v vectors:
        has_nan = dataset_df['ISO_6393'].isna().any()
        if has_nan:
            raise ValueError("The ISO_6393 column contains NaN values")

        codes = dataset_df["ISO_6393"].str.lower().tolist()  
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
    
    def __draw_overlap_plot(self, df_ref_freq, df_data_freq, reference_name, dataset_name, ref_feq, data_freq, morphology_plot = True):
        if morphology_plot:
            increment = self.__increment
            xlab_name = 'Mean word length'
            topylim = 50
        else:
            increment = 1
            xlab_name = 'l2v features'
            topylim = 100

        df_ref_freq.columns = [reference_name]
        df_data_freq.columns = [dataset_name]
        col1 = df_ref_freq  
        col2 = df_data_freq 
        fig, ax = plt.subplots()
        ax2 = ax.twinx()
        plot1 = col1.plot(kind = 'bar', ax = ax, width = increment, align = "edge", alpha = 0.4, color = 'orange')
        plot2 = col2.plot(kind = 'bar', ax = ax2, width = increment, align = "edge", alpha = 0.5, color = 'palegreen')

        positions, labels = self.__make_positions_and_labels(morphology_plot)

        plt.setp(ax, xticks = positions, xticklabels = labels)
        ax.tick_params(labelrotation = 0, labelsize = 12)
        ax2.tick_params(labelsize = 12)
        ax.legend(fontsize = 14)
        ax2.legend([dataset_name], loc = ('upper left'), fontsize = 14)

        ax2.xaxis.set_visible(False)
        ax.set_ylim(top = topylim)
        ax2.set_ylim(top = topylim)

        ax.set_xlabel(xlab_name, fontsize = 14)

        jacc = self.__jaccard_index(ref_feq, data_freq)[0] 
        textstr= "J=" + str(round(jacc,3))
        plt.gcf().text(0.5, 0.8, textstr, fontsize = 14)
        plt.show()
    
    def __make_positions_and_labels(self, morphology_plot):
        if morphology_plot:
            min = self.__min
            increment = self.__increment
            max = self.__max
        else:
            min = 1
            increment = 1
            max = self.__l2v_syn_features

        positions = [0]
        i = min
        while i < max:
            positions.append(i)
            i = i + increment
        labels = []
        i = min
        while i <= max:
            if morphology_plot:
                labels.append(i)
            else:
                if i == 1 or i % 5 == 0:
                    labels.append(i)
                else:
                    labels.append('')
            i = i + increment            
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

        if len(intersectionvalues) == 0:
            intersec = 0
        else:
            intersec = np.array(intersectionvalues).sum()
        
        if len(unionvalues) == 0:
            unionval = 0
        else:
            unionval = np.array(unionvalues).sum()

        jaccard = float(intersec / unionval)
        
        return (jaccard, union, intersection, unionvalues, intersectionvalues)
            
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
            return (scaled,dataset_freq)
    
    def get_dict(self, dataset_df):
        bins = np.arange(self.__min, self.__max, self.__increment)
        data_regions = pd.DataFrame(columns=['File','Avg_length', 'Median_length', 'Char_types', 'Types','Tokens','TTR','H','ISO_6393','region'])
        data_regions_freq = dict()
        for i in bins:
            aux = pd.DataFrame(dataset_df.loc[(dataset_df['Avg_length']>=i) & (dataset_df['Avg_length']<(i+self.__increment))])
            region = str(i) + "-" + str(i + self.__increment)
            data_regions_freq[region] = len(aux)
            aux['region'] = region   
            if not aux.dropna().empty: 
                if data_regions.dropna().empty:
                    data_regions = aux
                else:
                    data_regions= pd.concat([data_regions, aux], axis=0)
        return (data_regions, data_regions_freq)