#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar  7 12:38:44 2022

@author: savvina
"""
#%%
import pandas as pd
import numpy as np
import random as rd
my_seed = 0
rd.seed(my_seed)
np.random.seed(my_seed)
#%%

def sort_user_dist(user_dist,pop_count, user_hist,pop_fraq,pop_item_fraq, by = "pop_fraq"):
    user_dist = user_dist.sort_index()
    user_dist_sorted = pd.DataFrame(data = user_dist)
    
    user_dist_sorted.columns = ["count"]
    
    user_dist_sorted["pop_count"] = pop_count
    user_dist_sorted["user_hist"] = user_hist
    user_dist_sorted["pop_fraq"] = pop_fraq
    user_dist_sorted["pop_item_fraq"] = pop_item_fraq
    
    user_dist_sorted = user_dist_sorted.sort_values(by=[by])
    return user_dist_sorted

def split(user_dist_sorted, top_fraction):
    low, med, high = np.split(user_dist_sorted, [int(top_fraction*len(user_dist_sorted)), int((1-top_fraction)*len(user_dist_sorted))])
    return low, med, high
    
def split_differently(user_dist_sorted, low_pop_fraq, med_pop_fraq, high_pop_fraq):
    us1 = user_dist_sorted.pop_fraq.expanding().mean()
    user_dist_sorted["us1"] = us1
    low = user_dist_sorted[user_dist_sorted.us1<=low_pop_fraq]
    new_usd = pd.concat([user_dist_sorted, low]).drop_duplicates(keep=False).drop("us1", axis = 1)
    low = low.drop("us1", axis=1)
    us1 = new_usd.pop_fraq.expanding().mean()
    new_usd["us1"] = us1
    med = new_usd[new_usd.us1<=med_pop_fraq]
    high = pd.concat([new_usd, med]).drop_duplicates(keep=False).drop("us1", axis = 1)
    med = med.drop("us1", axis=1)
    return low, med, high

def read(low_user_file, medium_user_file, high_user_file):
    low_users = pd.read_csv(low_user_file, sep=',').set_index('user_id')
    medium_users = pd.read_csv(medium_user_file, sep=',').set_index('user_id')
    high_users = pd.read_csv(high_user_file, sep=',').set_index('user_id')
    no_users = len(low_users) + len(medium_users) + len(high_users)
    print('No. of users: ' + str(no_users))
    
    mainstreaminess = "M_global_R_APC"
    
    print('Average mainstreaminess per user for low: ' + str(low_users[mainstreaminess].mean()))
    print('Average mainstreaminess per user for med: ' + str(medium_users[mainstreaminess].mean()))
    print('Average mainstreaminess per user for high: ' + str(high_users[mainstreaminess].mean()))
    return no_users, low_users, medium_users, high_users