library("corrplot")
library("e1071")
library('mgcv')
library("reshape")
library("generalhoslem")

#project_model
a<-read.csv(file="RQ3/project_attri.csv", header = TRUE, sep = ",")
a_ <- a[complete.cases(a),]
summary(a_)

b<-cor(a_[,4:17], method= "spearman")
corrplot(b)
corrplot(b, method = "number", type = "upper", tl.cex = 1) 
corrplot(b,method="color",addCoef.col="grey") 

model1 = glm(log(total_earned+1) ~ log(commits+1) + log(issues+1) + log(stars+1)
             + num_round + team_member + log(len_description+1)
             + log(admin_profile_followers+1) + log(admin_grants_contributed+1) + log(admin_position+1) 
             + log(tweet_count+1),
             data = a, 
             family = gaussian(),
             na.action(na.omit))

summary(model1)
nobs(model1)
anova(model1,test="Chisq")
#McFadden's pseudo r-squared
with(summary(model1), 1 - deviance/null.deviance)

#grant_model
a<-read.csv(file="RQ3/grant_attri.csv", header = TRUE, sep = ",")
a_ <- a[complete.cases(a),]
summary(a_)

b<-cor(a_[,5:18], method= "spearman")
corrplot(b)
corrplot(b, method = "number", type = "upper", tl.cex = 1) 
corrplot(b,method="color",addCoef.col="grey") 

model2 = glm(log(total_earned+1) ~ log(issues+1) + log(stars+1)
             + round_times + team_member + log(len_description+1)
             + log(admin_profile_followers+1) + log(admin_grants_contributed+1) + log(admin_position+1)
             + log(tweet_count+1), 
             data = a, 
             family = gaussian(),
             na.action(na.omit))
summary(model2)
nobs(model2)
anova(model2,test="Chisq")
#McFadden's pseudo r-squared
with(summary(model2), 1 - deviance/null.deviance)



