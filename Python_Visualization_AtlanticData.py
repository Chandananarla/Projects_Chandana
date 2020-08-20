#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pandas as pd
import os
atlantic_data=pd.read_csv("C:/Users/chandana/Documents/Atlantic.csv")
atlantic_data
atlantic_data.dtypes

#Question 1a)
#Summary for Each data item
print(atlantic_data['year'].describe())
print(atlantic_data['cyclone_of_the_year'].describe())
print(atlantic_data['date'].describe())
print(atlantic_data['time'].describe())
print(atlantic_data['status_of_system'].describe())
print(atlantic_data['latitude'].describe())
print(atlantic_data['longitude'].describe())
print(atlantic_data['max_sustained_wind'].describe())
print(atlantic_data['central_pressure'].describe())

#Visualizations for the data items
import matplotlib.pyplot as plt


plt.hist(atlantic_data['cyclone_of_the_year'],width=2.5,color='orange')
plt.xlabel('Cyclones of the year',color='Black')
plt.ylabel('Number of cyclones of the year',color='Black')
plt.title('Visualization of the Cyclones of the year')

plt.hist(atlantic_data['year'],color='Green',bins=100)
plt.xlabel('Year',color='Black')
plt.ylabel('Number of years',color='Black')
plt.title('Visualization of the Year')

plt.hist(atlantic_data['time'],color='Green',width=200)
plt.xlabel('Time',color='Black')
plt.ylabel('Count',color='Black')
plt.title('Visualization of the Duration')

plt.hist(atlantic_data['date'],color='Orange')
plt.xlabel('date',color='Black')
plt.ylabel('Count',color='Black')
plt.title('Visualization of the date')

plt.plot(atlantic_data['date'],color='Orange')
plt.xlabel('date',color='Black')
plt.ylabel('Count',color='Black')
plt.title('Visualization of the date')

plt.hist(atlantic_data['status_of_system'],color='orange',bins=20)
plt.title('Visualization of System Status')
plt.xlabel('Status of System')
plt.ylabel('Count')

plt.hist(atlantic_data['latitude'],color='Orange',width=50)
plt.xlabel('latitude',color='Black')
plt.ylabel('Count',color='Black')
plt.title('Visualization of the latitude')

plt.hist(atlantic_data['longitude'],color='Orange',width=100)
plt.xlabel('longitude',color='Black')
plt.ylabel('Count',color='Black')
plt.title('Visualization of the longitude')

plt.hist(atlantic_data['max_sustained_wind'],color='Blue',width=25)
plt.xlabel('Maximum Wind Sustained',color='Black')
plt.ylabel('Count',color='Black')
plt.title('Visualization of the Maximum Wind Sustained')

plt.hist(atlantic_data['central_pressure'],color='Blue',width=150)
plt.xlabel('central_pressure',color='Black')
plt.ylabel('Count',color='Black')
plt.title('Visualization of the Central Pressure')


#Relationship between Max Wind Sustained and Centeral Pressure
plt.scatter(atlantic_data['max_sustained_wind'],atlantic_data['central_pressure'],color='Blue')
plt.title('Relation between Centeral Pressure and Max wind Sustained')
plt.xlabel('Max wind sustained')
plt.ylabel('Centeral Pressure')


#Relationship Between Max wind Sustained and Status of the System
plt.scatter(atlantic_data['status_of_system'],atlantic_data['max_sustained_wind'],color='Red')
plt.xlabel('Status of the System')
plt.ylabel('Maximum Wind Sustained')
plt.title('Scatter plot between Status of the system and Max wind Sustained')


#Dealing with Missing Values 
#To check the presence of null values and represented using True
print(atlantic_data.isnull())

#To give the summary of missing values
atlantic_data.isnull().sum()
atlantic_data.fillna(atlantic_data.mean(), inplace=True) 

atlantic_data.isnull().sum()

#There are missing values which are present in the atlantic data set 
#are normalized using the mean values.



import requests  # To get the url
import pandas as pd
import re  #For the Clean Up of data
from bs4 import  BeautifulSoup
from pandas import DataFrame as df

#Getting the contents of the given url
url=requests.get('https://top500.org/list/2019/06/?page=1')
print(url.text[0:500])





# In[ ]:




