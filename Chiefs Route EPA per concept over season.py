# -*- coding: utf-8 -*-
"""
Created on Wed Jul 21 15:29:07 2021

@author: Mark Schofield
"""

import pandas as pd
import numpy as np
from sklearn.neighbors import KernelDensity
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.gridspec as grid_spec
import seaborn as sns; sns.set_theme()
mydata = pd.read_csv("C:\\Users\Mark Schofield\\Desktop\\dfPlay4.csv")
mydata = pd.read_csv("C:\\Users\Mark Schofield\\Desktop\\SkillPositionPlayers.csv")

colors = ['#97233F', '#006778', '#FF3C00', '#4F2683', '#203731', 
          '#FFB612','#69BE28', '#D3BC8D','#0085CA']
dfSkill = pd.read_csv('C:\\Users\Mark Schofield\\Desktop\\SkillPositionPlayers.csv')
dfPlay = pd.read_csv('C:\\Users\Mark Schofield\\Desktop\\dfPlay4.csv')

dfPlay = dfPlay[dfPlay['concept_cv'].str.contains('y-cross')]
dfPlay = dfPlay[dfPlay['OffensiveTeam']=='Chiefs']
                                     
dfPlay['PlayID'] = dfPlay['GameID'].astype(str) + dfPlay['EventID'].astype(str)
dfSkill['PlayID'] = dfSkill['GameID'].astype(str) + dfSkill['EventID'].astype(str)
dfSkill2 = dfSkill[dfSkill['PlayID'].isin(dfPlay.PlayID.unique())]
dfSkill2 = dfSkill[dfSkill['PlayID'].isin(dfPlay.PlayID.unique())]
dfSkill2 = dfSkill2.merge(dfPlay[['PlayID','Week','EPA']],on='PlayID')
dfSkill2['Order_OutsideToInside'].fillna('0', inplace=True)
dfSkill2['Order_OutsideToInside'] = dfSkill2['Order_OutsideToInside'].astype(int)
dfSkill2['Pos'] = dfSkill2['SideOfCenter'].astype(str)+(dfSkill2['Order_OutsideToInside'].astype(str))


#%% Get and order routes/coverages
routes = dfSkill2.groupby('Route').count()
routes = routes['EPA']
routes = routes.sort_values(ascending=False)
routes = routes.reset_index()
routes = routes['Route']
weeks = dfSkill2.groupby('Week').count()
weeks = weeks['EPA']
weeks = weeks.sort_values(ascending=False)
weeks = weeks.reset_index()
weeks = weeks['Week']

#%% Group by Route/Coverage
dfSkill3 = dfSkill2[['Route','Week','EPA']]
dfSkill4 = dfSkill3.groupby(['Route','Week']).mean()
dfSkill4.reset_index(inplace=True)
dfSkill4['Route'] = pd.Categorical(dfSkill4['Route'], routes)
dfSkill4['Week'] = pd.Categorical(dfSkill4['Week'], weeks)
dfSkill4 = dfSkill4.sort_values(['Route', 'Week'])
dfSkill5 = dfSkill4.pivot('Route','Week','EPA')
cmap = sns.color_palette("Spectral", as_cmap=True)
# ax = sns.heatmap(dfSkill5, linewidths=.5, vmin=-0.25, vmax=0.25, cmap=cmap, yticklabels=True, cbar_kws={'label': 'EPA/Pass'})

#%% Find complementary routes
route = 'Curl'
dfSkill2['Order_OutsideToInside'].fillna('0', inplace=True)
dfSkill2['Order_OutsideToInside'] = dfSkill2['Order_OutsideToInside'].astype(int)
dfSkill2['SideOfCenter'].fillna('C', inplace=True)
dfSkill2['Pos'] = dfSkill2['SideOfCenter'].astype(str)+(dfSkill2['Order_OutsideToInside'].astype(str))
dfSkill2['RouteID'] = dfSkill2['PlayID']+dfSkill2['Pos']
dfSkill6 = dfSkill2[dfSkill2['Route']==route]

playIDs = dfSkill6['PlayID'].unique()
dfSkill7 = dfSkill2[dfSkill2['PlayID'].isin(playIDs)]

dfSkill8 = dfSkill7[['Route', 'Week', 'EPA']]

dfSkill9 = dfSkill8.groupby(['Route','Week']).mean()
dfSkill9.reset_index(inplace=True)
dfSkill9['Route'] = pd.Categorical(dfSkill9['Route'], routes)
dfSkill9['Week'] = pd.Categorical(dfSkill9['Week'], weeks, ordered=True)
dfSkill9 = dfSkill9.sort_values(['Route', 'Week'])
dfSkill10 = dfSkill9.pivot('Route','Week','EPA')
ax = sns.heatmap(dfSkill10, linewidths=.5, vmin=-0.25, vmax=0.25, cmap=cmap, yticklabels=True, cbar_kws={'label': 'EPA/Pass by Week for KC'})
