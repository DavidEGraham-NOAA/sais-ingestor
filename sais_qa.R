#sais IHS dataset qa processing
observations<-seq_len(656744)
#randomly select 250 observation points for quality check
set.seed(42)
samp<-sample(observations,250,replace=FALSE)
