  library(tidyverse)
  library(ggplot2) 
  #installing the usmap package to generate the USmap plot
  #install.packages("usmap")
  library(usmap)
  
  #Reading the CSV data file into a data frame
  shootingData=read.csv(file="F:/chandana/CourseWork/Sem_1/Assignments/Stat515/MidTerm/shootingdata_new_1.csv",header=TRUE)
  
  #There are certain blank rows in the csv file, To exclude the blank rows we use the below
  shootingData2<-shootingData[1:110,]
  shootingData2
  
  #Checking for null values
  is.na(shootingData2)
  
  #Assigning Levels to the Presidents using factor
  shootingData2$president<-factor(shootingData2$president,levels = c("Reagan","Bush Sr", "Clinton", "Bush",
                                                                     "Obama", "Trump"))
  xlabel<-c('Reagan \n  (1982-1989)','Bush Sr \n (1989-1992)','Clinton \n (1993-2000)','Bush \n (2001-2008)','Obama\n  (2009-2017)','Trump \n (2017-2019)')
  
  #Plot between Number of shootings and Presidents
  ggplot(shootingData2, aes(x=president,fill=president))+
    geom_bar()+
    labs(x='Presidential Terms',y='Number of shootings',title='Frequency of shooting under Presidential Terms') +
    scale_fill_brewer(palette = "Dark2")+scale_x_discrete(labels=xlabel)+
    geom_text(stat = 'count', aes(label=..count..), position=position_stack(1.10))
  
  #Plot between Location of Shooting and number of Shooting with presidency
  ggplot(shootingData2, aes(x=president, fill=categories))+
    geom_bar()+
    labs(x='Presidential Terms',y='Number of shootings',title='Frequency of shooting under Presidential Terms \n with respect to Location') +
    scale_fill_brewer(palette = "Dark2")+scale_x_discrete(labels=xlabel)
  
  #Plot between Location of Shooting and number of Shooting 
  ggplot(shootingData2, aes(x=categories,fill=categories))+
    geom_bar()+
    labs(x='Location of the Shootings',y='Number of shootings',title='Frequency of shooting with respect to Location') +
    scale_fill_brewer(palette = "Dark2")
  
  #Plot between States and the weapons obtained legally
  shootingData2$weapons_obtained_legally[shootingData2$weapons_obtained_legally == "Yes "] <- "Yes"
  
  shootingData2$weapons_obtained_legally<-factor(shootingData2$weapons_obtained_legally,levels = c('Yes','No','Unknown','TBD'))
  ggplot(shootingData2, aes(x=Location_ab, fill=weapons_obtained_legally))+
    geom_bar()+
    labs(x='States in the US',y='Number of shootings',title='Frequency of Shootings in each state \n  Based on the Weapons Obtained') +
    scale_fill_brewer(palette = "Dark2")
  
  
  #Plot between Weapons Obtained and the Presidential terms 
  shootingData2$weapons_obtained_legally[shootingData2$weapons_obtained_legally == "Yes "] <- "Yes"
  
  shootingData2$weapons_obtained_legally<-factor(shootingData2$weapons_obtained_legally,levels = c('Yes','No','Unknown','TBD'))
  ggplot(shootingData2, aes(x=president, fill=weapons_obtained_legally))+
    geom_bar()+
    labs(x='Presidential Terms',y='Number of shootings',title='Frequency of shooting under Presidential Terms \n with respect to Weapons Obtained') +
    scale_fill_brewer(palette = "Dark2")+scale_x_discrete(labels=xlabel)
  
  #States Prone to Shootings
  
  #using the usmap to show the most prone shooting states in the US
  #Considering the Total Victims column to interpret the shootings at that location
  
  a1<-shootingData2[, c('Location_ab', 'total_victims')]
  count2<-aggregate(cbind(count = total_victims) ~ Location_ab, 
                       data  = a1, 
                       FUN = function(x){NROW(x)})
  
  colnames(count2)<-c('state','count')
  
  plot_usmap(data=count2, values='count',lines='black',labels='True')+
    labs(title = "Mass shootings in USA from 1982 to 2019")+
    scale_fill_continuous(
      low = "orange", high = "red", name = "Mass shooting", label = scales::comma
    ) + theme(legend.position = "right")
  
  
  
