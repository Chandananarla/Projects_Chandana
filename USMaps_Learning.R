
#Here we use the micromap and micromapST packages

#inorder to install the package, we use the install.packages() function
#install.packages("micromap")
#install.packages("micromapST")

#Loading the packages using library() function
library(micromap)
library(micromapST)

#Loading the csv file which is present in the loacl
veterans<-read.csv(file = "F:/chandana/CourseWork/Sem_1/Assignments/Stat515/ACS07and17Edited.csv",header = TRUE,as.is = TRUE)
veterans #checking the loaded data 51 Observations and 14 variables.

names(veterans) # cheching the coloumn variables

#Adding two variables Zero and change 
veterans$Zero <- rep(0, nrow(veterans))
veterans$change <- veterans$VET2017_PRCNT18PLUS_EST -
  veterans$VET2007_PRCNT18PLUS_EST

names(veterans) #checking whether the variables are added to the data set

veterans$UBchange <- veterans$change + veterans$CHANGE_MOE
veterans$LBchange <- veterans$change - veterans$CHANGE_MOE 

#Creating the micromap panel descirption

#Panel description for the required micromap

#since the type of micromap given is cumulative,we use type as mapcum 
type=c('mapcum','id','arrow','arrow','dotconf')

#Labelling and column values are set for the map below
lab1=c('Cumulative Map','U.S.','2007 To','0 To','2017 -2007')
lab2=c('','States','2017','2017-2007','and 90% CI')
col1 = c(NA,NA,'VET2007_PRCNT18PLUS_EST','Zero','change')
col2 = c(NA,NA,'VET2017_PRCNT18PLUS_EST','change','LBchange')
col3 = c(NA,NA,NA,NA,'UBchange')
refVals=c(NA,NA,NA,0,0)
panelDesc <- data.frame(type,lab1,lab2,col1,col2,col3,refVals)

#Creating a pdf file to save the output micromap
mmFile = "MicroMap_Veterans3B.pdf"
pdf(file=mmFile,width=7.5,height=10)

#creating the micromap for the veterans data
micromapST(veterans,panelDesc,
           rowNamesCol='State',
           rowNames='full',
           sortVar=16,ascend=FALSE,
           title=c("Veteran percentages of population 18 years and older: 2007 and 2017",
                   "by Chandana Narla"),
           ignoreNoMatches=FALSE)
dev.off()





