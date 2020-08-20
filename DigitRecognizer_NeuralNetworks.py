#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd


# In[2]:


train = pd.read_csv('C:/Users/chand/Documents/ChandanaNarla/chandana/GMU/CourseWork/Sem_2/SYS568/Assignments/digitalreco_train.csv')
test = pd.read_csv('C:/Users/chand/Documents/ChandanaNarla/chandana/GMU/CourseWork/Sem_2/SYS568/Assignments/digitalreco_test.csv')


# In[3]:


train.shape


# In[4]:


train.isnull().sum()[train.isnull().sum() > 0]


# In[5]:


from sklearn.model_selection import train_test_split


# In[6]:


y = train.label
X = train.drop('label',1)


# In[113]:


xtr,xts,ytr,yts = train_test_split(X, y)


# In[114]:


import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')


# In[115]:


xtr_shaped = xtr.values.reshape(xtr.shape[0],28, 28)
xts_shaped = xts.values.reshape(xts.shape[0],28, 28)


# In[141]:


plt.imshow(xtr_shaped[1399])
print(ytr.iloc[1399])


# In[117]:


xtr= xtr / 255
xts = xts / 255


# In[118]:


import tensorflow as tf


# In[122]:


model = tf.keras.models.Sequential()


# In[123]:


model.add(tf.keras.layers.Dense(180, activation= 'relu', input_shape=(784,)))
model.add(tf.keras.layers.Dense(110, activation= 'relu'))
model.add(tf.keras.layers.Dense(10, activation= 'softmax'))


# In[124]:


model.compile(optimizer=tf.keras.optimizers.Adam(), loss = 'sparse_categorical_crossentropy')


# In[125]:


model.fit(xtr.values,ytr.values,epochs = 2)


# In[126]:


pred = model.predict(xts.values)


# In[127]:


pred.argmax(1)


# In[128]:


from sklearn.metrics import accuracy_score


# In[129]:


accuracy_score(yts, pred.argmax(1))


# In[130]:


test = test / 255


# In[133]:


predicted = model.predict(test.values)


# In[134]:


predicted.argmax(1)


# In[135]:


a=pd.DataFrame(predicted.argmax(1))
a=a.rename(columns={0: "Label"})


# In[136]:


b=list(range(1,28001))
b=pd.DataFrame(b)
b=b.rename(columns={0: "ImageId"})


# In[137]:


frames = [b,a]
result = pd.concat(frames,axis=1)


# In[138]:


result.to_csv(r'C:/Users/samsu/Desktop/Spring 2020/OR 568/Assignment 4/2/Submission.csv', index = False)


# In[ ]:





# In[ ]:





# In[ ]:




