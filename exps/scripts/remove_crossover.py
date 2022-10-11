import pandas as pd
from collections import Counter
import pickle

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

def check_freq_fandom(target_fandom_list, fandom_list):
	for item in fandom_list:
		if item not in target_fandom_list:
			return False
	return True



for fandom in fandoms:
	print('working on fandom: ', fandom)
	df = pd.read_csv( fandom + '_preprocessed_filter_en_merged_chs_20211216.tsv', sep = '\t')
	print('before: ', len(df))
	df.Fandoms = df.Fandoms.apply(lambda x: eval(x))
	target_fandom_list = pickle.load(open('../../data/subfandom_info/' + \
								fandom + '_sub_fandoms.p', 'rb'))
	df = df[df['Fandoms'].apply(lambda x: check_freq_fandom(
						target_fandom_list, x))]
	print('after: ', len(df))
	print()
	df.to_csv(fandom + '_preprocessed_filter_en_merged_chs_20211216_no_crossover.tsv', index = False, sep = '\t')
