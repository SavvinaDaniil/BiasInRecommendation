#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar  4 18:10:26 2022

@author: savvina
"""
#%%
import numpy as np
import pandas as pd
from sklearn.metrics import auc
import random as rd
import pickle as pkl
my_seed = 0
rd.seed(my_seed)
np.random.seed(my_seed)
#%%
def users_and_items(df_events, user_col, item_col):
    print('No. user events: ' + str(len(df_events)))
    print('No. items: ' + str(len(df_events[item_col].unique())))
    print('No. users: ' + str(len(df_events[user_col].unique())))
    print("\n")
    
    
    
def user_distribution(df_events, user_col, item_col, prnt = False):
    user_dist = df_events[user_col].value_counts() 
    num_users = len(user_dist)
    if prnt:
        print('Mean '+item_col+'s per user: ' + str(np.round(user_dist.mean(),1))) 
        print('Min '+item_col+'s per user: ' + str(np.round(user_dist.min(),1))) 
        print('Max '+item_col+'s per user: ' + str(np.round(user_dist.max(),1)))
        print("\n")
    return user_dist, num_users


def user_country_distribution(df, user_col, odds_col,  prnt = False):
    
    user_dict = {}
    for user in df[user_col].unique():
        user_df = df[df[user_col] == user]
        num_USA = len(user_df[user_df.country=="USA"])
        num_rest = len(user_df[user_df.country!="USA"])
        user_dict[user] = [num_USA, num_rest]
    user_country_dist = pd.DataFrame.from_dict(user_dict, orient="index",columns=["num_USA", "num_rest"])
    user_country_dist["num_total"] = user_country_dist["num_USA"] + user_country_dist["num_rest"] 
    user_country_dist["ratio_USA"] = user_country_dist["num_USA"]/user_country_dist["num_total"] 
    num_users = len(user_country_dist)
    if prnt:
        print('Mean '+odds_col+'s per user: ' + str(np.round(user_country_dist[odds_col].mean(),5)))
        print('Standard deviation of '+odds_col+'s per user: ' + str(np.round(user_country_dist[odds_col].std(),5)))
        print('Min '+odds_col+'s per user: ' + str(np.round(user_country_dist[odds_col].min(),5))) 
        print('Max '+odds_col+'s per user: ' + str(np.round(user_country_dist[odds_col].max(),5)))
    
    return user_country_dist.sort_values(by=odds_col), num_users


def item_distribution(df_events, user_col, item_col, prnt = False):
    item_dist = df_events[item_col].value_counts()
    num_items = len(item_dist)
    if prnt:
        print('Mean users per '+item_col+': ' + str(np.round(item_dist.mean(),1))) 
        print('Min users per '+item_col+': ' + str(np.round(item_dist.min(),1))) 
        print('Max users per '+item_col+': ' + str(np.round(item_dist.max(),1))) 
        print("\n")
    return item_dist, num_items
#%%
def calculate_popularity(df_events, top_item_dist, item_dist, num_users, user_col, item_col):
    pop_count = [] # number of top items per user
    user_hist = [] # user history sizes
    pop_fraq = [] # relative number of top items per user
    pop_item_fraq = [] # average popularity of items in user profiles
    for u, df in df_events.groupby(user_col):
        no_user_items = len(set(df[item_col]))
        no_user_pop_items = len(set(df[item_col]) & set(top_item_dist.index))
        pop_count.append(no_user_pop_items)
        user_hist.append(no_user_items) 
        pop_fraq.append(no_user_pop_items / no_user_items)
        user_pop_item_fraq = sum(item_dist[df[item_col]] / num_users) / no_user_items
        pop_item_fraq.append(user_pop_item_fraq)
    output = open('data/'+item_col+'_pop_fraq.pkl', 'wb')
    pkl.dump(pop_fraq, output)
    output.close()

    output = open('data/'+item_col+'_user_hist.pkl', 'wb')
    pkl.dump(user_hist, output)
    output.close()

    output = open('data/'+item_col+'_pop_count.pkl', 'wb')
    pkl.dump(pop_count, output)
    output.close()

    output = open('data/'+item_col+'_pop_item_fraq.pkl', 'wb')
    pkl.dump(pop_item_fraq, output)
    output.close()

    return pop_count,user_hist,pop_fraq, pop_item_fraq

#%%
def read_popularity(item_col):
    pkl_file = open('data/'+item_col+'_pop_fraq.pkl', 'rb')
    pop_fraq = pkl.load(pkl_file)
    pkl_file.close()
    pkl_file = open('data/'+item_col+'_user_hist.pkl', 'rb')
    user_hist = pkl.load(pkl_file)
    pkl_file.close()
    pkl_file = open('data/'+item_col+'_pop_count.pkl', 'rb')
    pop_count = pkl.load(pkl_file)
    pkl_file.close()
    pkl_file = open('data/'+item_col+'_pop_item_fraq.pkl', 'rb')
    pop_item_fraq = pkl.load(pkl_file)
    pkl_file.close()
    return pop_count,user_hist, pop_fraq, pop_item_fraq
#%%
def calculate_group_characteristics(low, med, high, count_column = "user_hist", way = "popularity"):
    low_profile_size = low[count_column].mean()
    med_profile_size = med[count_column].mean()
    high_profile_size = high[count_column].mean()
    
    low_nr_users = len(low)
    med_nr_users = len(med)
    high_nr_users = len(high)
    
    if way == "popularity":
        low_GAP = low.pop_item_fraq.mean()
        med_GAP = med.pop_item_fraq.mean()
        high_GAP = high.pop_item_fraq.mean()
    
        return low_profile_size, med_profile_size, high_profile_size, low_nr_users, med_nr_users, high_nr_users, low_GAP, med_GAP, high_GAP
    else:
        return low_profile_size, med_profile_size, high_profile_size, low_nr_users, med_nr_users, high_nr_users

def calculate_gini_coefficient(item_dist):
    total_uses = sum(item_dist.values)
    full_item_dist_df = pd.DataFrame(item_dist)[::-1]
    full_item_dist_df.columns = ["single_count"]
    full_item_dist_df["single_percentage"] = full_item_dist_df["single_count"]/total_uses
    cdf = np.cumsum(full_item_dist_df["single_percentage"].values)
    movs = np.array(range(1,len(item_dist)+1))/len(item_dist)
    A = auc(movs,movs) - auc(movs,cdf)
    AplusB = auc(movs,movs)
    GC = A/AplusB
    return GC, movs, cdf