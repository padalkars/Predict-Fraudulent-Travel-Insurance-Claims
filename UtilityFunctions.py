#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np


# In[27]:


class GetStats():
    def __init__(self, data):
        self.data = data
    
    #Find the count of missing values 
    def find_missing_values(self):
        features = list(self.data.columns)
        missing_value_count = self.data.isnull().sum()
        missing_value_percentage = missing_value_count * 100/self.data.shape[0]
        
        missing_value_df = pd.DataFrame({'Features': features,                                         'Missing Value Count': missing_value_count,                                         'Missing Value Percentage': missing_value_percentage},                                         columns = ['Features', 'Missing Value Count',                                                    'Missing Value Percentage'])
        
        #Sort in descending order of missing value count
        missing_value_df = missing_value_df.sort_values(by='Missing Value Count',                                                        ascending=False)
        
        return missing_value_df
    
    def check_types(self, dtype):
        if(dtype=='float' or dtype=='float64'):
            return 'Float'
        if(dtype=='int64' or dtype=='int'):
            return 'Integer'
        if(dtype=='datetime64'):
            return 'Date Time'
        if(dtype=='O'):
            return 'Categorical'
        return 'Other Type'
    
    #Get the data types of variables
    def get_data_types(self):
        data_types = pd.DataFrame(self.data.dtypes) #Obtain the data types of the column
        data_types = data_types.reset_index() #A new column named 'index' will be created
        
        #Rename the columns 
        data_types = data_types.rename(columns = {'index':'Features',                                                   0:'Data Types'})
        
        data_types['Data Types'] = list(map(lambda val: self.check_types(val),                                         data_types['Data Types']))
        
        return data_types
    
    def get_numeric_stats(self, data_types_df):
        #Stats for numeric variables
        numeric_vars = data_types_df.loc[(data_types_df['Data Types']=='Float') |                                      (data_types_df['Data Types']=='Integer'), 'Features'].tolist()
        numeric_stats = self.data[numeric_vars].describe().T
        
        numeric_stats = numeric_stats.reset_index()
        numeric_stats = numeric_stats.rename(columns = {'index':'Features'})
        
        return numeric_stats
    
    def get_category_count(self, data_types_df):
        cat_vars_stats = data_types_df.loc[data_types_df['Data Types']=='Categorical',                                    ['Features']]
        
        cat_vars_stats["Unique Categories"] = list(map(lambda var:len(np.unique(self.data[var])),                                                      cat_vars_stats['Features'].tolist()))
        
        return cat_vars_stats    
        
    #Driver function
    def driver(self):
        '''
        Merge the data frames obtained from various statistics
        '''
        missing_value_df = self.find_missing_values()
        
        data_types = self.get_data_types()
        
        stats_df = pd.merge(missing_value_df, data_types, on='Features', how='left')
        
        #Get the statistics for numeric variables
        numeric_stats = self.get_numeric_stats(data_types)
        stats_df = pd.merge(stats_df, numeric_stats, how='left', on='Features')
        
        #Count the number of categories
        cat_vars_stats = self.get_category_count(data_types)
        stats_df = pd.merge(stats_df, cat_vars_stats, how='left', on='Features')
        
        return stats_df


# In[12]:


#set(pd.DataFrame(train_data.dtypes)[0])\
#{dtype('int64'), dtype('float64'), dtype('O')}


# In[4]:


'''
train_data = pd.read_csv("train.csv")
train_data.head()
''' 


# In[28]:


#Get the descriptive statistics of the data
'''
stats_obj = GetStats(train_data)

data_stats = stats_obj.driver()

data_stats.head()
'''


# In[ ]:




