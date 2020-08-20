#!/usr/bin/env python
# coding: utf-8

# In[ ]:


#Importing the required packages

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sn

import statsmodels.api as sm
from scipy import stats

#Reading the csv file into the googleplaystore data frame
googlePlayStore= pd.read_csv('C:/Users/chand/Documents/ChandanaNarla/chandana/CourseWork/Sem_1/Assignments/AIT580/AITFinal/googleplaystore.csv')

#Checking whether the data set has been imported correctly
googlePlayStore

#Data cleaning for columns like size and installs and make them Ratio/ Integer from nominal data types for more accurate results
googlePlayStore['Size']=googlePlayStore['Size'].map(lambda x: x.rstrip('M')) #rstrip removes the right arguments

#here we are converting the KB into MB
#here we use strip() which removes the given arguments in the data
googlePlayStore['Size']=googlePlayStore['Size'].map(lambda x: str(round((float(x.strip('k'))/1024),1)) if x[-1]=='k' else x)

googlePlayStore['Size']=googlePlayStore['Size'].map(lambda x: np.nan if x.startswith('Varies') else x)

googlePlayStore['Size']    #All the App sizes are now commonly measured in MB


#here we removd the plus sign inorder to order the data and make it integer so that we could visualize the data
googlePlayStore['Installs']=googlePlayStore['Installs'].map(lambda x: x.rstrip('+'))
googlePlayStore['Installs']=googlePlayStore['Installs'].map(lambda x: ''.join(x.split(',')))
googlePlayStore['Installs']
#here we removed the $ sign inorder to use the Price of the app for futher predictions
#we use the lstrip() function to remove the dollar sign present on the left most
googlePlayStore['Price']=googlePlayStore['Price'].map(lambda x: x.lstrip('$').rstrip())  
googlePlayStore['Price']

#Checking for the NAN, NULL values in the considered dataframe.
googlePlayStore.isnull().sum()

#Since it has the null values, we drop the values and clean the dataset
googlePlayStore=googlePlayStore.dropna()  #dropna() is used to drop the NULL values from the dataframe
googlePlayStore

#to check the datatypes of the elements
googlePlayStore.dtypes

#to check whether the data is cleaned properly
googlePlayStore.to_csv('C:/Users/chand/Documents/ChandanaNarla/chandana/CourseWork/Sem_1/Assignments/AIT580/AITFinal/googleplaystore_CleanedData.csv')

#to convert the required columns into numeric / integers for better data visualizations and regression
googlePlayStore['Size']=pd.to_numeric(googlePlayStore['Size'])
googlePlayStore['Installs']=pd.to_numeric(googlePlayStore['Installs'])
googlePlayStore['Price']=pd.to_numeric(googlePlayStore['Price'])
googlePlayStore['Reviews']=pd.to_numeric(googlePlayStore['Reviews'])


#Visualizations
plt.figure(figsize=(50,8))
plt.hist(googlePlayStore['Category'],color='Green',bins=35)
plt.xlabel('Category of the App')
plt.ylabel('Number of Apps')
plt.title('To know which Category of App is more prevailing')

#Box Plots between Category and Rating
plt.figure(figsize=(60,9))
sn.boxplot(x='Category', y='Rating',data=googlePlayStore)
plt.title('To know the Most Prevailing Category in Apps')
plt.show()

#Box Plots between Category and Rating with Type (whether the App is Paid or Not)
plt.figure(figsize=(60,9))
sn.boxplot(x='Category', y='Rating',hue='Type',data=googlePlayStore)
plt.title('To know the Most Prevailing Category based on the Payment for Apps')
plt.show()

#Correlation Analysis
googlePlayStore.corr()
sn.pairplot(googlePlayStore)

#Scatter Plot between Content Rating and Reviews
plt.figure(figsize=(20,10))
plt.scatter(googlePlayStore['Content Rating'],googlePlayStore['Reviews'],color='red')
plt.xlabel('Content Rating')
plt.ylabel('Reviews')
plt.title('Relattion between the content rating and the Reviews')
#Scatter Plot between Content Rating and installs
plt.figure(figsize=(20,10))
plt.scatter(googlePlayStore['Content Rating'],googlePlayStore['Installs'],color='Orange')
plt.xlabel('Content Rating')
plt.ylabel('Installs')
plt.title('Relattion between the content rating and the Installs')


#Linear Regression
#Inorder to convert the Content Rating and Genre into numeric values
label_encoder=preprocessing.LabelEncoder()
googlePlayStore['Content Rating']=label_encoder.fit_transform(googlePlayStore['Content Rating'])
googlePlayStore['Genres']=label_encoder.fit_transform(googlePlayStore['Genres'])

#Target is rating and preicting varibles are Price, Size and Content Rating
targetcord=pd.DataFrame(googlePlayStore['Rating'])
X1=googlePlayStore[['Price','Size','Content Rating']]
Y=targetcord['Rating']
model_regression1=sm.OLS(Y,X1).fit()
model_predictions=model_regression1.predict(X1)
model_regression1.summary()

#Target is rating and preicting varibles are Price, Size, Content Rating and Genres
targetcord=pd.DataFrame(googlePlayStore['Rating'])
X2=googlePlayStore[['Price','Size','Content Rating','Genres']]
Y=targetcord['Rating']
model_regression2=sm.OLS(Y,X2).fit()
model_predictions=model_regression.predict(X2)
model_regression2.summary()

#Hypothesis Testing
data_hypothesis1=googlePlayStore[['Content Rating','Price']]

ttest1,pval1=stats.ttest_rel(data_hypothesis1['Content Rating'],data_hypothesis1['Price'])
print("Pvalue is "+ pval1.astype(str))
if pval1<0.05:
    print("We reject null hypothesis")
else:
    print("We accept null hypothesis")
    
data_hypothesis2=googlePlayStore[['Category','Price']]

ttest2,pval2=stats.ttest_rel(data_hypothesis2['Category'],data_hypothesis2['Price'])
print("Pvalue is "+ pval2.astype(str))
if pval2<0.05:
    print("We reject null hypothesis")
else:
    print("We accept null hypothesis")  
    
data_hypothesis3=googlePlayStore[['Category','Installs']]

ttest3,pval3=stats.ttest_rel(data_hypothesis3['Category'],data_hypothesis3['Installs'])
print("Pvalue is "+ pval3.astype(str))
if pval3<0.05:
    print("We reject null hypothesis")
else:
    print("We accept null hypothesis")

