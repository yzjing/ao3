rule :
	input:
		train_data = "data/train_episodes.tsv",
		seen_test_data = "data/seen_program_test_episodes.tsv",
		unseen_test_data = "data/unseen_program_test_episodes.tsv",
		process = "exps/data_processing_scripts/generate_bert_podcast_features.py"
	output:
		train_output = "data/train_feature_df_podcast.p",
		seen_test_output = "data/seen_test_feature_df_podcast.p",
		unseen_test_output = "data/unseen_test_feature_df_podcast.p"
	shell: "python {input.process} {input.train_data} {input.seen_test_data} \
			{input.unseen_test_data} {output.train_output} {output.seen_test_output} {output.unseen_test_output}"

# rule train_test_split:
# 	input:
# 		data = "data/preprocessed_data.tsv",
# 		process = "exps/data_processing_scripts/train_test_split_data.py"
# 	output:
# 		train_output = "data/train_episodes.tsv",
# 		seen_test_output = "data/seen_program_test_episodes.tsv",
# 		unseen_test_output = "data/unseen_program_test_episodes.tsv"
# 	shell: "python {input.process} {input.data} {output.train_output} \
# 			{output.seen_test_output} {output.unseen_test_output}"

# rule preprocess_based_on_agreement:
# 	input:
# 		data = "data/annotated_transcriptions.tsv",
# 		process = "exps/data_processing_scripts/preprocess_based_on_agreement_relaxed.py"
# 	output:
# 		"data/preprocessed_data.tsv"
# 	shell: "python {input.process} {input.data} {output}"

# rule build_transcription_data:
# 	input: 
# 		data = "data/annotations.jsonl",
# 		process = "exps/data_processing_scripts/process_CAT_new.py"
# 	output:
# 		"data/annotated_transcriptions.tsv"
# 	shell: "python {input.process} {input.data} {output}"


