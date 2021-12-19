
# coding: utf-8

from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
import pandas as pd
import re
from collections import Counter
from scipy import spatial
from scipy.stats import entropy
import random
import cProfile
import random

data_path = '/home/nx/user/jingy/ao3/data/preprocessed_data/preprocessed_filter_en_merged_chs_20211216_no_crossover/'

def create_timelist(df):
    timelist = df.PublishDate.drop_duplicates().tolist()
    timelist = [str(item)[:7] for item in timelist]
    timelist = [item for item in timelist if int(item[0:4]) >= 2009]
    return sorted(list(set(timelist)))

def create_df_time(df, time_window):
    dfs = []
    for time in time_window:
        dfs.append(df[df.PublishDate.str[:7] == time])
    return pd.concat(dfs)

def get_dist(matrix, idx):
    return matrix[idx,:]

def compute_cosine(row, std):
    return spatial.distance.cosine(row, std)

def sample_text(text, sample_size):
	sample_text = ''
	for i in range(sample_size):
		sample_text += random.choice(text) + ' '
	return sample_text

def main(fandom):
    print('working on fandom: ', fandom)
    df = pd.read_csv( data_path + fandom + '_preprocessed_filter_en_merged_chs_20211216_no_crossover.tsv', sep = '\t')
    df = df[df.Text.str.split().map(len) >= 500]

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
                # df_t_curr['Text'] = df_t_curr.apply(lambda row: sample_text(row['Text'].split(' '), 1000), axis=1)

                df_t_prev = df_t_prev.reset_index()
                # df_t_prev['Text'] = df_t_prev.apply(lambda row: sample_text(row['Text'].split(' '), 1000), axis=1)

                df_two = pd.concat([df_t_curr, df_t_prev])

                tf_l1 = TfidfVectorizer(min_df=2, norm='l1') # used for entropy 
                tf_l2 = TfidfVectorizer(min_df=2, norm='l2') # used for cosine distance
                vectorizer_l1 = tf_l1.fit(df_two.Text.tolist()) 
                vectorizer_l2 = tf_l2.fit(df_two.Text.tolist()) 
                transformed_curr_l1 = vectorizer_l1.transform(df_t_curr.Text.tolist()).toarray()
                transformed_curr_ent = np.apply_along_axis(entropy, 1, transformed_curr_l1)

                transformed_prev_l2 = vectorizer_l2.transform(df_t_prev.Text.tolist())
                transformed_curr_l2 = vectorizer_l2.transform(df_t_curr.Text.tolist()).toarray()
                prev_std = np.mean(transformed_prev_l2, axis=0)
                transformed_curr_dist = np.apply_along_axis(compute_cosine, 1, transformed_curr_l2, std=prev_std)
              
                df_t_curr['Cos'] = df_t_curr.apply(lambda row: transformed_curr_dist[row.name], axis=1)
                # df_t_curr['Entropy'] = df_t_curr.apply(lambda row: transformed_curr_ent[row.name], axis=1)

                del df_t_curr['Text']

                df_all.append(df_t_curr)
    
    try:
        df_all = pd.concat(df_all)
        print(fandom, ' ', len(df_all))
        df_all.to_csv(fandom + '_temporal_tfidf_cos_merged_chapters_20211216_no_crossover.tsv', index = False, sep = '\t')
        # print('Done with: ', fandom)
    except:
        print('not enough sample, results not created')


fandoms = [
'shakespare_william_works',
'bishoujo_senshi_sailor_moon',
'haikyuu',
'hamilton_miranda',
'kuroko_no_basuke',
'les_miserables_all_media_types',
'the_walking_dead_&_related_fandoms',
'hetalia_axis_powers',
'naruto',
'star_wars_all_media_types',
'buffy_the_vampire_slayer',
'arthurian_mythology_&_related_fandoms',
'ms_paint_adventures',
'one_direction',
'attack_on_titan',
'doctor_who_&_related_fandoms',
'tolkien_j_r_r_works_&_related_fandoms',
'dcu',
'dragon_age_all_media_types',
'sherlock_holmes_&_related_fandoms',
'harry_potter',
'supernatural',
'marvel',
]


for fandom in fandoms:
    # try:
    # cProfile.run('main(fandom)')
    main(fandom)
    
    # except:
    #     print('failed with: ',fandom)
    #     continue
        


