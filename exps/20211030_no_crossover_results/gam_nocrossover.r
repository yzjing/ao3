library(mgcv)
df <- read.csv(file='/Users/blackbird/Desktop/professional/PhD_program/ao3/data/fanfic_regression_data_20210915_no_crossover.tsv', header=TRUE, sep='\t')


df_kudos <- df[df$Kudos != 0, ]
 res_kudos <- mgcv::bam(Kudos ~ s(Term_novelty, bs='cr', sp=0.1,k=5) + s(Topic_novelty, bs='cr', sp=0.1,k=5)
 	+ s(Chapters, sp=0.1, bs='cr') + s(author_fic_cnt, sp=0.1, bs='cr') 
+  Freq_relationship + Category_F_F + Category_F_M + Category_Gen + Category_M_M
+  Category_Multi + Category_Other + ArchiveWarnings_underage + ArchiveWarnings_death + 
+ ArchiveWarnings_choose_no + ArchiveWarnings_no_apply + ArchiveWarnings_violence + Rating_E                  
+ Rating_G + Rating_M + Rating_N + Fandom_harry_potter + Fandom_dcu + Fandom_doctor_who + Fandom_star_wars          
+ Fandom_arthurian + Fandom_supernatural + Fandom_haikyuu  + Fandom_kuroko_no_basuke + Fandom_hamilton_miranda 
+ Fandom_dragon_age + Fandom_the_walking_dead + Fandom_buffy  + Fandom_les_miserables + Fandom_naruto + Fandom_tolkien 
+ Fandom_shakespare + Fandom_hetalia + Fandom_attack_on_titan + Fandom_ms_paint_adventures + Fandom_marvel             
+ Fandom_sailor_moon+ Fandom_one_direction, data=df_kudos, method='REML', family='gaussian')

df_hits <- df[df$Hits != 0, ]
 res_hits <- mgcv::bam(Hits ~ s(Term_novelty, bs='cr', sp=0.1,k=5) + s(Topic_novelty, bs='cr', sp=0.1,k=5)
 	+ s(Chapters, sp=0.1, bs='cr') + s(author_fic_cnt, sp=0.1, bs='cr') 
+  Freq_relationship + Category_F_F + Category_F_M + Category_Gen + Category_M_M
+  Category_Multi + Category_Other + ArchiveWarnings_underage + ArchiveWarnings_death + 
+ ArchiveWarnings_choose_no + ArchiveWarnings_no_apply + ArchiveWarnings_violence + Rating_E                  
+ Rating_G + Rating_M + Rating_N + Fandom_harry_potter + Fandom_dcu + Fandom_doctor_who + Fandom_star_wars          
+ Fandom_arthurian + Fandom_supernatural + Fandom_haikyuu  + Fandom_kuroko_no_basuke + Fandom_hamilton_miranda 
+ Fandom_dragon_age + Fandom_the_walking_dead + Fandom_buffy  + Fandom_les_miserables + Fandom_naruto + Fandom_tolkien 
+ Fandom_shakespare + Fandom_hetalia + Fandom_attack_on_titan + Fandom_ms_paint_adventures + Fandom_marvel             
+ Fandom_sailor_moon+ Fandom_one_direction, data=df_kudos, method='REML', family='gaussian')

df_comments <- df[df$Comments != 0, ]
res_comments <- mgcv::bam(Comments ~ s(Term_novelty, bs='cr', sp=0.1,k=5) + s(Topic_novelty, bs='cr', sp=0.1,k=5)
 	+ s(Chapters, sp=0.1, bs='cr') + s(author_fic_cnt, sp=0.1, bs='cr') 
+  Freq_relationship + Category_F_F + Category_F_M + Category_Gen + Category_M_M
+  Category_Multi + Category_Other + ArchiveWarnings_underage + ArchiveWarnings_death + 
+ ArchiveWarnings_choose_no + ArchiveWarnings_no_apply + ArchiveWarnings_violence + Rating_E                  
+ Rating_G + Rating_M + Rating_N + Fandom_harry_potter + Fandom_dcu + Fandom_doctor_who + Fandom_star_wars          
+ Fandom_arthurian + Fandom_supernatural + Fandom_haikyuu  + Fandom_kuroko_no_basuke + Fandom_hamilton_miranda 
+ Fandom_dragon_age + Fandom_the_walking_dead + Fandom_buffy  + Fandom_les_miserables + Fandom_naruto + Fandom_tolkien 
+ Fandom_shakespare + Fandom_hetalia + Fandom_attack_on_titan + Fandom_ms_paint_adventures + Fandom_marvel             
+ Fandom_sailor_moon+ Fandom_one_direction, data=df_kudos, method='REML', family='gaussian')

df_bookmarks <- df[df$Bookmarks != 0, ]
 res_bookmarks <- mgcv::bam(Hits ~ s(Term_novelty, bs='cr', sp=0.1,k=5) + s(Topic_novelty, bs='cr', sp=0.1,k=5)
 	+ s(Chapters, sp=0.1, bs='cr') + s(author_fic_cnt, sp=0.1, bs='cr') 
+  Freq_relationship + Category_F_F + Category_F_M + Category_Gen + Category_M_M
+  Category_Multi + Category_Other + ArchiveWarnings_underage + ArchiveWarnings_death + 
+ ArchiveWarnings_choose_no + ArchiveWarnings_no_apply + ArchiveWarnings_violence + Rating_E                  
+ Rating_G + Rating_M + Rating_N + Fandom_harry_potter + Fandom_dcu + Fandom_doctor_who + Fandom_star_wars          
+ Fandom_arthurian + Fandom_supernatural + Fandom_haikyuu  + Fandom_kuroko_no_basuke + Fandom_hamilton_miranda 
+ Fandom_dragon_age + Fandom_the_walking_dead + Fandom_buffy  + Fandom_les_miserables + Fandom_naruto + Fandom_tolkien 
+ Fandom_shakespare + Fandom_hetalia + Fandom_attack_on_titan + Fandom_ms_paint_adventures + Fandom_marvel             
+ Fandom_sailor_moon+ Fandom_one_direction, data=df_kudos, method='REML', family='gaussian')


pdf('/Users/blackbird/Desktop/gam_res_merged_20210915_no_crossover.pdf', width=17, height=8)
par(mfrow=c(2,4))
plot(res_kudos, scale=0, shade=TRUE, select=1, xlab='Term novelty', ylab='Kudos', cex.lab=1.6, cex.axis=2)
plot(res_hits, scale=0, shade=TRUE, select=1, xlab='Term novelty', ylab='Hits', cex.lab=1.6, cex.axis=2)
plot(res_comments, scale=0, shade=TRUE,  select=1, xlab='Term novelty', ylab='Comments', cex.lab=1.6, cex.axis=2)
plot(res_bookmarks, scale=0, shade=TRUE, select=1, xlab='Term novelty', ylab='Bookmarks', cex.lab=1.6, cex.axis=2)
plot(res_kudos, scale=0, shade=TRUE, select=2, xlab='Topic novelty', ylab='Kudos', cex.lab=1.6, cex.axis=2)
plot(res_hits, scale=0, shade=TRUE, select=2, xlab='Topic novelty', ylab='Hits', cex.lab=1.6, cex.axis=2)
plot(res_comments, scale=0, shade=TRUE,  select=2, xlab='Topic novelty', ylab='Comments', cex.lab=1.6, cex.axis=2)
plot(res_bookmarks, scale=0, shade=TRUE, select=2, xlab='Topic novelty', ylab='Bookmarks', cex.lab=1.6, cex.axis=2)
dev.off()
        


# produce results like the previous ones 
# res <- mgcv::gam(Kudos ~ s(Term_novelty, bs='cr', sp=0.8, k=12) + s(Topic_novelty, bs='cr', sp=0.8, k=12), data = df)

#family = 'nb' is better than default


