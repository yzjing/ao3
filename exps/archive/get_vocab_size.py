
# coding: utf-8

# In[1]:
from sklearn.feature_extraction.text import CountVectorizer
import numpy as np
import pandas as pd
import re
import sgt_opt as sgt
from collections import Counter

# In[3]:

# create a corpus to give to sklearn
def create_corpus_for_voc(df):
    doc = []
    for i in df.Text.tolist():
        #Remove some non-ascii characters and 'aa's
        i = re.sub(r'aA|aa', 'a', i)
        i = re.sub(r'\\xe2........|\\xc|\\xa|\\n|[0123456789*_]', '', i)
        i = i.lower()
        doc.append(i)  
    return doc


# In[4]:

# Get a vocabulary using sklearn's filtering
def get_voc(corpus, ngram, mindf):
    vectorizer = CountVectorizer(stop_words='english', ngram_range=(ngram,ngram),min_df=mindf)
    f = vectorizer.fit_transform(corpus)
    return set(sorted(vectorizer.get_feature_names()))


# In[5]:

# compute unigram-frequency dict using the same preprocessing, using only words from the vocabulary
def create_unigram_freq_dict(df, voc):
    text = {}
    df_text = df.Text.tolist()
    for line in df_text:
        line_f = re.sub(r'aA|aa', 'a', line)
        line_f = re.sub(r'\\xe2........|\\xc|\\xa|\\n|[0123456789*_]', '', line_f).lower()
        line_f = re.findall(u'(?u)\\b\\w\\w+\\b', line_f)
        line_f = [word for word in line_f if word in voc]
        text[line] = dict(Counter(line_f))
    return text


# In[6]:
def create_timelist(df):
    timelist = df.PublishDate.drop_duplicates().tolist()
    timelist = [str(i)[:7] for i in timelist]
    return sorted(list(set(timelist)))


# In[7]:
def create_df_time(df, time):
    return df[df.PublishDate.str[:7] == time]


# In[8]:

# calculate unigram probabilities by simple Good Turing smoothing.
# imput: unigram-freq dict
# output: unigram-prob dict, mimic of a document-term matrix
# if unigram is in this doc, prob = the unigram prob calculated by sgt
# otherwise, prob = the probability given to "all unknown unigrams" by sgt
# def calc_sgt(line_dict, voc):
#     prob_line = []
#     sgt_line = sgt.simpleGoodTuringProbs(line_dict)
#     num_abs_words = len(voc - set(line_dict.keys()))
#     for word in voc:
#         if word in line_dict.keys():
#             prob_line.append(sgt_line[0][word])
#         else:
#             prob_line.append(sgt_line[1]/float(num_abs_words))
#     gc.collect()
#     return prob_line


# # In[13]:
# def get_dist(text, di, vocab):
#     return calc_sgt(di[text], vocab)

def get_dist(text, di, vocab):
    prob_line = []
    try:
        sgt_line = sgt.simpleGoodTuringProbs(di[text])
        num_abs_words = len(vocab - set(di[text].keys()))
        for word in vocab:
            if word in di[text].keys():
                prob_line.append(sgt_line[0][word])
            else:
                prob_line.append(sgt_line[1]/float(num_abs_words))
        return prob_line
    except:
        return [0]


def main(fandom):
    print('working on fandom: ', fandom)
    df = pd.read_csv(fandom + '_preprocessed.tsv', sep = '\t')
    df = df.fillna(0)
    
    min_df = 4
    
    # filter to exclude the months with less than 10 authors or 10000 words
    tl = create_timelist(df)
    timelist = []
    for t in tl:
        df_t = create_df_time(df, t)
        try:
            df_t = df_t.drop(['ChapterIndex', 'URL', 'CompleteDate','UpdateDate','Comments','PublishDate','Notes','Bookmarks'], axis=1)
            df_t = df_t.drop_duplicates()
        except:
            df_t = df_t.drop(['ChapterIndex', 'CompleteDate','UpdateDate','Comments','PublishDate','Notes','Bookmarks'], axis=1)
            df_t = df_t.drop_duplicates()

        words = df_t.Words.sum()
        authors = len(set(df_t.Author.tolist()))
        if words >= 10000 and authors >= 10:
            timelist.append(t)

    df = df[df.PublishDate.str[:7].isin(timelist)]
    df = df[df.Words.astype(int) > 500]
    
    df = df.sample(5000,replace=True)

    # Add a column of smoothed unigram probablities to df
    corp = create_corpus_for_voc(df)
    vocab = get_voc(corp,1,min_df)
    with open('vocab_size.txt', 'a') as g:
        g.write(str(len(vocab)) + "\n")
    # unigram_dict = create_unigram_freq_dict(df, vocab)
    # df['Dist'] = df['Text'].map(lambda x: get_dist(x, unigram_dict, vocab))
    # del df['Text']

    # df.to_csv(fandom + '_unigram_dist.tsv', index = False, sep = '\t')
    print('Done with: ', fandom)

fandoms = [
'bishoujo_senshi_sailor_moon',
'haikyuu',
'hamilton_miranda',
'kuroko_no_basuke',
'les_miserables_all_media_types',
'shakespare_william_works',
'the_walking_dead_&_related_fandoms',
'hetalia_axis_powers',
'naruto',
'star_wars_all_media_types',
'buffy_the_vampire_slayer',
'arthurian_mythology_&_related_fandoms',
'ms_paint_adventures',
'homestuck',
'one_direction',
'attack_on_titan',
'doctor_who_&_related_fandoms',
'tolkien_j_r_r_works_&_related_fandoms',
'dcu',
'dragon_age_all_media_types',
'sherlock_holmes_&_related_fandoms',
'the_avengers_all_media_types',
'harry_potter',
'supernatural',
'marvel',
]


# jobs = []
# for fandom in fandoms:
#     p = multiprocessing.Process(target=main, args=(fandom,))
#     jobs.append(p)
#     p.start()

for fandom in fandoms:
    main(fandom)

# profile.run('main("shakespare_william_works")')

# main("shakespare_william_works")

'''
done:

''' 

