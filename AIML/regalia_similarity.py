#!/usr/bin/env python
# coding: utf-8

# In[27]:


import numpy as np
from pandas import read_csv
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer


# In[28]:


get_ipython().system('pip install rake-nltk')
from rake_nltk import Rake


# In[30]:


df=read_csv("regalia_product.csv",sep=",")
df.head()


# In[31]:


df.columns = df.columns.str.strip()
df['productid'] = df['productid'].astype(int)


# In[33]:


df.columns


# In[34]:


df1 = df[['productid','product_name','sku','sub_product_id','product_rating']].copy()
df1.head()


# In[35]:


import nltk
nltk.download('stopwords')
nltk.download('punkt')


# In[36]:


df1['keywords'] = ""
lst = []


# In[37]:


for index,row in df1.iterrows():
    prodname = row['product_name']

    r = Rake()
    r.extract_keywords_from_text(prodname)

    key_words_dict_scores = r.get_word_degrees()  
    
    lst.append(list(key_words_dict_scores.keys()))
    


# In[38]:


df1['keywords'] = lst


# In[39]:


df1.head()


# In[40]:


df1.set_index('productid', inplace = True)
df1.head()


# In[41]:


df1['text'] = ''
columns = ['product_name','sub_product_id']
lst = []
for index, row in df1.iterrows():
    words = ''
    for col in columns:
        words = words + ' ' + row[col] + ' '
    print(words)
    lst.append(words)
df1['text'] = lst


# In[42]:


columns = ['text','keywords']
lst = []
for index, row in df1.iterrows():
    words = ''
    for col in columns:
        words = words + ' '.join(row[col]) + ' '
    print(words)
    lst.append(words)
df1['bag_of_words'] = lst


# In[43]:


df1['bag_of_words'].head(5)
df1.drop(['sku','sub_product_id','product_name','text','keywords'], axis = 1, inplace = True)
df1.head()


# In[44]:


count = CountVectorizer()
count_matrix = count.fit_transform(df1['bag_of_words'])
count_matrix


# In[45]:


indices = pd.Series(df1.index)
indices[:5]
cosine_sim = cosine_similarity(count_matrix, count_matrix)
cosine_sim


# In[46]:


cosine_sim.shape


# In[47]:


def recommendations(Product_ID, cosine_sim = cosine_sim):
    recommended_prods = []
    
    idx = indices[indices == Product_ID].index[0]
    
    score_series = pd.Series(cosine_sim[idx]).sort_values(ascending = False)
    
    top20_indexes = list(score_series.iloc[1:21].index)
    
    for i in top20_indexes:
        recommended_prods.append(list(indices)[i])
    return recommended_prods


# In[48]:


recommended_prods = recommendations(202212001)


# In[49]:


for index,row in df.iterrows():
    for i in recommended_prods:
        if row['productid'] == i:
            print(row['product_name'])


# In[50]:


import pickle

filename = 'cosine_sim.sav' #model_dumpfile_name
pickle.dump(cosine_sim, open(filename, 'wb')) #name of model and variable


# In[51]:


loaded_cosine = pickle.load(open("cosine_sim.sav", 'rb'))
loaded_cosine
pickle.dump(indices, open("indices.sav", 'wb')) #name of model and variable


# In[52]:


loaded_indices = pickle.load(open("indices.sav", 'rb'))
loaded_indices


# In[ ]:




