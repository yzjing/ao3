1. start with the data files with the suffix "\_preprocessed.tsv"

2. use the script "lang_detect.py" to remove non-English entries.

3. I manually recovered some false negatives from the step above. They are stored in the data files with the suffix "\__preprocessed_filter_en_20210915.tsv".

4. merge chapters with the script "merge_chapters.py".

5. I compiled the major subfandoms for each fandom. The data is stored in the directory "subfandom_info".

6. (optional) use the script "remove_crossover.py" to remove crossovers.

7. use script "temporal_tfidf_toprev_conlen_opt.py" to compute term novelty.