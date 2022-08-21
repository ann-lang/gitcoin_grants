library(lmerTest)
library(lme4)
library(MuMIn)
library(car)

d = read.csv('RQ2/ITS/info.csv')
head(d)
d$pk = as.factor(d$pk)

# commit model
Q1 <- quantile(d$num_commit, .25)
Q3 <- quantile(d$num_commit, .75)
IQR <- IQR(d$num_commit)
no_outliers <- subset(d, d$num_commit > (Q1 - 1.5*IQR) & d$num_commit < (Q3 + 1.5*IQR))
m_commit = lmer(log(num_commit+0.001) ~
           log(earning_after_adoption)
         + month_index 
         + intervention 
         + time_after_intervention
         #+ count_grant
         + num_repo
         + (1|pk)
         , data = no_outliers
         , REML = FALSE)
m_commit2 = lmer(log(num_commit+0.001) ~
                  log(earning_after_adoption)
                + month_index 
                + intervention 
                + time_after_intervention
                + count_grant
                + num_repo
                + (1|pk)
                , data = no_outliers
                , REML = FALSE)
dim(no_outliers)
vif(m_commit)
summary(m_commit)
r.squaredGLMM(m_commit)
anova(m_commit, m_commit2)
Anova(m_commit)



# comment model
Q1 <- quantile(d$num_comment, .25)
Q3 <- quantile(d$num_comment, .75)
IQR <- IQR(d$num_comment)
no_outliers <- subset(d, d$num_comment > (Q1 - 1.5*IQR) & d$num_comment < (Q3 + 1.5*IQR))
m_comment = lmer(log(num_comment+0.001) ~
                  log(earning_after_adoption)
                + month_index 
                + intervention 
                + time_after_intervention
                + num_repo
                + (1|pk)
                , data = no_outliers
                , REML = FALSE)

vif(m_comment)
summary(m_comment)
r.squaredGLMM(m_comment)
Anova(m_comment)


# star model
Q1 <- quantile(d$num_star, .25)
Q3 <- quantile(d$num_star, .75)
IQR <- IQR(d$num_star)
no_outliers <- subset(d, d$num_star > (Q1 - 1.5*IQR) & d$num_star < (Q3 + 1.5*IQR))
m_star = lmer(log(num_star+0.001) ~
                   log(earning_after_adoption)
                 + month_index 
                 + intervention 
                 + time_after_intervention
                 + num_repo
                 + (1|pk)
                 , data = no_outliers
                 , REML = FALSE)

vif(m_star)
summary(m_star)
r.squaredGLMM(m_star)
Anova(m_star)

