
# coding: utf-8

# In[1]:
import numpy as np
import pandas as pd
import re
from gensim import corpora, models, similarities
from scipy import special, spatial
import pickle
# from nltk.corpus import wordnet as wn
# from nltk.stem.wordnet import WordNetLemmatizer
from gensim.models import Phrases
from gensim.corpora import Dictionary

data_path = '/home/nx/user/jingy/ao3/data/preprocessed_data/preprocessed_filter_en_merged_chs_20211216_no_crossover/'


# create a corpus to give to sklearn
def preprocess(df):
    docs = []
     # Lemmatize all words in documents.
    # lemmatizer = WordNetLemmatizer()  
    for line in df.Text.tolist():
        #Remove some non-ascii characters and 'aa's
        line = re.sub(r'aA|aa', 'a', line)
        line = re.sub(r'\\xe2........|\\xc|\\xa|\\n|[0123456789*_]', '', line)
        line = re.findall(u'(?u)\\b\\w\\w+\\b', line)
        line = [word.lower() for word in line] 
        # line = [lemmatizer.lemmatize(word) for word in line]
        docs.append(line)  
    return docs

def add_ngrams(docs, bigram, trigram):
    for idx in range(len(docs)):
        for token in bigram[docs[idx]]:
            if '_' in token:
                # Token is a bigram, add to document.
                docs[idx].append(token)
        for token in trigram[docs[idx]]:
            if '_' in token:
                # Token is a bigram, add to document.
                docs[idx].append(token)
    return docs

def create_corpus(sentences):
    id2word = corpora.dictionary.Dictionary(sentences)
    corpus = [id2word.doc2bow(sentence) for sentence in sentences]
    return id2word, corpus

def create_timelist(df):
    timelist = df.PublishDate.drop_duplicates().tolist()
    timelist = [str(i)[:7] for i in timelist]
    timelist = [item for item in timelist if int(item[0:4]) >= 2009]
    return sorted(list(set(timelist)))

def create_timewindow(timelist, window_len):
    idx = 0
    window_all = []
    while idx <= len(timelist) - window_len:
        window_all.append(timelist[idx:idx+window_len])
        idx += window_len
    window_all.append(timelist[idx:])
    window_all = [w for w in window_all if len(w) > 0]
    return window_all

def create_df_time(df, time_window):
    dfs = []
    for time in time_window:
        dfs.append(df[df.PublishDate.str[:7] == time])
    return pd.concat(dfs)

def get_dist(line, model, id2word):
    dist = model.get_document_topics(id2word.doc2bow(line), minimum_probability = 0)
    return [i[1] for i in dist]

def calc_kl(p, q):
    return sum([p[i]*(np.log2(p[i]/q[i])) for i in range(len(p))])

def JSD(P, Q):
    M = 0.5 * (P + Q)
    return 0.5 * (sum(special.rel_entr(P, M)) + sum(special.rel_entr(Q, M)))

def main(fandom):
    print('working on fandom: ', fandom)
    df = pd.read_csv(data_path + fandom + '_preprocessed_filter_en_merged_chs_20211216_no_crossover.tsv', sep = '\t')
    # filter very short documents
    df = df[df.Text.str.split().map(len) >= 500]

    # if len(df) > 10000:
    #     df = df.sample(10000, replace=False, random_state=42)

    timelist = create_timelist(df)
    df_all = []
    for time in timelist:
        prev_window = timelist[timelist.index(time)-6:timelist.index(time)]
        if len(prev_window) > 0:
            # use the current month and the past 6 months
            df_t_curr = create_df_time(df, [time])
            df_t_prev = create_df_time(df, prev_window)
            if len(df_t_curr) > 20 and len(df_t_prev) > 50:
                # if len(df_t_curr) > 100:
                #     df_t_curr = df_t_curr.sample(100, replace=False, random_state=42)
                # if len(df_t_prev) > 500:
                #     df_t_prev = df_t_prev.sample(500, replace=False, random_state=42)
                df_t_curr = df_t_curr.reset_index()
                df_t_prev = df_t_prev.reset_index()
                df_two = pd.concat([df_t_curr, df_t_prev])
                sentences = preprocess(df_two)
                # bigram = Phrases(sentences, min_count=10)
                # trigram = Phrases(bigram[sentences])
                # sentences = add_ngrams(sentences, bigram, trigram)
                del df_two['Text']
                df_two['Processed_text'] = sentences
                id2word = Dictionary(sentences)
                # print('Number of unique words in initital documents:', len(id2word))
                # Filter out words that occur less than x documents, or more than x% of the documents.
                id2word.filter_extremes(no_below=5, no_above=0.9)
                # print('Number of unique words after removing rare and common words:', len(id2word))
                corpus = [id2word.doc2bow(doc) for doc in sentences]
                model = models.LdaMulticore(corpus=corpus,id2word=id2word,num_topics=100,workers=30)               

                df_t_curr['Dist'] = df_two['Processed_text'].map(lambda x: get_dist(x, model, id2word))[0:len(df_t_curr)]
                df_t_prev['Dist'] = df_two['Processed_text'].map(lambda x: get_dist(x, model, id2word))[len(df_t_curr):]

                prev = df_t_prev.Dist.tolist()
                std_prev = np.mean(np.asarray(prev), axis=0)

                df_t_curr['JSD'] = df_t_curr.apply(lambda row: JSD(row['Dist'], std_prev), axis=1)
                df_all.append(df_t_curr)

    try:
        df_all = pd.concat(df_all)
        del df_all['Text']
        print(fandom, ' ', len(df_all))
        df_all.to_csv(fandom + '_lda_with_dist_merged_chs_no_crossover_20211216.tsv', index = False, sep = '\t')
        print('Done with: ', fandom)
    except:
        print('not enough sample, results not created')



fandoms = [
'shakespare_william_works',
'sherlock_holmes_&_related_fandoms',
'star_wars_all_media_types',
'les_miserables_all_media_types',
'bishoujo_senshi_sailor_moon',
'haikyuu',
'hamilton_miranda',
'kuroko_no_basuke',
'the_walking_dead_&_related_fandoms',
'hetalia_axis_powers',
'naruto',
'buffy_the_vampire_slayer',
'arthurian_mythology_&_related_fandoms',
'ms_paint_adventures',
'one_direction',
'attack_on_titan',
'doctor_who_&_related_fandoms',
'tolkien_j_r_r_works_&_related_fandoms',
'dcu',
'dragon_age_all_media_types',
'harry_potter',
'marvel',
'supernatural'

]


for fandom in fandoms:
    # try:
    main(fandom)
    # except:
    #     print('failed with: ',fandom)
    #     continue
        
# profile.run('main("shakespare_william_works")')

'''
done:

''' 

'''
'''

