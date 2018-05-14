
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
value=pd.read_csv("C:/work/machine/meinian/05.data/train.csv")


# In[2]:


value.describe()


# In[3]:


def ya_clean(x):
    try:
        y = float(x)
        if y>=250 or y<=30:
            y = np.nan
    except:
        y = np.nan
    return y
    


# In[4]:


value['a']=value['a'].apply(ya_clean)
value['b']=value['b'].apply(ya_clean)


# In[5]:


def e_clean(x):
    try:
        y = float(x)
        if y<0:
            y = np.nan
    except:
        y = np.nan
    return y

value['e']=value['e'].apply(e_clean)


# In[6]:


value.describe()


# In[7]:


def c_clean(x):
    try:
        y = float(x)
        if y<0:
            y = np.nan
    except:
        y = np.nan
    return y
value['c']=value['c'].apply(c_clean)


# In[8]:


value.describe()


# In[9]:


#value


# In[10]:


value.to_csv("C:/work/machine/meinian/05.data/value_clean.csv",index=False)


# In[11]:


print (value[value.isnull().values==True])




