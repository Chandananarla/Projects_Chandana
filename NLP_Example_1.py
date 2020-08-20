#!/usr/bin/env python
# coding: utf-8


import nltk
import re
from nltk.corpus import stopwords
nltk.download('punkt')

ch_contents = open('F:/chandana/CourseWork/Sem_1/Assignments/AIT580/material/DATA/BikeInjury.txt', 'rt')
chandana_contents = ch_contents.read() # to read the contents from the loaded file
print(chandana_contents) #checking whether the contents are loaded properly


value1 = re.sub(r'\W+', ' ', chandana_contents) #here we replace the substrings in the given data
value1 = value1.lower() #converts the uppercase to lower case
value1 = value1.split() 
value1 = [word for word in value1 if word not in stopwords.words('english')]
print(value1)


injuries = ['contusion','head','neck','lung','broken','scrapes','knee','fractured','lacerations','elbows'
            ,'clavicle','ribs','limbs','traumatic','elbow','forearm','brain','stomach','thigh','shoulders',
            'wrist','chin','hip','hematoma','abrasion']

common_injuries = [] #assigning variable to store the common inury values

for i in injuries:
    for j in value1:
        if i == j:
            common_injuries.append(i)    

#Graph of frequent types of biking injuries
            
freq_dist = nltk.FreqDist(common_injuries)
print(freq_dist)
print(freq_dist.most_common(25))
freq_dist.plot(25)



tokens_description = nltk.sent_tokenize(chandana_contents)

print(tokens_description[0])
print(tokens_description[1])
print(tokens_description[2])
print(tokens_description[3])
print(tokens_description[4])
print(tokens_description[5])
print(tokens_description[6])
print(tokens_description[7])
print(tokens_description[9])
print(tokens_description[10])






