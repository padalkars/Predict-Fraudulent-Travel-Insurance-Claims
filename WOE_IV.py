#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
from collections import Counter


# In[2]:


#Check the target distribution
def get_distribution(cat_var, data):
    '''
    Input
    cat_var:- A categorical variable
    Results
    counts_df:- A data frame containing the counts and the % of entries
    '''
    counts = dict(Counter(data[cat_var]))
    
    counts_df = pd.DataFrame({"Category": counts.keys(),                               "Values": counts.values()},                            columns=["Category", "Values"])
    total = sum(counts_df["Values"])
    
    counts_df["Percentage"] = counts_df["Values"]*100/total
    
    #Sort in descending order of counts
    counts_df = counts_df.sort_values(by="Values", ascending=False)
    
    return counts_df


# In[42]:


'''
Adjusted WOE = 
ln([(non_event_count + 0.5)/total_non_event]/[(event_count + 0.5)/total_event])
'''

def woe_sanity(ind, woe_iv_df, total_event, total_non_event):
    '''
    For each index of the woe_iv_df data frame compute the woe values
    ["Event Count", "Non Event Count", "Event %", "Non Event %"]
    '''
    event_per, non_event_per = woe_iv_df.loc[ind, "Event %"], woe_iv_df.loc[ind, "Non Event %"]
    event_count, non_event_count = woe_iv_df.loc[ind, "Event Count"], woe_iv_df.loc[ind, "Non Event Count"] 
        
    if((event_count==0) or (non_event_count==0)):
        numerator = (non_event_count + 0.5)/total_non_event
        denominator = (event_count + 0.5)/total_event
        #np.ln(numerator/denominator)
        adjusted_woe =(np.log(numerator/denominator))/(np.log(np.e)) 
        
        return adjusted_woe
    woe = non_event_per/event_per
    
    return woe


# In[30]:


def create_df(column_list, value_list):
    '''
    Input
    column_list:- Contains a list of column names for the data frame
    value_list:- It's a list of lists containing the set of values for each column
    '''
    df = pd.DataFrame(columns=column_list)
    for col, values in zip(column_list, value_list):
        df[col] = values
    
    return df

def caluclate_woe_iv(woe_iv_df):
    woe_cat_wise = [] #Stores the woe calculations for each category
    
    total_events = sum(woe_iv_df["Event Count"])
    total_non_events = sum(woe_iv_df["Non Event Count"])
    
    woe_iv_df["Total Counts"] = woe_iv_df["Event Count"] + woe_iv_df["Non Event Count"]
    woe_iv_df["Event %"] = woe_iv_df["Event Count"]/total_events
    woe_iv_df["Non Event %"] = woe_iv_df["Non Event Count"]/total_non_events

    woe_iv_df["Event Rate"] = woe_iv_df["Event Count"]/woe_iv_df["Total Counts"]
    
    woe_cat_wise = [woe_sanity(ind, woe_iv_df, total_events, total_non_events)                     for ind in woe_iv_df.index]
    
    woe_iv_df["WOE"] = woe_cat_wise
    
    return woe_iv_df

def woe_iv(cat_var, data, events='Good', non_events='Bad', target='Listing_Type'):
    data_grp = data[[cat_var, target]].groupby(cat_var)
    event_counts, non_event_counts = [], []
    categories = []
    
    for grp, df in data_grp:
        categories.append(grp)
        event_count = df.loc[df[target]==events, :].shape[0]
        non_event_count = df.shape[0] - event_count
        event_counts.append(event_count)
        non_event_counts.append(non_event_count)
    
    #Create a data frame for this distribution
    column_list = ["Categories", "Event Count", "Non Event Count"]
    value_list = [categories, event_counts, non_event_counts]
    woe_iv_df = create_df(column_list, value_list)
    
    #Compute percentage of events and non-event
    woe_iv_df = caluclate_woe_iv(woe_iv_df)
    
    #Sort the data in descending order of counts
    woe_iv_df = woe_iv_df.sort_values(by="Total Counts", ascending=False)

    return woe_iv_df


# In[25]:


sample_df = pd.DataFrame({"City":["Mumbai", "Mumbai", "Delhi", "Delhi",                                   "Kolkata", "Kolkata"],                         "Listing_Type": ["Good", "Good", "Good", "Good", "Bad", "Bad"]},                        columns = ["City", "Listing_Type"])
sample_df


# In[43]:


woe_iv("City", sample_df)

