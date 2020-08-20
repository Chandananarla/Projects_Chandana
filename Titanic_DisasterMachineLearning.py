#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import missingno as msno
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from xgboost import XGBClassifier
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import RandomizedSearchCV, train_test_split
from sklearn.metrics import accuracy_score


# In[10]:


import seaborn as sns


# In[5]:


df = pd.read_csv('C:/Users/chand/Documents/ChandanaNarla/chandana/GMU/CourseWork/Sem_2/SYS568/Assignments/titanic_train.csv')


# In[6]:


df.head()


# In[7]:


df.columns


# In[8]:


print(pd.isna(df).sum())


# In[232]:


msno.matrix(df)


# #There are missing values in Age, Cabin and Embarked

# In[11]:


corr = df.corr()
ax = sns.heatmap(
    corr, 
    vmin=-1, vmax=1, center=0,
    cmap=sns.diverging_palette(20, 220, n=200),
    square=True
)
ax.set_xticklabels(
    ax.get_xticklabels(),
    rotation=45,
    horizontalalignment='right'
);


# In[234]:


#Dropping 'cabin' as it has many missing data, Ticket and Name are the categorical columns which do not have any 
#contribution towards our prediction. 
df.drop(['PassengerId','Cabin','Ticket','Name'],axis=1,inplace=True)


# In[235]:


df.head()


# In[236]:


pd.isna(df[['Age','Embarked']]).sum()


# In[237]:


plt.hist(df['Age'], bins='auto')
plt.show()


# In[238]:


#df['Age'].mean()
#df['Age'].median()
#df['Age'].fillna(28,inplace=True)


# In[239]:


df['Embarked'].value_counts()
#Imputing missing Embarked values with mode.
df['Embarked'].fillna("S",inplace=True)
pd.isna(df[['Age','Embarked']]).sum()


# In[240]:


df.info()


# In[241]:


convert_dict = {'Pclass': object} 
df = df.astype(convert_dict) 
print(df.dtypes)


# In[242]:


#df['Age'] = df.groupby(['Sex', 'Pclass'])['Age'].apply(lambda x: x.fillna(x.median()))


# In[243]:


IsAlone = []
for i, j in zip(df.iloc[:,4], df.iloc[:, 5]):
    k=i+j;
    IsAlone.append(k);
df['IsAlone']=IsAlone
df = df.drop(["SibSp","Parch"],axis=1)


# In[244]:


#Pclass, Sex, Embarked
df = pd.get_dummies(df)


# In[259]:


df


# In[246]:


from sklearn.impute import KNNImputer
imputer = KNNImputer(n_neighbors=5,weights="uniform")
temp=imputer.fit_transform(df[['Age','Sex_female','Sex_male']])


# In[247]:


df[['Age','Sex_female','Sex_male']]=temp
df.head()


# In[248]:


pd.isna(df).sum()


# In[249]:


x=df.iloc[:,1:]
y=df.iloc[:,0]


# In[250]:


xtr, xts, ytr, yts = train_test_split(x,y)


# In[304]:


rf = RandomForestClassifier(n_jobs=-1, n_estimators=1000)

#paramRf = {"n_estimators" : [100, 200, 300, 400, 500],"max_depth" : [10, 12, 14, 16, 18, 20],
#            "min_samples_leaf" : [5, 10, 15, 20],"class_weight" : ['balanced','balanced_subsample']}
 
#rf = RandomizedSearchCV(estimator = rfc_grid, param_distributions = paramRf, cv = 10, n_iter=10,n_jobs=-1)


# In[305]:


svm = SVC(C=1, kernel = 'linear', degree=5)

#paramSvm = { 'C': [1, 5, 10],'kernel': ['rbf','linear'],'degree': [3, 5, 7],'gamma': [0.5, 1, 1.5, 2, 5]}
 
#svm = RandomizedSearchCV(estimator = svm_grid, param_distributions = paramSvm, cv= 10, n_iter=10,n_jobs=-1)


# In[306]:


xg = XGBClassifier(min_child_weight=5, gamma=1, subsample=0.6, colsample_bytree=0.6,max_depth=3)

#paramXg = {'min_child_weight': [1, 5, 10],'gamma': [ 1, 2, 5],'subsample': [0.6, 0.8, 1.0],
#           'colsample_bytree': [0.6, 0.8, 1.0],'max_depth': [3, 4, 5]}
 
#xg = RandomizedSearchCV(estimator = xgb_grid, param_distributions = paramXg, cv = 10, n_iter=10,n_jobs=-1)


# In[307]:


rf.fit(xtr,ytr)
predRf = rf.predict(xts)


# In[308]:


svm.fit(xtr,ytr)
predSvm = svm.predict(xts)


# In[309]:


xg.fit(xtr,ytr)
predXg = xg.predict(xts)


# In[310]:


print(accuracy_score(yts,predRf))
print(accuracy_score(yts,predSvm))
print(accuracy_score(yts,predXg))


# In[258]:


from sklearn.ensemble import VotingClassifier
from sklearn import model_selection
estimators = []
estimators.append(('Random Forest', rf))
estimators.append(('SVM', svm))
estimators.append(('XGBoost', xg))
#create the ensemble model
ensemble = VotingClassifier(estimators)
results = model_selection.cross_val_score(ensemble, xtr,ytr, cv=10,n_jobs=-1)
print(results.mean())


# In[ ]:





# In[ ]:





# In[289]:


predRf = rf.predict(NewDf)
predSvm = svm.predict(NewDf)
predXg = xg.predict(NewDf)


# In[272]:


NewDf = pd.read_csv('C:/Users/samsu/Desktop/Spring 2020/OR 568/Assignment 4/1/test.csv')


# In[273]:


len(NewDf)


# In[274]:


print(pd.isna(NewDf).sum())


# In[275]:


print(NewDf['Fare'].median())
NewDf['Fare'].fillna(14.45,inplace=True)


# In[276]:


print(pd.isna(NewDf).sum())


# In[277]:


NewDf1=NewDf.iloc[:,0]


# In[278]:


NewDf.drop(['PassengerId','Cabin','Ticket','Name'],axis=1,inplace=True)


# In[279]:


convert_dict = {'Pclass': object} 
NewDf = NewDf.astype(convert_dict)


# In[284]:


IsAlone = []
for i, j in zip(NewDf.iloc[:,3], NewDf.iloc[:, 4]):
    k=i+j;
    IsAlone.append(k);
NewDf['IsAlone']=IsAlone
NewDf = NewDf.drop(["SibSp","Parch"],axis=1)


# In[285]:


NewDf = pd.get_dummies(NewDf)


# In[286]:


NewDf.head()


# In[287]:


temp1=imputer.transform(NewDf[['Age','Sex_female','Sex_male']])
NewDf[['Age','Sex_female','Sex_male']]=temp1
NewDf.head()


# In[288]:


print(pd.isna(NewDf).sum())


# In[290]:


a=pd.DataFrame(predRf)


# In[291]:


b=pd.DataFrame(predSvm)


# In[292]:


c=pd.DataFrame(predXg)


# In[293]:


d=pd.DataFrame(NewDf1)


# In[294]:


a=a.rename(columns={0: "Survived"})


# In[295]:


b=b.rename(columns={0: "Survived"})


# In[296]:


c=c.rename(columns={0: "Survived"})


# In[297]:


framesRf=[d,a]
resultRf=pd.concat(framesRf,axis=1)


# In[298]:


framesSvm=[d,b]
resultSvm=pd.concat(framesSvm,axis=1)


# In[299]:


framesXg=[d,c]
resultXg=pd.concat(framesXg,axis=1)


# In[300]:


resultRf.to_csv(r'C:/Users/samsu/Desktop/Spring 2020/OR 568/Assignment 4/1/SubmissionRf.csv', index = False)


# In[301]:


resultSvm.to_csv(r'C:/Users/samsu/Desktop/Spring 2020/OR 568/Assignment 4/1/SubmissionSvm.csv', index = False)


# In[302]:


resultXg.to_csv(r'C:/Users/samsu/Desktop/Spring 2020/OR 568/Assignment 4/1/SubmissionXg.csv', index = False)


# In[ ]:





# In[ ]:





# In[ ]:




