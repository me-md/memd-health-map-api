import os
import pandas as pd
import geopandas as gpd
import psycopg2
import sqlalchemy as db
import matplotlib.pyplot as plt
import descartes
import platform
import mapclassify as mc
import json
import seaborn as sns
import numpy as np
import io
from datetime import datetime

# from sqlalchemy import create_engine
# POSTGRES_ADDRESS = 'localhost'
# POSTGRES_PORT = '5432'
# POSTGRES_USERNAME = 'nathanthomas'
# POSTGRES_PASSWORD = 'cashflow'
# POSTGRES_DBNAME = 'conditions'
# postgres_str = (f'postgresql://{POSTGRES_USERNAME}:{POSTGRES_PASSWORD}@{POSTGRES_ADDRESS}:{POSTGRES_PORT}/{POSTGRES_DBNAME}')
#
# cnx = create_engine(postgres_str)

conditions = pd.read_sql_query('SELECT * FROM conditions_map_conditions;', cnx)

conditions = conditions[['name', 'state']]
conditions_map_data = conditions.rename(index=int, columns={'name':'CONDITION', 'state':'STATE_ABBR'})

states= gpd.read_file('/Users/nathanthomas/turing/4module/projects/mymd2/testing_testing/Data/states.shp')
states_formatted = states[['STATE_ABBR', 'geometry']]

usa = states_formatted[~states_formatted.STATE_ABBR.isin(['HI', 'AK'])]

merged = usa.set_index('STATE_ABBR').join(conditions_map_data.set_index('STATE_ABBR'))

grpd = merged.groupby(['STATE_ABBR','CONDITION']).size().to_frame('NUM').reset_index()

def fetch_map_data(condition):
    user_condition = grpd[grpd.CONDITION == f'{condition}']
    joined = usa.set_index('STATE_ABBR').join(user_condition.set_index('STATE_ABBR')).reset_index()
    values = {'CONDITION': 'no record', 'NUM': 0}
    rtp = joined.fillna(value = values)
    return rtp

def plot_map(condition):
    map_data = fetch_map_data(condition)
    ax = map_data.dropna().plot(column=map_data.NUM,
                                figsize=(15,9),
                                cmap='Blues',
                                edgecolor='black',
                                linewidth=0.8)

    ax.axis('off')
    ax.set_title(f'MeMD {condition.capitalize()} Diagnosis Across the US', fontdict={'fontsize': '35', 'fontweight' : '5'})
    current_time = datetime.now()
    date = current_time.strftime('%m-%d-%Y')
    ax.annotate(f'This map is a representation of {condition} diagnosis across the US among MeMD users only. Last Updated: {date}', xy=(0.1, .08),  xycoords='figure fraction', horizontalalignment='left', verticalalignment='top', fontsize=12, color='#555555')
    fig = ax.get_figure()
    cbax = fig.add_axes([0.82, 0.26, 0.01, 0.27])
    cbax.set_title('MeMD Users')


    sm = plt.cm.ScalarMappable(cmap='Blues', \
                    norm=plt.Normalize(vmin=min(map_data.NUM), vmax=max(map_data.NUM)))
    sm._A = []

    fig.colorbar(sm, cax=cbax, format="%d")

    ax.get_figure()
    return ax
