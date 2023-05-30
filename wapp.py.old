# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import math
import os
import base64

import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px

import dash
import dash_table
from dash_table.Format import Format
import dash_table.FormatTemplate as FormatTemplate
from dash_table.Format import Format, Group, Scheme, Symbol
import dash_core_components as dcc
import dash_html_components as html
import dash_daq as daq
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from babel import Locale
from babel.numbers import format_currency


###################################
# Private function and variable
###################################

def  get_data_num(case_type):    
    '''
    Generate case table, incremental number and percentage
    '''
    df_tmp = pd.read_csv('./lineplot_data/df_{}.csv'.format(case_type))
    df_tmp = df_tmp.astype({'Date': 'datetime64'})
    plusNum = df_tmp['plusNum'][0]
    plusPercent = df_tmp['plusPercentNum'][0]

    return df_tmp, plusNum, plusPercent

def make_country_table(countryName):
    '''This is the function for building df for Province/State of a given country'''
    countryTable = df_latest.loc[df_latest['Country/Region'] == countryName]
    # Suppress SettingWithCopyWarning
    pd.options.mode.chained_assignment = None
    countryTable['Faturamento'] = countryTable['fatur']
    countryTable['Ativas'] = countryTable['A']
    countryTable['Inaugurar'] = countryTable['I']
    countryTable['Analise'] = countryTable['N']
    countryTable['Clientes'] = countryTable['clientes']
    countryTable['Cli/Pop'] = ((countryTable['clientes'] / countryTable['population'])*100).round(decimals=3)
    countryTable['Fat/Cli'] = (countryTable['fatur'] / countryTable['clientes'])
    countryTable['Funcionarios'] = countryTable['funcion']
    countryTable['Func/Cli'] = countryTable['funcion'] / countryTable['clientes']
    countryTable['Chamados'] = countryTable['chamados']

    countryTable = countryTable[['Province/State', 'Faturamento', 'Ativas', 'Inaugurar', 'Analise', 'Clientes', 'Cli/Pop', 'Fat/Cli',  'Funcionarios', 'Func/Cli', 'Chamados', 'lat', 'lon']]

    countryTable = countryTable.sort_values(by=['Faturamento'], ascending=False).reset_index(drop=True)
    # Set row ids pass to selected_row_ids
    countryTable['id'] = countryTable['Province/State']
    countryTable.set_index('id', inplace=True, drop=False)
    # Turn on SettingWithCopyWarning
    pd.options.mode.chained_assignment = 'warn'

    return countryTable


def make_dcc_country_tab(countryName, dataframe):
    '''This is for generating tab component for country table'''
    if countryName == 'Australia':
        return dcc.Tab(
                id='tab-datatable-interact-location-{}'.format(countryName),
                label=countryName,
                value=countryName,
                className='custom-tab',
                selected_className='custom-tab--selected',
                children=[
                    dash_table.DataTable(
                        id='datatable-interact-location-{}'.format(countryName),
                        # Don't show coordinates
                        columns=[{"name": 'Province/State', "id": 'Province/State'}
                                    if i == 'Province/State' else {"name": 'Country/Region', "id": 'Country/Region'}
                                        for i in dataframe.columns[0:1]] +
                                [{"name": i, "id": i, "type": "numeric","format": FormatTemplate.percentage(2)}
                                    if i == 'Death rate' or i == 'Positive rate' else {"name": i, "id": i, 'type': 'numeric', 'format': Format(group=',')}
                                        for i in dataframe.columns[1:10]],
                        # But still store coordinates in the table for interactivity
                        data=dataframe.to_dict("rows"),
                        #css= [{'selector': 'tr:hover', 'rule': 'background-color: #2674f6;'}],
                        row_selectable="single",
                        sort_action="native",
                        style_as_list_view=True,
                        style_cell={'font_family': 'Roboto',
                                    'backgroundColor': '#ffffff', 
                        },
                        fixed_rows={'headers': True, 'data': 0},
                        style_table={'minHeight': '400px',
                                     'height': '400px',
                                     'maxHeight': '400px',
                                     'overflowX': 'auto',
                        },
                        style_header={'backgroundColor': '#ffffff',
                                      'fontWeight': 'bold'},
                        style_cell_conditional=[{'if': {'column_id': 'Province/State'}, 'width': '22%'},
                                                {'if': {'column_id': 'Country/Regions'}, 'width': '22%'},
                                                {'if': {'column_id': 'Active'}, 'width': '8%'},
                                                {'if': {'column_id': 'Confirmed'}, 'width': '8%'},
                                                {'if': {'column_id': 'Recovered'}, 'width': '8%'},
                                                {'if': {'column_id': 'Deaths'}, 'width': '8%'},
                                                {'if': {'column_id': 'Death rate'}, 'width': '8%'},
                                                {'if': {'column_id': 'Tests'}, 'width': '8%'},
                                                {'if': {'column_id': 'Positive rate'}, 'width': '10%'},
                                                {'if': {'column_id': 'Tests/100k'}, 'width': '10%'},    
                                                {'if': {'column_id': 'Confirmed/100k'}, 'width': '10%'},
                                                {'if': {'column_id': 'Active'}, 'color':'#f0953f'},
                                                {'if': {'column_id': 'Confirmed'}, 'color': '#f03f42'},
                                                {'if': {'column_id': 'Recovered'}, 'color': '#2ecc77'},
                                                {'if': {'column_id': 'Deaths'}, 'color': '#7f7f7f'},
                                                {'textAlign': 'center'}
                        ],
                    ),
                ]
            )
    else:
        return dcc.Tab(
                #id='tab-datatable-interact-location-{}'.format(countryName) if countryName != 'United States' else 'tab-datatable-interact-location-US',
                id='tab-datatable-interact-location-{}'.format(countryName),
                label=countryName,
                value=countryName,
                className='custom-tab',
                selected_className='custom-tab--selected',
                children=[
                    dash_table.DataTable(
                        id='datatable-interact-location-{}'.format(countryName),
                        # Don't show coordinates
                        columns=[{"name": 'Province/State', "id": 'Province/State'}
                                    if i == 'Province/State' else {"name": 'Country/Region', "id": 'Country/Region'}
                                        for i in dataframe.columns[0:1]] +
                        	[{"name": i, "id": i, "type": "numeric","format": FormatTemplate.percentage(2)}
                            	    if i == 'Cli/Pop' or i == 'Func/Cli' else 
                        	{"name": i, "id": i, "type": "numeric","format": FormatTemplate.money(0)}
				    	   if i == 'Fat/Cli' else
						{"name": i, "id": i, 'type': 'numeric', 'format': Format(group=',')}
                                for i in dataframe.columns[1:11]],
                        # But still store coordinates in the table for interactivity
                        data=dataframe.to_dict("rows"),
                        #css= [{'selector': 'tr:hover', 'rule': 'background-color: #2674f6;'}],
                        row_selectable="single",
                        sort_action="native",
                        style_as_list_view=True,
                        style_cell={'font_family': 'Roboto',
                                    'backgroundColor': '#ffffff', 
                        },
                        fixed_rows={'headers': True, 'data': 0},
                        style_table={'minHeight': '400px',
                                     'height': '400px',
                                     'maxHeight': '400px',
                                     'overflowX': 'auto',
                        },
                        style_header={'backgroundColor': '#ffffff',
                                      'fontWeight': 'bold'},
                	style_cell_conditional=[
                                        	{'if': {'column_id': 'Province/State'}, 'width': '17%'},
						{'if': {'column_id': 'Country/Region'}, 'width': '17%'},
                                        	{'if': {'column_id': 'Faturamento'}, 'width': '8%'},
                                        	{'if': {'column_id': 'Ativas'}, 'width': '8%'},
                                        	{'if': {'column_id': 'Inaugurar'}, 'width': '8%'},
                                        	{'if': {'column_id': 'Analise'}, 'width': '8%'},
                                        	{'if': {'column_id': 'Clientes'}, 'width': '8%'},
                                        	{'if': {'column_id': 'Cli/Pop'}, 'width': '8%'},
                                        	{'if': {'column_id': 'Fat/Cli'}, 'width': '8%'},
                                        	{'if': {'column_id': 'Funcionarios'}, 'width': '9%'},
                                        	{'if': {'column_id': 'Func/Cli'}, 'width': '9%'},    
                                        	{'if': {'column_id': 'Chamados'}, 'width': '9%'},
                                        	{'if': {'column_id': 'Analise'}, 'color':'#f0953f'},
                                        	{'if': {'column_id': 'Faturamento'}, 'color': '#f03f42'},
                                        	{'if': {'column_id': 'Inaugurar'}, 'color': '#2ecc77'},
                                        	{'if': {'column_id': 'Ativas'}, 'color': '#7f7f7f'},
                                        	{'textAlign': 'center'}
                        ],
                    ),
                ]
            )

def render_region_map(countyrdata, dff, latitude, longitude, zoom):

    '''
    This is the function to render map for Brazil, Chile, Germany and Spain
    '''

    hovertext_value = ['Faturamento: ${:n}<br>População: {:.0f}<br>Clientes: {:.0f}<br>Cli/Pop: {:.2%}'.format(h, i, j, k) 
                            for h, i, j, k in zip(
				countyrdata['fatur'],
                                countyrdata['population'], 
                                countyrdata['clientes'],
                                countyrdata['clientes']/countyrdata['population']
                            ) 
    ] 
    
    # MapBox Token here!
    #mapbox_access_token = "pk.eyJ1IjoicGxvdGx5bWFwYm94IiwiYSI6ImNqdnBvNDMyaTAxYzkzeW5ubWdpZ2VjbmMifQ.TXcBE-xg9BFdV2ocecc_7g"
    mapbox_access_token = "pk.eyJ1Ijoid2FuZGVyZWxzayIsImEiOiJja2ZxcDB2aHowbmFnMnNzOXZ4dXNsc3lvIn0.ZmAPFa_Vcnhg5UdX4GKgKw"

    # Generate a list for hover text display
    textList = []
    for area, region in zip(countyrdata['Province/State'], countyrdata['Country/Region']):

        if type(area) is str:
            textList.append(area+', '+region)
        else:
            textList.append(region)

    fig2 = go.Figure(go.Scattermapbox(
        lat=countyrdata['lat'],
        lon=countyrdata['lon'],
        mode='markers',
        marker=go.scattermapbox.Marker(
            color='#f03f42',
            size=[i**(1/3) for i in countyrdata['population']],
            sizemin=1,
            sizemode='area',
            sizeref=2.*max([math.sqrt(i)
                for i in countyrdata['population']])/(100.**2),
        ),
        text=textList,
        hovertext=hovertext_value,
        hovertemplate="<b>%{text}</b><br><br>" +
                      "%{hovertext}<br>" +
                      "<extra></extra>")
    )
    fig2.update_layout(
        plot_bgcolor='#ffffff',
        paper_bgcolor='#ffffff',
        margin=go.layout.Margin(l=10, r=10, b=10, t=0, pad=40),
        hovermode='closest',
        transition={'duration': 500},
        mapbox=go.layout.Mapbox(
            accesstoken=mapbox_access_token,
            style="light",
            # The direction you're facing, measured clockwise as an angle from true north on a compass
            bearing=0,
            center=go.layout.mapbox.Center(
                lat=latitude,
                lon=longitude
            ),
            pitch=0,
            zoom=zoom
        )
    )

    return fig2

input_list = [
    Input('tabs-table', 'value'),
    Input('datatable-interact-location', 'derived_virtual_selected_rows'),
    Input('datatable-interact-location', 'selected_row_ids'),
    Input('datatable-interact-location-Brazil', 'derived_virtual_selected_rows'),
    Input('datatable-interact-location-Brazil', 'selected_row_ids'),
    Input('datatable-interact-location-Chile', 'derived_virtual_selected_rows'),
    Input('datatable-interact-location-Chile', 'selected_row_ids'),
    Input('datatable-interact-location-Germany', 'derived_virtual_selected_rows'),
    Input('datatable-interact-location-Germany', 'selected_row_ids'),
    Input('datatable-interact-location-Spain', 'derived_virtual_selected_rows'),
    Input('datatable-interact-location-Spain', 'selected_row_ids'),
]

################################################################################
# Data processing
################################################################################
# Method #1
# Import csv file and store each csv in to a df list
# NOTE all following steps really rely on the correct order of these csv files in folder raw_data

filename = os.listdir('./wraw_data/')

brazil_file_name = [i for i in filename if i.endswith('Brazil_data.csv')]
chile_file_name = [i for i in filename if i.endswith('Chile_data.csv')]
germany_file_name = [i for i in filename if i.endswith('Germany_data.csv')]
spain_file_name = [i for i in filename if i.endswith('Spain_data.csv')]

path = os.getcwd()
# Import Brazil data
for f in brazil_file_name:
    df_brazil = pd.read_csv(os.path.join(path+'/wraw_data', f), encoding='utf-8')

# Import Germany data
for f in germany_file_name:
    df_germany = pd.read_csv(os.path.join(path+'/wraw_data', f), encoding='UTF-8')

# Import Chile data
for f in chile_file_name:
    df_chile = pd.read_csv(os.path.join(path+'/wraw_data', f), encoding='UTF-8')

# Import Spain data
for f in spain_file_name:
    df_spain = pd.read_csv(os.path.join(path+'/wraw_data', f), encoding='UTF-8')

df_latest = pd.concat([df_brazil, df_chile, df_germany, df_spain]).reset_index(drop=True)

# Create data table to show in app
# Generate sum values for Country/Region level
cols = df_latest.columns.values.tolist()

cols.remove('modelo')
metadata = df_latest[cols].copy()
dfe = df_latest.groupby([df_latest['Province/State'], 'state_name', 'Country/Region', 'modelo'])['modelo'].count().unstack().reset_index().fillna(0)

# Transform float into integer
dfe_cols = ['premium','smart','express']
dfe[dfe_cols] = dfe[dfe_cols].applymap(np.int64)

cols.remove('status')
metadata = df_latest[cols].copy()
dfx = df_latest.groupby([df_latest['Province/State'], 'state_name', 'Country/Region', 'status'])['status'].count().unstack().reset_index().fillna(0)
# Transform float into integer
dfx_cols = ['A','I','N']
dfx[dfx_cols] = dfx[dfx_cols].applymap(np.int64)

dfz = dfe.merge(dfx)

df_latest = dfz.merge(metadata)

df_latest[['population', 'population_proper', 'fatur', 'compras', 'funcion', 'clientes', 'chamados']].astype('int')

df_latest[['Province/State', 'state_name', 'Country/Region', 'iso2', 'state_id']] = df_latest[['Province/State', 'state_name', 'Country/Region', 'iso2', 'state_id']].astype(str)

df_latest.to_csv(os.path.join(path+'/wraw_data/output.csv'), encoding='utf-8')

# Construct confirmed cases dataframe for line plot and 24-hour window case difference
df_confirmed, plusConfirmedNum, plusPercentNum1 = get_data_num('confirmed')

# Construct recovered cases dataframe for line plot and 24-hour window case difference
df_recovered, plusRecoveredNum, plusPercentNum2 = get_data_num('recovered')

# Construct death case dataframe for line plot and 24-hour window case difference
df_deaths, plusDeathNum, plusPercentNum3 = get_data_num('deaths')

# Construct remaining case dataframe for line plot and 24-hour window case difference
df_remaining, plusRemainNum, plusRemainNum3 = get_data_num('remaining')

#dfCase = df_latest.groupby([df_latest.city, 'state_name', 'country'], sort=False).sum().reset_index()
dfCase = df_latest.groupby([df_latest['Province/State'], 'state_name', 'Country/Region', 'iso2', 'state_id', 'fatur', 'compras'], sort=False).sum().reset_index()

# Rearrange columns 
dfCase = dfCase[['Province/State', 'state_name', 'Country/Region', 'express', 'premium', 'smart', 'A', 'I', 'N', 'iso2', 'state_id', 'population', 'population_proper', 'fatur', 'compras', 'funcion', 'clientes', 'chamados']]


dfCase = dfCase.sort_values(
    by=['Province/State'], ascending=False).reset_index(drop=True)

# Grep lat and lon by the first instance to represent its Country/Region
dfGPS = df_latest.groupby([df_latest['Province/State'], 'state_name', 'Country/Region'], sort=False).first().reset_index()
dfGPS = dfGPS[['Province/State', 'lat', 'lon', 'Country/Region']]

# Merge two dataframes
dfCase = dfCase.sort_values(
			by=['Province/State'], ascending=True).reset_index(drop=True)
dfGPS = dfGPS.sort_values(
			by=['Province/State'], ascending=True).reset_index(drop=True)

WorldwildTable = pd.merge(dfCase, dfGPS)

# Save numbers into variables to use in the app

faturamento = WorldwildTable['fatur'].sum().astype(int)
unidAtivas = WorldwildTable['A'].sum()
unidInaug = WorldwildTable['I'].sum() 
unidAnalise = WorldwildTable['N'].sum()
unidPremium = WorldwildTable['premium'].sum()
unidSmart = WorldwildTable['smart'].sum()
unidExpress = WorldwildTable['express'].sum()

unidAtivas_p = WorldwildTable.loc[(WorldwildTable['premium'] == 1) & (WorldwildTable['A'] == 1)].count().unique()[0]
unidAtivas_s = WorldwildTable.loc[(WorldwildTable['smart'] == 1) & (WorldwildTable['A'] == 1)].count().unique()[0]
unidAtivas_e = WorldwildTable.loc[(WorldwildTable['express'] == 1) & (WorldwildTable['A'] == 1)].count().unique()[0]

unidInaug_p = WorldwildTable.loc[(WorldwildTable['premium'] == 1) & (WorldwildTable['I'] == 1)].count().unique()[0]
unidInaug_s = WorldwildTable.loc[(WorldwildTable['smart'] == 1) & (WorldwildTable['I'] == 1)].count().unique()[0]
unidInaug_e = WorldwildTable.loc[(WorldwildTable['express'] == 1) & (WorldwildTable['I'] == 1)].count().unique()[0]

unidAnalise_p = WorldwildTable.loc[(WorldwildTable['premium'] == 1) & (WorldwildTable['N'] == 1)].count().unique()[0]
unidAnalise_s = WorldwildTable.loc[(WorldwildTable['smart'] == 1) & (WorldwildTable['N'] == 1)].count().unique()[0]
unidAnalise_e = WorldwildTable.loc[(WorldwildTable['express'] == 1) & (WorldwildTable['N'] == 1)].count().unique()[0]

fatur_p = WorldwildTable.fatur[WorldwildTable['premium'] == 1].sum().astype(int)
fatur_s = WorldwildTable.fatur[WorldwildTable['smart'] == 1].sum().astype(int)
fatur_e = WorldwildTable.fatur[WorldwildTable['express'] == 1].sum().astype(int)

WorldwildTable['Ativas_P'] = (WorldwildTable.apply(lambda x: 1 if (x.premium == 1 and x.A == 1) else 0, axis=1))
WorldwildTable['Ativas_S'] = (WorldwildTable.apply(lambda x: 1 if (x.smart == 1 and x.A == 1) else 0, axis=1))
WorldwildTable['Ativas_E'] = (WorldwildTable.apply(lambda x: 1 if (x.express == 1 and x.A == 1) else 0, axis=1))

WorldwildTable = WorldwildTable.groupby(by='Country/Region', sort=False, as_index=False).agg({'Country/Region': 'first', 'express': 'sum', 'premium': 'sum', 'smart': 'sum', 'A': 'sum', 'I': 'sum', 'N': 'sum', 'population': 'sum', 'population_proper': 'sum', 'fatur': 'sum', 'compras': 'sum', 'funcion': 'sum', 'clientes': 'sum', 'chamados': 'sum', 'lat': 'first', 'lon': 'first', 'Ativas_P': 'sum', 'Ativas_S': 'sum', 'Ativas_E': 'sum'})

WorldwildTable.to_csv(os.path.join(path+'/wraw_data/WorldwildTable.csv'), encoding='utf-8')

WorldwildTable['Faturamento'] = WorldwildTable['fatur']
WorldwildTable['Clientes'] = WorldwildTable['clientes']
WorldwildTable['Cli/Pop'] = ((WorldwildTable['clientes'] / WorldwildTable['population'])*100).round(decimals=3)
WorldwildTable['Fat/Cli'] = (WorldwildTable['fatur'] / WorldwildTable['clientes'])
WorldwildTable['Funcionarios'] = WorldwildTable['funcion']
WorldwildTable['Func/Cli'] = WorldwildTable['funcion'] / WorldwildTable['clientes']
WorldwildTable['Chamados'] = WorldwildTable['chamados']
WorldwildTable['Compras'] = WorldwildTable['compras']
WorldwildTable['Compras/Fat'] = ((WorldwildTable['compras']/WorldwildTable['fatur'])*100).round(decimals=3)
WorldwildTable['Ativas'] = WorldwildTable['A']
WorldwildTable['Inaugurar'] = WorldwildTable['I']
WorldwildTable['Analise'] = WorldwildTable['N']

# Rearrange columns to correspond to the number plate order
WorldwildTable = WorldwildTable[['Country/Region', 'Faturamento', 'Ativas', 'Inaugurar', 'Analise', 'Ativas_P', 'Ativas_S', 'Ativas_E', 'Clientes', 'Cli/Pop', 'Fat/Cli',  'Funcionarios', 'Func/Cli', 'Chamados', 'lat', 'lon']]

# Sort value based on Active cases and then Confirmed cases
WorldwildTable = WorldwildTable.sort_values(
    by=['Country/Region'], ascending=True).reset_index(drop=True)
# Set row ids pass to selected_row_ids
WorldwildTable['id'] = WorldwildTable['Country/Region']
WorldwildTable.set_index('id', inplace=True, drop=False)

# Create tables for tabs
BrazilTable = make_country_table('Brazil')
ChileTable = make_country_table('Chile')
GermanyTable = make_country_table('Germany')
SpainTable = make_country_table('Spain')

# Save numbers into variables to use in the app
latestDate = datetime.strftime(df_confirmed['Date'][0], '%b %d, %Y %H:%M GMT+10')
secondLastDate = datetime.strftime(df_confirmed['Date'][1], '%b %d')
daysOutbreak = (df_confirmed['Date'][0] - datetime.strptime('12/31/2019', '%m/%d/%Y')).days
actualDate = datetime.today().strftime('%Y-%m-%d')  #Alterar depois para a data do ultimo arquivo consolidado

# Read confirmed growth data from ./lineplot_data folder
dfs_curve = pd.read_csv('./lineplot_data/dfs_curve.csv')
# Read death growth data from ./lineplot_data folder
dfs_curve_death = pd.read_csv('./lineplot_data/dfs_curve_death.csv')

# Pseduo data for logplot
pseduoDay = np.arange(1, daysOutbreak+1)
y1 = 100*(1.85)**(pseduoDay-1)  # 85% growth rate
y2 = 100*(1.35)**(pseduoDay-1)  # 35% growth rate
y3 = 100*(1.15)**(pseduoDay-1)  # 15% growth rate
y4 = 100*(1.05)**(pseduoDay-1)  # 5% growth rate
# Pseduo data for deathplot
z1 = 3*(1.85)**(pseduoDay-1)  # 85% growth rate
z2 = 3*(1.35)**(pseduoDay-1)  # 35% growth rate
z3 = 3*(1.15)**(pseduoDay-1)  # 15% growth rate
z4 = 3*(1.05)**(pseduoDay-1)  # 5% growth rate

# Generate data for Sunburst plot
df_sunburst = df_latest

# Require n/a as None type 
df_sunburst = df_sunburst.where(pd.notnull(df_sunburst), None)

# Data for ternary chart
df_ternary = WorldwildTable.drop(WorldwildTable[WorldwildTable['Country/Region'] == 'Artania Cruise'].index, axis=0)

# generate option list for ternary chart dropdown
optionList = []
for i in WorldwildTable['Country/Region']:
    optionList.append({'label':i, 'value':i})
optionList = sorted(optionList, key = lambda i: i['value'])
# Add 'All' at the beginning of the list
optionList = [{'label':'All', 'value':'All'}] + optionList



#############################################################################################
# Start to make plots
#############################################################################################

# Line plot for death rate cases
# Set up tick scale based on death case number of Mainland China
#tickList = np.arange(0, (df_recovered['Total']/df_confirmed['Total']*100).max()+0.5, 0.5)

# Create empty figure canvas
fig_rate = go.Figure()
# Add trace to the figure
fig_rate.add_trace(go.Scatter(x=df_deaths['Date'], y=df_deaths['Total']/df_confirmed['Total']*100,
                                mode='lines+markers',
                                line_shape='spline',
                                name='Lost Rate',
                                line=dict(color='#7f7f7f', width=2),
                                marker=dict(size=2, color='#7f7f7f',
                                            line=dict(width=.5, color='#7f7f7f')),
                                text=[datetime.strftime(
                                    d, '%b %d %Y GMT+10') for d in df_deaths['Date']],
                                hovertext=['Global lost rate<br>{:.2f}%'.format(
                                    i) for i in df_deaths['Total']/df_confirmed['Total']*100],
                                hovertemplate='%{hovertext}' +
                                              '<extra></extra>'))
fig_rate.add_trace(go.Scatter(x=df_recovered['Date'], y=df_recovered['Total']/df_confirmed['Total']*100,
                                mode='lines+markers',
                                line_shape='spline',
                                name='Recovery Rate',
                                line=dict(color='#2ecc77', width=2),
                                marker=dict(size=2, color='#2ecc77',
                                            line=dict(width=.5, color='#2ecc77')),
                                text=[datetime.strftime(
                                    d, '%b %d %Y GMT+10') for d in df_recovered['Date']],
                                hovertext=['Global recovery rate<br>{:.2f}%'.format(
                                    i) for i in df_recovered['Total']/df_confirmed['Total']*100],
                                hovertemplate='%{hovertext}' +
                                              '<extra></extra>'))
# Customise layout
fig_rate.update_layout(
    margin=go.layout.Margin(
        l=10,
        r=10,
        b=10,
        t=5,
        pad=0
    ),
    yaxis=dict(
        showline=False, linecolor='#272e3e',
        zeroline=False,
        # showgrid=False,
        gridcolor='rgba(203, 210, 211,.3)',
        gridwidth=.1,
        tickmode='array',
        # Set tick range based on the maximum number
        #tickvals=tickList,
        # Set tick label accordingly
        #ticktext=['{:.1f}'.format(i) for i in tickList]
    ),
#    yaxis_title="Total Confirmed Case Number",
    xaxis=dict(
        showline=False, linecolor='#272e3e',
        showgrid=False,
        gridcolor='rgba(203, 210, 211,.3)',
        gridwidth=.1,
        zeroline=False
    ),
    xaxis_tickformat='%b %d',
    hovermode='x unified',
    showlegend=True,
    legend_orientation="h",
    legend=dict(x=.36, y=-0.1,),
    plot_bgcolor='#ffffff',
    paper_bgcolor='#ffffff',
    font=dict(color='#292929', size=10)
)

# Create empty figure canvas
fig_cumulative_tab = go.Figure()
# Customise layout
fig_cumulative_tab.update_layout(
        margin=go.layout.Margin(
            l=10,
            r=10,
            b=10,
            t=5,
            pad=0
        ),
        yaxis_title="Cumulative cases numbers",
        yaxis=dict(
            showline=False, linecolor='#272e3e',
            zeroline=False,
            # showgrid=False,
            gridcolor='rgba(203, 210, 211,.3)',
            gridwidth=.1,
            tickmode='array',
        ),
        xaxis_title="Select a location from the table (Toggle the legend to see specific curve)",
        xaxis=dict(
            showline=False, linecolor='#272e3e',
            showgrid=False,
            gridcolor='rgba(203, 210, 211,.3)',
            gridwidth=.1,
            zeroline=False
        ),
        xaxis_tickformat='%b %d',
        # transition = {'duration':500},
        hovermode='x unified',
        legend_orientation="h",
        legend=dict(x=.02, y=.95, bgcolor="rgba(0,0,0,0)",),
        plot_bgcolor='#ffffff',
        paper_bgcolor='#ffffff',
        font=dict(color='#292929', size=10)
    )

# Create empty figure canvas
fig_daily_tab = go.Figure()
# Customise layout
fig_daily_tab.update_layout(
        margin=go.layout.Margin(
            l=10,
            r=10,
            b=10,
            t=5,
            pad=0
        ),
        yaxis_title="Daily cases numbers",
        yaxis=dict(
            showline=False, linecolor='#272e3e',
            zeroline=False,
            # showgrid=False,
            gridcolor='rgba(203, 210, 211,.3)',
            gridwidth=.1,
            tickmode='array',
        ),
        xaxis_title="Select a location from the table (Toggle the legend to see specific curve)",
        xaxis=dict(
            showline=False, linecolor='#272e3e',
            showgrid=False,
            gridcolor='rgba(203, 210, 211,.3)',
            gridwidth=.1,
            zeroline=False
        ),
        xaxis_tickformat='%b %d',
        # transition = {'duration':500},
        hovermode='x unified',
        legend_orientation="h",
        legend=dict(x=.02, y=.95, bgcolor="rgba(0,0,0,0)",),
        plot_bgcolor='#ffffff',
        paper_bgcolor='#ffffff',
        font=dict(color='#292929', size=10)
    )


# Default log curve plot for confirmed cases
# Create empty figure canvas
fig_curve_tab = go.Figure()

fig_curve_tab.add_trace(go.Scatter(x=pseduoDay,
                                   y=y1,
                                   line=dict(color='rgba(0, 0, 0, .3)', width=1, dash='dot'),
                                   text=['85% growth rate' for i in pseduoDay],
                                   hovertemplate='<b>%{text}</b><br>' +
                                                 'Doubles every 1.1 days<br>' +
                                                 '<extra></extra>'
                            )
)
fig_curve_tab.add_trace(go.Scatter(x=pseduoDay,
                                   y=y2,
                                   line=dict(color='rgba(0, 0, 0, .3)', width=1, dash='dot'),
                                   text=['35% growth rate' for i in pseduoDay],
                                   hovertemplate='<b>%{text}</b><br>' +
                                                 'Doubles every 2.3 days<br>' +
                                                 '<extra></extra>'
                            )
)
fig_curve_tab.add_trace(go.Scatter(x=pseduoDay,
                                   y=y3,
                                   line=dict(color='rgba(0, 0, 0, .3)', width=1, dash='dot'),
                                   text=['15% growth rate' for i in pseduoDay],
                                   hovertemplate='<b>%{text}</b><br>' +
                                                 'Doubles every 5 days<br>' +
                                                 '<extra></extra>'
                            )
)
fig_curve_tab.add_trace(go.Scatter(x=pseduoDay,
                                   y=y4,
                                   line=dict(color='rgba(0, 0, 0, .3)', width=1, dash='dot'),
                                   text=['5% growth rate' for i in pseduoDay],
                                   hovertemplate='<b>%{text}</b><br>' +
                                                 'Doubles every 14.2 days<br>' +
                                                 '<extra></extra>'
                            )
)
for regionName in ['Worldwide', 'Brazil', 'Chile', 'Germany', 'Spain']:

  dotgrayx_tab = [np.array(dfs_curve.loc[dfs_curve['Region'] == regionName, 'DayElapsed'])[0]]
  dotgrayy_tab = [np.array(dfs_curve.loc[dfs_curve['Region'] == regionName, 'Confirmed'])[0]]

  fig_curve_tab.add_trace(go.Scatter(x=dfs_curve.loc[dfs_curve['Region'] == regionName]['DayElapsed'],
                                     y=dfs_curve.loc[dfs_curve['Region'] == regionName]['Confirmed'],
                                     mode='lines',
                                     line_shape='spline',
                                     name=regionName,
                                     opacity=0.3,
                                     line=dict(color='#636363', width=1.5),
                                     text=[
                                            i for i in dfs_curve.loc[dfs_curve['Region'] == regionName]['Region']],
                                     hovertemplate='<b>%{text}</b><br>' +
                                                   '%{y:,d}<br>'
                                                   '<br>after %{x} clients<br>'
                                                   '<extra></extra>'
                             )
  )

  fig_curve_tab.add_trace(go.Scatter(x=dotgrayx_tab,
                                     y=dotgrayy_tab,
                                     mode='markers',
                                     marker=dict(size=6, color='#636363',
                                     line=dict(width=1, color='#636363')),
                                     opacity=0.5,
                                     text=[regionName],
                                     hovertemplate='<b>%{text}</b><br>' +
                                                   '%{y:,d}<br>'
                                                   '<br>after %{x} clients<br>'
                                                   '<extra></extra>'
                            )
  )

# Customise layout
fig_curve_tab.update_xaxes(range=[0, daysOutbreak-19])
fig_curve_tab.update_yaxes(range=[1.9, 7.5])
fig_curve_tab.update_layout(
        #xaxis_title="Number of day since 3rd death case",
        #yaxis_title="Confirmed cases (Logarithmic)",
        xaxis_title="Number of clients",
        yaxis_title="Faturamento (Logarithmic)",
        margin=go.layout.Margin(
            l=10,
            r=10,
            b=10,
            t=5,
            pad=0
            ),
        yaxis_type="log",
        yaxis=dict(
            showline=False, 
            linecolor='#272e3e',
            zeroline=False,
            # showgrid=False,
            gridcolor='rgba(203, 210, 211,.3)',
            gridwidth = .1,
        ),
        xaxis=dict(
            showline=False, 
            linecolor='#272e3e',
            # showgrid=False,
            gridcolor='rgba(203, 210, 211,.3)',
            gridwidth = .1,
            zeroline=False
        ),
        showlegend=False,
        # hovermode = 'x unified',
        plot_bgcolor='#ffffff',
        paper_bgcolor='#ffffff',
        font=dict(color='#292929', size=10)
    )

# Default curve plot for death toll curve
# Create empty figure canvas
fig_death_curve_tab = go.Figure()

fig_death_curve_tab.add_trace(go.Scatter(x=pseduoDay,
                                   y=z1,
                                   line=dict(color='rgba(0, 0, 0, .3)', width=1, dash='dot'),
                                   text=['85% growth rate' for i in pseduoDay],
                                   hovertemplate='<b>%{text}</b><br>' +
                                                 'Doubles every 1.1 days<br>' +
                                                 '<extra></extra>'
                            )
)
fig_death_curve_tab.add_trace(go.Scatter(x=pseduoDay,
                                   y=z2,
                                   line=dict(color='rgba(0, 0, 0, .3)', width=1, dash='dot'),
                                   text=['35% growth rate' for i in pseduoDay],
                                   hovertemplate='<b>%{text}</b><br>' +
                                                 'Doubles every 2.3 days<br>' +
                                                 '<extra></extra>'
                            )
)
fig_death_curve_tab.add_trace(go.Scatter(x=pseduoDay,
                                   y=z3,
                                   line=dict(color='rgba(0, 0, 0, .3)', width=1, dash='dot'),
                                   text=['15% growth rate' for i in pseduoDay],
                                   hovertemplate='<b>%{text}</b><br>' +
                                                 'Doubles every 5 days<br>' +
                                                 '<extra></extra>'
                            )
)
fig_death_curve_tab.add_trace(go.Scatter(x=pseduoDay,
                                   y=z4,
                                   line=dict(color='rgba(0, 0, 0, .3)', width=1, dash='dot'),
                                   text=['5% growth rate' for i in pseduoDay],
                                   hovertemplate='<b>%{text}</b><br>' +
                                                 'Doubles every 14.2 days<br>' +
                                                 '<extra></extra>'
                            )
)

for regionName in ['Worldwide', 'Brazil', 'Chile', 'Germany', 'Spain']:

  dotgrayx_tab_death = [np.array(dfs_curve_death.loc[dfs_curve_death['Region'] == regionName, 'DayElapsed_death'])[0]]
  dotgrayy_tab_death = [np.array(dfs_curve_death.loc[dfs_curve_death['Region'] == regionName, 'Deaths'])[0]]

  fig_death_curve_tab.add_trace(go.Scatter(x=dfs_curve_death.loc[dfs_curve_death['Region'] == regionName]['DayElapsed_death'],
                                     y=dfs_curve_death.loc[dfs_curve_death['Region'] == regionName]['Deaths'],
                                     mode='lines',
                                     line_shape='spline',
                                     name=regionName,
                                     opacity=0.3,
                                     line=dict(color='#636363', width=1.5),
                                     text=[
                                            i for i in dfs_curve_death.loc[dfs_curve_death['Region'] == regionName]['Region']],
                                     hovertemplate='<b>%{text}</b><br>' +
                                                   '%{y:,d}<br>'
                                                   '<br>after %{x} clients<br>'
                                                   '<extra></extra>'
                             )
  )

  fig_death_curve_tab.add_trace(go.Scatter(x=dotgrayx_tab_death,
                                     y=dotgrayy_tab_death,
                                     mode='markers',
                                     marker=dict(size=6, color='#636363',
                                     line=dict(width=1, color='#636363')),
                                     opacity=0.5,
                                     text=[regionName],
                                     hovertemplate='<b>%{text}</b><br>' +
                                                   '%{y:,d}<br>'
                                                   '<br>after %{x} clients<br>'
                                                   '<extra></extra>'
                            )
  )

# Customise layout
fig_death_curve_tab.update_xaxes(range=[0, daysOutbreak-19])
fig_death_curve_tab.update_yaxes(range=[0.477, 5.8])
fig_death_curve_tab.update_layout(
        xaxis_title="Number of clients",
        yaxis_title="Lost cases (Logarithmic)",
        margin=go.layout.Margin(
            l=10,
            r=10,
            b=10,
            t=5,
            pad=0
            ),
        yaxis=dict(
            showline=False, 
            linecolor='#272e3e',
            zeroline=False,
            # showgrid=False,
            gridcolor='rgba(203, 210, 211,.3)',
            gridwidth = .1,
        ),
        yaxis_type="log",
        xaxis=dict(
            showline=False, 
            linecolor='#272e3e',
            # showgrid=False,
            gridcolor='rgba(203, 210, 211,.3)',
            gridwidth = .1,
            zeroline=False
        ),
        showlegend=False,
        # hovermode = 'x unified',
        plot_bgcolor='#ffffff',
        paper_bgcolor='#ffffff',
        font=dict(color='#292929', size=10)
    )



##################################################################################################
# Start dash app
##################################################################################################
BS = "https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/css/bootstrap.min.css"

aa = (format_currency(fatur_p, 'R$', locale='pt_BR.utf8')).split(",", 1)[0]

app = dash.Dash(__name__,
                assets_folder='./assets/',
                external_stylesheets=[BS],
      )

app.title = 'BI/AI Global Monitor'

image_filename = './logotop.png' # replace with your own image
encoded_image = base64.b64encode(open(image_filename, 'rb').read())


server = app.server

app.config['suppress_callback_exceptions'] = True # This is to prevent app crash when loading since we have plot that only render when user clicks.

app.layout = html.Div(
    id='app-body',
    children=[
        #html.Div([
        #    # Company Logo here!
	#    html.Img(
        #    src='data:image/png;base64,{}'.format(encoded_image.decode()),
        #    style={
        #        'height': '7%',
        #        'width': '7%'
        #     })
  	#], style={'textAlign': 'left'}),
        html.Div(
            id="header",
            children=[
                html.H1(
                    id='header-title',
		    style={
			"fontSize":"5.2em", 'textAlign':'center', 'padding':'20px', 'color':'#003434',
			"box-shadow": 
				'inset 0 0 0 1px rgba(53,86,129, 0.4)', 
			"border-radius": '0 10px 0 10px',
			#"background": '#fff url(../assets/image-3.jpeg) no-repeat center left'},
			"background": 'url(../assets/image-3.jpeg) center left, url(../assets/flipimage.jpg) center right',
			"background-repeat": 'no-repeat'},
                    children="BI/AI Global Monitor"),
#                html.P(
#                    id="description",
#                    children=dcc.Markdown(
#                        children=(
#                            '''
#	The term Business Intelligence (BI) refers to technologies, 
#	applications and practices for the collection, integration, analysis, and presentation of 
#	business information to support better business decision making.
#
#	Artificial Intelligence (AI) learning process focuses on acquiring data and creating rules, 
#	which are called algorithms, for how to turn the data into actionable information. 
#
#	This dashboard is developed to visualise and track the recent reported 
#	information about the company.'''.format(latestDate, faturamento),
#                        )
#                    )
#                ),
                html.P(
                    className='time-stamp',
                    #children="Last update: {}. (Hover over items for additional information)".format(latestDate)
                    children="Last update: {}. (Hover over items for additional information)".format(actualDate)
                ),
                html.Hr(
                ),
            ], style={'textAlign': 'center'}
        ), 
        html.Div(
            className="number-plate",
            children=[
                html.Div(
                    className='number-plate-single',
                    style={'border-top': '#292929 solid .2rem',},
                    children=[
                        html.H5(
                            style={'color': '#292929',},
                            children="Total de unidades"
                        ),
                        html.H3(
                            style={'color': '#292929'},
                            children=[
                                '{}'.format(unidAtivas+unidInaug+unidAnalise),
                                html.P(
                                    style={'color': '#ffffff',},
                                #    children='xxxx xx xxx xxxx xxx xxxxx'
                                ), 
                            ]
                        ),
                        html.H3(
			    style={'border-bottom': '#292929 solid .2rem',},
                            children=[
                                html.P(
                                    children='Premium'
                                ),
                                
                            ]
                        ),
                        html.H3(
			    style={'border-bottom': '#292929 solid .2rem',},
                            children=[
                                html.P(
                                    children='Smart'
                                ),
                                
                            ]
                        ),
                        html.H3(
			    style={'border-bottom': '#292929 solid .2rem',},
                            children=[
                                html.P(
                                    children='Express'
                                ),
                                
                            ]
                        ),
                    ]
		    
                ),
                html.Div(
                    className='number-plate-single',
                    id='number-plate-fatur',
                    style={'border-top': '#f03f42 solid .2rem',},
                    children=[
                        html.H5(
                            style={'color': '#f03f42'},
                            children="Faturamento"
                        ),
                        html.H3(
                            style={'color': '#f03f42'},
                            children=[
                                '{:s}'.format((format_currency(faturamento, 'R$', locale='pt_BR.utf8')).split(",", 1)[0], faturamento),
                                html.P(
                                    #children='+ {:,d} in the past 24h ({:.1%})'.format(plusConfirmedNum, plusPercentNum1)
                                    #children='$ {:,d} ({:.1%})'.format(fatur_p, (fatur_p/faturamento))
                                ),
                                
                            ]
                        ),
                        html.H3(
			    style={'border-bottom': '#f03f42 solid .2rem',},
                            children=[
                                html.P(
                                    style={'color': '#f03f42'},
                                    children='{:s} ({:.1%})'.format((format_currency(fatur_p, 'R$', locale='pt_BR.utf8')).split(",", 1)[0], (fatur_p/faturamento))
                                ),
                                
                            ]
                        ),
                        html.H3(
			    style={'border-bottom': '#f03f42 solid .2rem',},
                            children=[
                                html.P(
                                    style={'color': '#f03f42'},
                                    children='{:s} ({:.1%})'.format((format_currency(fatur_s, 'R$', locale='pt_BR.utf8')).split(",", 1)[0], (fatur_s/faturamento))
                                ),
                                
                            ]
                        ),
                        html.H3(
			    style={'border-bottom': '#f03f42 solid .2rem',},
                            children=[
                                html.P(
                                    style={'color': '#f03f42'},
                                    children='{:s} ({:.1%})'.format((format_currency(fatur_e, 'R$', locale='pt_BR.utf8')).split(",", 1)[0], (fatur_e/faturamento))
                                ),
                                
                            ]
                        ),
                        
                    ]
                ),
                html.Div(
                    className='number-plate-single',
                    id='number-plate-ativas',
                    style={'border-top': '#7f7f7f solid .2rem',},
                    children=[
                        html.H5(
                            style={'color': '#7f7f7f'},
                            children="Ativas"
                        ),
                        html.H3(
                        	style={'color': '#7f7f7f'},
                            children=[
                                '{:,d}'.format(unidAtivas),
                                html.P(
                                    #children='+ {:,d} ({:.1%})'.format(unidPremium, unidPremium/unidAtivas)
                                ),
                                
                            ]
                        ),
                        html.H3(
			    style={'border-bottom': '#7f7f7f solid .2rem',},
                            children=[
                                html.P(
                                    #children='Premium'
                        	    style={'color': '#7f7f7f'},
                                    children='{:,d} ({:.1%})'.format(unidAtivas_p, unidAtivas_p/unidAtivas)
                                ),
                                
                            ]
                        ),
                        html.H3(
			    style={'border-bottom': '#7f7f7f solid .2rem',},
                            children=[
                                html.P(
                                    #children='Smart'
                        	    style={'color': '#7f7f7f'},
                                    children='{:,d} ({:.1%})'.format(unidAtivas_s, unidAtivas_s/unidAtivas)
                                ),
                                
                            ]
                        ),
                        html.H3(
			    style={'border-bottom': '#7f7f7f solid .2rem',},
                            children=[
                                html.P(
                                    #children='Express'
                        	    style={'color': '#7f7f7f'},
                                    children='{:,d} ({:.1%})'.format(unidAtivas_e, unidAtivas_e/unidAtivas)
                                ),
                                
                            ]
                        ),
                        
                    ]
                ),
                html.Div(
                    className='number-plate-single',
                    id='number-plate-inaug',
                    style={'border-top': '#2ecc77 solid .2rem',},
                    children=[
                        html.H5(
                            style={'color': '#2ecc77'},
                            children="A inaugurar"
                        ),
                        html.H3(
                            style={'color': '#2ecc77'},
                            children=[
                                '{:,d}'.format(unidInaug),
                                html.P(
                                    #children='+ {:,d} in the past 24h ({:.1%})'.format(plusRecoveredNum, plusPercentNum2)
                                ),
                                
                            ]
                        ),
                        html.H3(
			    style={'border-bottom': '#2ecc77 solid .2rem',},
                            children=[
                                html.P(
                                    #children='Premium'
                                    style={'color': '#2ecc77'},
                                    children='{:,d} ({:.1%})'.format(unidInaug_p, unidInaug_p/unidInaug)
                                ),
                                
                            ]
                        ),
                        html.H3(
			    style={'border-bottom': '#2ecc77 solid .2rem',},
                            children=[
                                html.P(
                                    #children='Smart'
                                    style={'color': '#2ecc77'},
                                    children='{:,d} ({:.1%})'.format(unidInaug_s, unidInaug_s/unidInaug)
                                ),
                                
                            ]
                        ),
                        html.H3(
			    style={'border-bottom': '#2ecc77 solid .2rem',},
                            children=[
                                html.P(
                                    #children='Express'
                                    style={'color': '#2ecc77'},
                                    children='{:,d} ({:.1%})'.format(unidInaug_e, unidInaug_e/unidInaug)
                                ),
                                
                            ]
                        ),
                        
                    ]
                ),
                html.Div(
                    className='number-plate-single',
                    id='number-plate-analise',
                    style={'border-top': '#f0953f solid .2rem',},
                    children=[
                        html.H5(
                            style={'color': '#f0953f'},
                            children="Em Análise"
                        ),
                        html.H3(
                        	style={'color': '#f0953f'},
                            children=[
                                '{:,d}'.format(unidAnalise),
                                html.P(
                                    #children='+ {:,d} in the past 24h ({:.1%})'.format(plusRemainNum, plusRemainNum3) if plusRemainNum > 0 else '{:,d} in the past 24h ({:.1%})'.format(plusRemainNum, plusRemainNum3)
                                ),      
                            ]
                        ),
                        html.H3(
			    style={'border-bottom': '#f0953f solid .2rem',},
                            children=[
                                html.P(
                                    #children='Premium'
                        	    style={'color': '#f0953f'},
                                    children='{:,d} ({:.1%})'.format(unidAnalise_p, unidAnalise_p/unidAnalise) 
                                ),
                                
                            ]
                        ),
                        html.H3(
			    style={'border-bottom': '#f0953f solid .2rem',},
                            children=[
                                html.P(
                                    #children='Smart'
                        	    style={'color': '#f0953f'},
                                    children='{:,d} ({:.1%})'.format(unidAnalise_s, unidAnalise_s/unidAnalise) 
                                ),
                                
                            ]
                        ),
                        html.H3(
			    style={'border-bottom': '#f0953f solid .2rem',},
                            children=[
                                html.P(
                                    #children='Express'
                        	    style={'color': '#f0953f'},
                                    children='{:,d} ({:.1%})'.format(unidAnalise_e, unidAnalise_e/unidAnalise) 
                                ),
                                
                            ]
                        ),
                    ]
                ),
                dbc.Tooltip(
                    target='number-plate-analise',
                    style={"fontSize":"1.8em", 'textAlign':'right', 'padding':'10px',},
                    children=
                        dcc.Markdown(
                            '''
                            Mês anterior: **{:.0f}**

                            Há 2 meses: **{:.0f}** 

			    '''.format(unidAnalise - (unidAnalise * 0.10), unidAnalise - (unidAnalise * 0.20)), 
                        ) 
                ),
                dbc.Tooltip(
                    target='number-plate-fatur',
                    style={"fontSize":"1.8em", 'textAlign':'right', 'padding':'10px',},
                    children=
                        dcc.Markdown(
                            '''
                            Mês anterior: **${:.0f}**
			
                            Há 2 meses: **${:.0f}** 
		
			    '''.format(faturamento - (faturamento * 0.10), faturamento - (faturamento * 0.20)),	    
                        ) 
                ),
                dbc.Tooltip(
                    target='number-plate-inaug',
                    style={"fontSize":"1.8em", 'textAlign':'right', 'padding':'10px',},
                    children=
                        dcc.Markdown(
                            '''
                            Mês anterior: **{:.0f}**

                            Há 2 meses: **{:.0f}** 

			    '''.format(unidInaug - (unidInaug * 0.10), unidInaug - (unidInaug * 0.20)),
                        ) 
                ),
                dbc.Tooltip(
                    target='number-plate-ativas',
                    style={"fontSize":"1.8em", 'textAlign':'right', 'padding':'10px',},
                    children=
                        dcc.Markdown(
                            '''
                            Mês anterior: **{:.0f}**

                            Há 2 meses: **{:.0f}** 

			    '''.format(unidAtivas - (unidAtivas * 0.10), unidAtivas - (unidAtivas * 0.20)),
                        ) 
                ),
            ]
        ),
        html.Div(
            className='section-line',
            children=[
                html.Hr(
                ),
            ]
        ),
        html.Div(
            className='row dcc-plot',
            children=[
                html.Div(
                	className='dcc-sub-plot',
                    children=[
                        html.Div(
                            id='case-timeline-log-button',
                            children=[
                                html.H5(
                                    children='Attendance Timeline | Worldwide'
                                ),
                                daq.PowerButton(
                                    id='log-button',
                                    size=22,
                                    color="#2674f6",
                                    on=False,
                                ),
                                dbc.Tooltip(
                                	"Switch between linear and logarithmic y-axis",
                                    target='log-button',
                                    style={"fontSize":"1.8em"},
                                ),
                            ],
                        ),
                        dcc.Graph(
                            id='combined-line-plot',
                            config={"displayModeBar": False, "scrollZoom": False}, 
                        ),
                    ]
                ),
                html.Div(
                	className='dcc-sub-plot',
                    children=[                                  
                        html.H5(
                            id='dcc-death-graph-head',
                            children='Recovery/Lost Rate (%) Timeline | Worldwide'
                        ),
                        dcc.Graph(
                            style={'height': '301px'}, 
                            figure=fig_rate,
                            config={"displayModeBar": False, "scrollZoom": False},
                        ),
                        dbc.Tooltip(
                            target='dcc-death-graph-head',
                            style={"fontSize":"1.8em", 'textAlign':'left', 'padding':'10px','width':'auto', 'maxWidth':'450px'},
                            children=[
                                dcc.Markdown(
                                    '''
                                    Lost rate is calculated using the formula: 
                            
                                    **Lost rate = (Lost/Confirmed attendances) x 100%**
                                    
                                    Note that this is only a conservative estimation. The real death rate can only be 
                                    revealed as all cases are resolved. 
                                    ''',
                                )
                            ] 
                        ),
                    ]
                ),
            ]
        ),
        html.Div(
            className='row dcc-plot',
            children=[
                html.Div(
                	className='dcc-sub-plot',
                    children=[
                        html.H5(
                            children='Units Location Map'
                        ),
                        dcc.Graph(
                            id='datatable-interact-map',
                            style={'height': '400px'},
                            config={"displayModeBar": False, "scrollZoom": True},
                        ),
                    ]
                ),
                html.Div(
                	className='dcc-sub-plot',
                    children=[
                        html.H5(
                            children='Summary Graph'
                        ),
                        dcc.Dropdown(
                            id="dcc-dropdown",
                            placeholder="Select a graph type",
                            value='Daily Attendance',
                            options=[
                                {'label':'Cumulative Attendance', 'value':'Cumulative Attendance'},
                                {'label':'Daily Attendance', 'value':'Daily Attendance'},
                                {'label':'Attendance Trajectories', 'value':'Attendance Trajectories'},
                                {'label':'Lost Attendance Trajectories', 'value':'Lost Attendance Trajectories'},
                            ]
                        ),                                  
                        html.Div(
                        	id='tabs-content-plots',
                        ),
                    ]
                ),
            ]
        ),
        html.Div(
            className='dcc-table',
            children=[
                html.H5(
                    id='dcc-table-header',
                    children='Units Summary by Location'
                ),
                dcc.Tabs(
                    id="tabs-table",
                    value='Worldwide',
                    parent_className='custom-tabs',
                    className='custom-tabs-container',
                    children=[
                        dcc.Tab(
                       	    label='Worldwide',
                            value='Worldwide',
                            className='custom-tab',
                            selected_className='custom-tab--selected',
                            children=[
                                dash_table.DataTable(
                                    id='datatable-interact-location',
                                    # Don't show coordinates
                                    columns=[{"name": 'Country/Region', "id": 'Country/Region'}] +
                                            [{"name": i, "id": i, "type": "numeric","format": FormatTemplate.percentage(2)}
                                                if i == 'Cli/Pop' or i == 'Func/Cli' else 
 						   {"name": i, "id": i, "type": "numeric","format": FormatTemplate.money(0)}
							if i == 'Fat/Cli' else
						   	   {"name": i, "id": i, 'type': 'numeric', 'format': Format(group=',')}
                                                    for i in WorldwildTable.columns[1:11]],
                                    # But still store coordinates in the table for interactivity
                                    data=WorldwildTable.to_dict("rows"),
                                    #css= [{'selector': 'tr:hover', 'rule': 'background-color: #2674f6;'}],
                                    row_selectable="single",
                                    sort_action="native",
                                    style_as_list_view=True,
                                    style_cell={
                                        'fontFamily': 'Roboto',
                                        'backgroundColor': '#ffffff', 
                                    },
                                    fixed_rows={
                                        'headers': True, 'data': 0},
                                    style_table={
                                        'minHeight': '400px',
                                        'height': '400px',
                                        'maxHeight': '400px',
                                        'overflowX': 'auto',
                                    },
                                    style_header={
                                        'backgroundColor': '#ffffff',
                                        'fontWeight': 'bold'
                                    },
                                    style_cell_conditional=[
                                        {'if': {'column_id': 'Country/Region'}, 'width': '17%'},
                                        {'if': {'column_id': 'Faturamento'}, 'width': '8%'},
                                        {'if': {'column_id': 'Ativas'}, 'width': '8%'},
                                        {'if': {'column_id': 'Inaugurar'}, 'width': '8%'},
                                        {'if': {'column_id': 'Analise'}, 'width': '8%'},
                                        {'if': {'column_id': 'Clientes'}, 'width': '8%'},
                                        {'if': {'column_id': 'Cli/Pop'}, 'width': '8%'},
                                        {'if': {'column_id': 'Fat/Cli'}, 'width': '8%'},
                                        {'if': {'column_id': 'Funcionarios'}, 'width': '9%'},
                                        {'if': {'column_id': 'Func/Cli'}, 'width': '9%'},    
                                        {'if': {'column_id': 'Chamados'}, 'width': '9%'},
                                        {'if': {'column_id': 'Analise'}, 'color':'#f0953f'},
                                        {'if': {'column_id': 'Faturamento'}, 'color': '#f03f42'},
                                        {'if': {'column_id': 'Inaugurar'}, 'color': '#2ecc77'},
                                        {'if': {'column_id': 'Ativas'}, 'color': '#7f7f7f'},
                                        {'textAlign': 'center'}
                                    ],
                                )
                            ]
                        ),
			# Paises que compoem a header tab
                        make_dcc_country_tab(
                            'Brazil', BrazilTable),
                        make_dcc_country_tab(
                            'Chile', ChileTable),
                        make_dcc_country_tab(
                            'Germany', GermanyTable),
                        make_dcc_country_tab(
                            'Spain', SpainTable),
                    ]
                ),
            ]
        ),
        html.Div(
            className='dcc-plot',
            id='sunburst-chart',
            children=[
                html.Div(
                    className='dcc-sub-plot sunburst-ternary-plot',
                    children=[
                        html.Div(
                            className='header-container',                            
                            children=[
                                html.H5(
                                    children='Sunburst Chart | Worldwide'
                                ),
                            ]
                        ),
                        dcc.Dropdown(
                        	id="sunburst-dropdown",
                            placeholder="Select a metric",
                            value='fatur',
                            searchable=False,
                            clearable=False,
                            options=[{'label':'Clientes', 'value':'clientes'},
                                     {'label':'Faturamento', 'value':'fatur'},
                                     {'label':'Ativas', 'value':'A'},
                                     {'label':'Funcionários', 'value':'funcion'},
                            ]
                        ),                                  
                        dcc.Graph(
                        	id='dropdown-sunburst-plots',
                            style={'height': '500px'},
                            config={"displayModeBar": False, "scrollZoom": False},
                        ),
                    ]
                ),
                html.Div(
                    className='dcc-sub-plot sunburst-ternary-plot',
                    children=[
                        html.Div(
                            className='header-container',
                            id='ternary-plot',
                            children=[
                                html.H5(
                                    children='Ternary Chart | Worldwide'
                                ),
                            ]
                        ),
                        dcc.Dropdown(
                        	id="ternary-dropdown",
                            placeholder="Select or search a location name",
                            value='All',
                            options=optionList,
                        ),                 
                        dcc.Graph(
                            id='ternary-dropdown-chart',
                            style={'height': '500px'},
                            config={"displayModeBar": False, "scrollZoom": False}, 
                        ),
                    ]
                ),
                dbc.Tooltip(
                    target='ternary-plot',
                    style={"fontSize":"1.8em", 'textAlign':'left', 'padding':'10px'},
                    children=
                        dcc.Markdown(
                            children=(
                                '''
                                The ternary diagram displays the proportion of **premium**, **smart** and **express** units.
			    
                                Point size represents population. 
			    
                                '''
                            )
                        )
                ),
            ]
        ),
        html.Div(
            className='footer-container',
            id='my-footer',
            children=[
                html.P(
                    #'Together we stop the spread',
                    'Bringing wisdom to Business Intelligence',
                ),
                html.P(
                    ' | ',
                ),
                html.P(
                    children=[
                        html.A(
                            'Adapted by Wander' 
                        ),
                    ],
                ),
                html.P(
                    ' | ',
                ),
                html.Div(
                    id='contributor-button',
                    children=[
                        dbc.Button(
                            "Contributors", 
                            id="open-contributor", 
                            className="button", 
                        ),
                    ]
                ),
                html.P(
                    ' | ',
                ),
                html.P(
                    children=[
                        html.A(
                            'About this dashboard', 
                            #href='https://github.com/Perishleaf/data-visualisation-scripts/tree/master/dash-2019-coronavirus',
                            #target='_blank'
                        ),
                    ],
                ),
                html.P(
                    ' | ',
                ),           
                html.P(
                    children=[
                        html.A(
                            'Report a bug', 
                            #href='https://twitter.com/perishleaf', 
                            #target='_blank'
                        ),
                    ],
                ),                
                html.P(
                    ' | ',
                ),
                html.Div(
                    id='disclaimer-button',
                    children=[
                        dbc.Button(
                        	"Disclaimer", 
                        	id="open", 
                        	#color="info", 
                        	className="button", 
                        ),
                        dbc.Modal(
                        	id='modal',
                            children=[
                                dbc.ModalHeader("Disclaimer"),
                                dbc.ModalBody(
                                    '''
                                    This website and its contents herein, including all data, 
                                    mapping and analysis, is provided exclusivelly to the +TOP head manager 
                                    for general presentation purposes only. All the information was created 
                                    with dummy data. I make no representations or warranties of any kind,
                                    express or implied, about the completeness, accuracy, reliability, with 
                                    respect to the website or the information. I do not bear any legal responsibility 
                                    for any consequence caused by the use of the information provided.  
                                    Use of the website in commerce is strongly not recommended. Any action you take
                                    upon the information on this website is strictly at your own risk and I will not be
                                    liable for any losses and damages in connection with the use of this website.
                                    '''
                                ),
                                dbc.ModalFooter(
                                	children=[
                                	    dbc.Button(
                                		    "Close", 
                                		    id="close", 
                                		    className="ml-auto",
                                            style={'background-color':'#20b6e6', 'font-weight':'bold'}
                                        )
                                    ],            
                                ),
                            ],
                        ),
                    ]
                ),
            ]
        ),
    ]
)

@app.callback(
    Output("modal", "is_open"),
    [Input("open", "n_clicks"), Input("close", "n_clicks")],
    [State("modal", "is_open")],
)
def toggle_modal(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open

@app.callback(
    Output("modal-contributor", "is_open"),
    [Input("open-contributor", "n_clicks"), Input("close-contributor", "n_clicks")],
    [State("modal-contributor", "is_open")],
)
def toggle_modal_contributor(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open


# Summary Graph here!
@app.callback(Output('tabs-content-plots', 'children'),
              [Input('dcc-dropdown', 'value')]
)
def render_content(tab):
    if tab == 'Cumulative Attendance':
        return dcc.Graph(id='datatable-interact-lineplot',
                         style={'height': '364px'},
                         figure=fig_cumulative_tab,
                         config={"displayModeBar": False, "scrollZoom": False},
                )
    elif tab == 'Daily Attendance':
        return dcc.Graph(id='datatable-interact-dailyplot',
                         style={'height': '364px'},
                         figure=fig_daily_tab,
                         config={"displayModeBar": False, "scrollZoom": False},
                )
    elif tab == 'Attendance Trajectories':
        return dcc.Graph(id='datatable-interact-logplot',
                         style={'height': '364px'},
                         figure=fig_curve_tab,
                         config={"displayModeBar": False, "scrollZoom": False},
                )
    elif tab == 'Lost Attendance Trajectories':
        return dcc.Graph(id='datatable-interact-deathplot',
                         style={'height': '364px'},
                         figure=fig_death_curve_tab,
                         config={"displayModeBar": False, "scrollZoom": False},
                )

@app.callback(Output('combined-line-plot', 'figure'),
              [Input('log-button', 'on')])

def render_combined_line_plot(log):
  if log is True:
    axis_type = 'log'
  else:
    axis_type = 'linear'

  # Line plot for combine recovered cases
  # Set up tick scale based on total recovered case number
  #tickList = np.arange(0, df_remaining['Total'].max()+10000, 30000)

  # Create empty figure canvas
  fig_combine = go.Figure()
  # Add trace to the figure
  
  fig_combine.add_trace(go.Scatter(x=df_remaining['Date'], y=df_remaining['Total'],
                                mode='lines+markers',
                                line_shape='spline',
                                name='Recovered',
                                line=dict(color='#f0953f', width=2),
                                marker=dict(size=2, color='#f0953f',
                                            line=dict(width=.5, color='#f0953f')),
                                text=[datetime.strftime(
                                    d, '%b %d %Y GMT+10') for d in df_deaths['Date']],
                                hovertext=['Total recovered<br>{:,d} cases<br>'.format(
                                    i) for i in df_remaining['Total']],
                                hovertemplate='%{hovertext}' +
                                              '<extra></extra>'))
  fig_combine.add_trace(go.Scatter(x=df_confirmed['Date'], y=df_confirmed['Total'],
                                   mode='lines+markers',
                                   line_shape='spline',
                                   name='Calls',
                                   line=dict(color='#f03f42', width=2),
                                   marker=dict(size=2, color='#f03f42',
                                               line=dict(width=.5, color='#f03f42')),
                                   text=[datetime.strftime(
                                       d, '%b %d %Y GMT+10') for d in df_confirmed['Date']],
                                   hovertext=['Total calls<br>{:,d} cases<br>'.format(
                                       i) for i in df_confirmed['Total']],
                                   hovertemplate='%{hovertext}' +
                                                 '<extra></extra>'))
  fig_combine.add_trace(go.Scatter(x=df_recovered['Date'], y=df_recovered['Total'],
                                   mode='lines+markers',
                                   line_shape='spline',
                                   name='Attendances',
                                   line=dict(color='#2ecc77', width=2),
                                   marker=dict(size=2, color='#2ecc77',
                                               line=dict(width=.5, color='#2ecc77')),
                                   text=[datetime.strftime(
                                       d, '%b %d %Y GMT+10') for d in df_recovered['Date']],
                                   hovertext=['Total attendances<br>{:,d} cases<br>'.format(
                                       i) for i in df_recovered['Total']],
                                   hovertemplate='%{hovertext}' +
                                                 '<extra></extra>'))
  fig_combine.add_trace(go.Scatter(x=df_deaths['Date'], y=df_deaths['Total'],
                                mode='lines+markers',
                                line_shape='spline',
                                name='Lost',
                                line=dict(color='#7f7f7f', width=2),
                                marker=dict(size=2, color='#7f7f7f',
                                            line=dict(width=.5, color='#7f7f7f')),
                                text=[datetime.strftime(
                                    d, '%b %d %Y GMT+10') for d in df_deaths['Date']],
                                hovertext=['Total lost<br>{:,d} cases<br>'.format(
                                    i) for i in df_deaths['Total']],
                                hovertemplate='%{hovertext}' +
                                              '<extra></extra>'))
  # Customise layout
  fig_combine.update_layout(
    margin=go.layout.Margin(
        l=10,
        r=10,
        b=10,
        t=5,
        pad=0
    ),
    yaxis_type=axis_type,
    yaxis=dict(
        showline=False, linecolor='#272e3e',
        zeroline=False,
        # showgrid=False,
        gridcolor='rgba(203, 210, 211,.3)',
        gridwidth=.1,
        #tickmode='array',
        # Set tick range based on the maximum number
        #tickvals=tickList,
        # Set tick label accordingly
        #ticktext=["{:.0f}k".format(i/1000) for i in tickList]
    ),
#    yaxis_title="Total Confirmed Case Number",
    xaxis=dict(
        showline=False, linecolor='#272e3e',
        showgrid=False,
        gridcolor='rgba(203, 210, 211,.3)',
        gridwidth=.1,
        zeroline=False
    ),
    xaxis_tickformat='%b %d',
    hovermode='x unified',
    legend_orientation="h",
    legend=dict(x=.26, y=-.1,),
    plot_bgcolor='#ffffff',
    paper_bgcolor='#ffffff',
    font=dict(color='#292929', size=10)
  )
  
  return fig_combine


# Sunburst here!
@app.callback(Output('dropdown-sunburst-plots', 'figure'),
              [Input('sunburst-dropdown', 'value')])

def render_sunburst_plot(metric):
    colorTheme=px.colors.qualitative.Safe

    if metric == 'fatur':
        hovertemplate = '<b>%{label} </b> <br><br>fatur: %{value}'
    elif metric == 'A':
        hovertemplate = '<b>%{label} </b> <br>A: %{value}'
    elif metric == 'funcion':
        hovertemplate = '<b>%{label} </b> <br>funcion: %{value}'
    elif metric == 'clientes':
        hovertemplate = '<b>%{label} </b> <br>clientes: %{value}'

    fig_sunburst = px.sunburst(
        df_sunburst, 
        path=['Country/Region', 'Province/State'], 
        values=metric,
        hover_data=[metric],
        color_discrete_sequence=colorTheme,           
    )

    fig_sunburst.update_traces(
        textinfo='label+percent root',
  	    hovertemplate=hovertemplate
    )
    fig_sunburst.update_layout(
        annotations=[
            dict(
                x=0.5,
                y=-0.2,
                xref='paper',
                yref='paper',
                text='Click to unfold segment',
                showarrow=False,
                font=dict(
                    family='Roboto, sans-serif',
                    size=16,
                    color="#292929"
                ),
            )
        ]
    )

    return fig_sunburst


# Ternary here!
@app.callback(Output('ternary-dropdown-chart', 'figure'),
              [Input('ternary-dropdown', 'value')]
        )

def render_ternary_plot(value):
    # make ternary chart
    if value == 'All':
        fig_ternary = px.scatter_ternary(df_ternary, a="Ativas_P", b="Ativas_S", c="Ativas_E", template='plotly_white', 
            size=[i**(1/3) for i in df_ternary['Ativas_P'] + df_ternary['Ativas_S'] + df_ternary['Ativas_E']],
            color='Faturamento',
            color_continuous_scale=px.colors.sequential.Aggrnyl,
        )
        fig_ternary.update_traces(
            text=df_ternary['Country/Region'],
            hovertemplate="<b>%{text}</b><br><br>" +
                          "Total premium rate: %{a:.2f}<br>" +
                          "Total smart rate: %{b: .2f}<br>" +
                          "Total express rate: %{c: .2f}<br>" +
                          "Faturamento: %{marker.color: .0f}",
            marker=dict(line=dict(width=1, color='White')),               
        )
        fig_ternary.update_layout(
            annotations=[
                dict(
                    x=0.5,
                    y=-0.2,
                    xref='paper',
                    yref='paper',
                    text='Double click the chart to reset view after zoom in',
                    showarrow=False,
                    font=dict(
                        family='Roboto, sans-serif',
                        size=16,
                        color="#292929"
                    ),
                )
            ]
        )
        return fig_ternary 
    else:
        fig_ternary = px.scatter_ternary(df_ternary, a="Ativas_P", b="Ativas_S", c="Ativas_E", template='plotly_white', 
            size=[i**(1/3) for i in df_ternary['Ativas_P'] + df_ternary['Ativas_S'] + df_ternary['Ativas_E']],
            opacity=[1 if i == value else 0.1 for i in WorldwildTable['Country/Region']],
            color='Faturamento',
            color_continuous_scale=px.colors.sequential.Aggrnyl,
        )
        fig_ternary.update_traces(
            text=df_ternary['Country/Region'],
            hovertemplate="<b>%{text}</b><br><br>" +
                          "Total premium rate: %{a:.2f}<br>" +
                          "Total smart rate: %{b: .2f}<br>" +
                          "Total express rate: %{c: .2f}<br>" +
                          "Faturamento: %{marker.color: .0f}",
            marker=dict(line=dict(width=1, color='White')),               
        )
        fig_ternary.update_layout(
            annotations=[
                dict(
                    x=0.5,
                    y=-0.2,
                    xref='paper',
                    yref='paper',
                    text='Double click the chart to reset view after zoom in',
                    showarrow=False,
                    font=dict(
                        family='Roboto, sans-serif',
                        size=16,
                        color="#292929"
                    ),
                )
            ]
        )

        return fig_ternary 

@app.callback(
    Output('datatable-interact-map', 'figure'),
    input_list
)
def update_figures(
    value, 
    Worldwide_derived_virtual_selected_rows, Worldwide_selected_row_ids,
    Brazil_derived_virtual_selected_rows, Brazil_selected_row_ids,
    Chile_derived_virtual_selected_rows, Chile_selected_row_ids,
    Germany_derived_virtual_selected_rows, Germany_selected_row_ids,
    Spain_derived_virtual_selected_rows, Spain_selected_row_ids,
):

    # When the table is first rendered, `derived_virtual_data` and
    # `derived_virtual_selected_rows` will be `None`. This is due to an
    # idiosyncracy in Dash (unsupplied properties are always None and Dash
    # calls the dependent callbacks when the component is first rendered).
    # So, if `rows` is `None`, then the component was just rendered
    # and its value will be the same as the component's dataframe.
    # Instead of setting `None` in here, you could also set
    # `derived_virtual_data=df.to_rows('dict')` when you initialize
    # the component.

    if value not in ['Brazil', 'Chile', 'Germany', 'Spain']:

        if value == 'Worldwide':
            if Worldwide_derived_virtual_selected_rows is None:
                Worldwide_derived_virtual_selected_rows = []

            dff = WorldwildTable
            latitude = 14.056159 if len(Worldwide_derived_virtual_selected_rows) == 0 else dff.loc[Worldwide_selected_row_ids[0]].lat
            longitude = 6.395626 if len(Worldwide_derived_virtual_selected_rows) == 0 else dff.loc[Worldwide_selected_row_ids[0]].lon
            zoom = 1.02 if len(Worldwide_derived_virtual_selected_rows) == 0 else 4

	# Hover over de map for Worldwide
        hovertext_value = ['Faturamento: ${:n}<br>População: {:.0f}<br>Clientes: {:.0f}<br>Cli/Pop: {:.2%}<br>'.format(h, i, j, k) 
                            for h, i, j, k in zip(
                                df_latest['fatur'],
                                df_latest['population'],  
				df_latest['clientes'],
				df_latest['clientes']/df_latest['population']
                            )
        ]

	# MapBox Access Token here!!
        #mapbox_access_token = "pk.eyJ1IjoicGxvdGx5bWFwYm94IiwiYSI6ImNqdnBvNDMyaTAxYzkzeW5ubWdpZ2VjbmMifQ.TXcBE-xg9BFdV2ocecc_7g"
        mapbox_access_token = "pk.eyJ1Ijoid2FuZGVyZWxzayIsImEiOiJja2ZxcDB2aHowbmFnMnNzOXZ4dXNsc3lvIn0.ZmAPFa_Vcnhg5UdX4GKgKw"

        # Generate a list for hover country name text display
        textList = []
        for area, region in zip(df_latest['Province/State'], df_latest['Country/Region']):

            if type(area) is str:
                if region == "Hong Kong" or region == "Macau" or region == "Taiwan":
                    textList.append(area)
                else:
                    textList.append(area+', '+region)
            else:
                textList.append(region)

        # Generate a list for color gradient display
        colorList = []
        for faturamento, population in zip(df_latest['fatur'], df_latest['population']):
            remaining = faturamento / population 
            colorList.append(remaining)
   
        fig2 = go.Figure(go.Scattermapbox(
            lat=df_latest['lat'],
            lon=df_latest['lon'],
            mode='markers',
            marker=go.scattermapbox.Marker(
                color=['#f03f42' if i > 0 else '#2ecc77' for i in colorList],
                size=[i**(1/3) for i in df_latest['population']],
                sizemin=1,
                sizemode='area',
                sizeref=2.*max([math.sqrt(i)
                    for i in df_latest['population']])/(100.**2),
            ),
            text=textList,
            hovertext=hovertext_value,
            hovertemplate="<b>%{text}</b><br><br>" +
                          "%{hovertext}<br>" +
                          "<extra></extra>")
        )
        fig2.update_layout(
            plot_bgcolor='#ffffff',
            paper_bgcolor='#ffffff',
            margin=go.layout.Margin(l=10, r=10, b=10, t=0, pad=40),
            hovermode='closest',
            transition={'duration': 500},
#            annotations=[
#                dict(x=.5,
#                    y=-.0,
#                    align='center',
#                    showarrow=False,
#                    text="Points are placed based on data geolocation levels.<br>Province/State level - Australia, China, Canada, and United States; Country level- other countries.",
#                    xref="paper",
#                    yref="paper",
#                    font=dict(size=10, color='#292929'),
#                )
#            ],
            mapbox=go.layout.Mapbox(
                accesstoken=mapbox_access_token,
                style="light",
                # The direction you're facing, measured clockwise as an angle from true north on a compass
                bearing=0,
                center=go.layout.mapbox.Center(
                    lat=latitude,
                    lon=longitude
                ),
                pitch=0,
                zoom=zoom
            )
        )

        return fig2

    else:
        if value == 'Brazil':
            if Brazil_derived_virtual_selected_rows is None:
                Brazil_derived_virtual_selected_rows = []

            dff = BrazilTable
            latitude = -15.749997 if len(Brazil_derived_virtual_selected_rows) == 0 else dff.loc[Brazil_selected_row_ids[0]].lat
            longitude = -47.9499962 if len(Brazil_derived_virtual_selected_rows) == 0 else dff.loc[Brazil_selected_row_ids[0]].lon
            zoom = 2.7 if len(Brazil_derived_virtual_selected_rows) == 0 else 5

            fig2 = render_region_map(df_brazil, dff, latitude, longitude, zoom)
        
        elif value == 'Chile':
            if Chile_derived_virtual_selected_rows is None:
                Chile_derived_virtual_selected_rows = []

            dff = ChileTable
            latitude = -35.6751 if len(Chile_derived_virtual_selected_rows) == 0 else dff.loc[Chile_selected_row_ids[0]].lat
            longitude = -71.5430 if len(Chile_derived_virtual_selected_rows) == 0 else dff.loc[Chile_selected_row_ids[0]].lon
            zoom = 3 if len(Chile_derived_virtual_selected_rows) == 0 else 5

            fig2 = render_region_map(df_chile, dff, latitude, longitude, zoom)

        elif value == 'Germany':
            if Germany_derived_virtual_selected_rows is None:
                Germany_derived_virtual_selected_rows = []

            dff = GermanyTable
            latitude = 50.849548 if len(Germany_derived_virtual_selected_rows) == 0 else dff.loc[Germany_selected_row_ids[0]].lat
            longitude = 10.231292 if len(Germany_derived_virtual_selected_rows) == 0 else dff.loc[Germany_selected_row_ids[0]].lon
            zoom = 4.5 if len(Germany_derived_virtual_selected_rows) == 0 else 5

            fig2 = render_region_map(df_germany, dff, latitude, longitude, zoom)

        elif value == 'Spain':
            if Spain_derived_virtual_selected_rows is None:
                Spain_derived_virtual_selected_rows = []

            dff = SpainTable
            latitude = 40.4168 if len(Spain_derived_virtual_selected_rows) == 0 else dff.loc[Spain_selected_row_ids[0]].lat
            longitude = -3.7038 if len(Spain_derived_virtual_selected_rows) == 0 else dff.loc[Spain_selected_row_ids[0]].lon
            zoom = 4.5 if len(Spain_derived_virtual_selected_rows) == 0 else 5

            fig2 = render_region_map(df_spain, dff, latitude, longitude, zoom)
  
        return fig2

@app.callback(
    Output('datatable-interact-lineplot', 'figure'),
    input_list
)
def update_lineplot(
  value, 
  derived_virtual_selected_rows, selected_row_ids,
  Brazil_derived_virtual_selected_rows, Brazil_selected_row_ids,
  Chile_derived_virtual_selected_rows, Chile_selected_row_ids,
  Germany_derived_virtual_selected_rows, Germany_selected_row_ids,
  Spain_derived_virtual_selected_rows, Spain_selected_row_ids,
  ):
    if value == 'Worldwide':
      if derived_virtual_selected_rows is None:
        derived_virtual_selected_rows = []

      dff = WorldwildTable

      if selected_row_ids:
        if selected_row_ids[0] == 'Mainland China':
          Region = 'China'
        else:
          Region = selected_row_ids[0]
      else:
        Region = 'Worldwide' # Display the global total case number 

    elif value == 'Brazil':
      if Brazil_derived_virtual_selected_rows is None:
        Brazil_derived_virtual_selected_rows = []

      dff = BrazilTable
      if Brazil_selected_row_ids:
        Region = Brazil_selected_row_ids[0]
      else:
        Region = 'Brazil'

    elif value == 'Chile':
      if Chile_derived_virtual_selected_rows is None:
        Chile_derived_virtual_selected_rows = []

      dff = ChileTable
      if Chile_selected_row_ids:
        Region = Chile_selected_row_ids[0]
      else:
        Region = 'Chile'

    elif value == 'Germany':
      if Germany_derived_virtual_selected_rows is None:
        Germany_derived_virtual_selected_rows = []

      dff = GermanyTable
      if Germany_selected_row_ids:
        Region = Germany_selected_row_ids[0]
      else:
        Region = 'Germany'

    elif value == 'Spain':
      if Spain_derived_virtual_selected_rows is None:
        Spain_derived_virtual_selected_rows = []

      dff = SpainTable
      if Spain_selected_row_ids:
        Region = Spain_selected_row_ids[0]
      else:
        Region = 'Spain'

    # Read cumulative data of a given region from ./cumulative_data folder
    df_region = pd.read_csv('./cumulative_data/{}.csv'.format(Region))
    df_region = df_region.astype(
        {'date_day': 'datetime64'})

    # Create empty figure canvas
    fig3 = go.Figure()
    # Add trace to the figure
    fig3.add_trace(go.Scatter(x=df_region['date_day'],
                           y=df_region['Confirmed'],
                           mode='lines+markers',
                           #name='Confirmed case',
                           name='Confirmed attendances',
                           line=dict(color='#f03f42', width=2),
                           text=[datetime.strftime(d, '%b %d %Y GMT+10')
                                                   for d in df_region['date_day']],
                           #hovertext=['{} Confirmed<br>{:,d} cases<br>'.format(
                           hovertext=['{} Confirmed<br>{:,d} attendances<br>'.format(
                               Region, i) for i in df_region['Confirmed']],
                           hovertemplate=
                                                   '%{hovertext}' +
                                                   '<extra></extra>'))
    fig3.add_trace(go.Scatter(x=df_region['date_day'],
                           y=df_region['Recovered'],
                           mode='lines+markers',
                           #name='Recovered case',
                           name='Recovered attendances',
                           line=dict(color='#2ecc77', width=2),
                           text=[datetime.strftime(d, '%b %d %Y GMT+10')
                                                   for d in df_region['date_day']],
                           hovertext=['{} Recovered<br>{:,d} attendances<br>'.format(
                               Region, i) for i in df_region['Recovered']],
                           hovertemplate=
                                                   '%{hovertext}' +
                                                   '<extra></extra>'))
    fig3.add_trace(go.Scatter(x=df_region['date_day'],
                           y=df_region['Deaths'],
                           mode='lines+markers',
                           #name='Death case',
                           name='Lost attendances',
                           line=dict(color='#7f7f7f', width=2),
                           text=[datetime.strftime(d, '%b %d %Y GMT+10')
                                                   for d in df_region['date_day']],
                           #hovertext=['{} Deaths<br>{:,d} cases<br>'.format(
                           hovertext=['{} Lost<br>{:,d} attendances<br>'.format(
                               Region, i) for i in df_region['Deaths']],
                           hovertemplate=
                                                   '%{hovertext}' +
                                                   '<extra></extra>'))
    # Customise layout
    fig3.update_layout(
      margin=go.layout.Margin(
          l=10,
          r=10,
          b=10,
          t=5,
          pad=0
      ),
      annotations=[
          dict(
              x=.5,
              y=.4,
              xref="paper",
              yref="paper",
              text=Region,
              opacity=0.5,
              font=dict(family='Roboto, sans-serif',
                        size=40,
                        color="grey"),
          )
      ],
      #yaxis_title="Cumulative case numbers",
      yaxis_title="Cumulative attendance numbers",
      yaxis=dict(
          showline=False, linecolor='#272e3e',
          zeroline=False,
          gridcolor='rgba(203, 210, 211,.3)',
          gridwidth=.1,
          tickmode='array',
      ),
      xaxis_title="Select a location from the table (Toggle the legend to see specific curve)",
      xaxis=dict(
          showline=False, linecolor='#272e3e',
          showgrid=False,
          gridcolor='rgba(203, 210, 211,.3)',
          gridwidth=.1,
          zeroline=False
      ),
      xaxis_tickformat='%b %d',
      #transition = {'duration':500},
      hovermode='x unified',
      legend_orientation="h",
      legend=dict(x=.02, y=1.15, bgcolor="rgba(0,0,0,0)",),
      plot_bgcolor='#ffffff',
      paper_bgcolor='#ffffff',
      font=dict(color='#292929', size=10)
    )

    return fig3

@app.callback(
    Output('datatable-interact-dailyplot', 'figure'),
    input_list
)

def update_dailyplot(
  value, 
  derived_virtual_selected_rows, selected_row_ids,
  Brazil_derived_virtual_selected_rows, Brazil_selected_row_ids,
  Chile_derived_virtual_selected_rows, Chile_selected_row_ids,
  Germany_derived_virtual_selected_rows, Germany_selected_row_ids,
  Spain_derived_virtual_selected_rows, Spain_selected_row_ids,
  ):

    if value == 'Worldwide':
      if derived_virtual_selected_rows is None:
        derived_virtual_selected_rows = []

      dff = WorldwildTable

      if selected_row_ids:
        if selected_row_ids[0] == 'Mainland China':
          Region = 'China'
        else:
          Region = selected_row_ids[0]
      else:
        Region = 'Worldwide' # Display the global total case number 

    elif value == 'Brazil':
      if Brazil_derived_virtual_selected_rows is None:
        Brazil_derived_virtual_selected_rows = []

      dff = BrazilTable
      if Brazil_selected_row_ids:
        Region = Brazil_selected_row_ids[0]
      else:
        Region = 'Brazil'
	
    elif value == 'Chile':
      if Chile_derived_virtual_selected_rows is None:
        Chile_derived_virtual_selected_rows = []

      dff = ChileTable
      if Chile_selected_row_ids:
        Region = Chile_selected_row_ids[0]
      else:
        Region = 'Chile'

    elif value == 'Germany':
      if Germany_derived_virtual_selected_rows is None:
        Germany_derived_virtual_selected_rows = []

      dff = GermanyTable
      if Germany_selected_row_ids:
        Region = Germany_selected_row_ids[0]
      else:
        Region = 'Germany'

    elif value == 'Spain':
      if Spain_derived_virtual_selected_rows is None:
        Spain_derived_virtual_selected_rows = []

      dff = SpainTable
      if Spain_selected_row_ids:
        Region = Spain_selected_row_ids[0]
      else:
        Region = 'Spain'

    # Read cumulative data of a given region from ./cumulative_data folder
    df_region = pd.read_csv('./cumulative_data/{}.csv'.format(Region))
    df_region = df_region.astype(
        {'date_day': 'datetime64'})
    
    df_region = df_region.sort_values(by='date_day')
    df_region['rolling_mean'] = df_region['New'].rolling(7).mean()
    #df_region['rolling_mean'] = df_region['rolling_mean'].fillna(value=0)


    # Create empty figure canvas
    fig_daily = go.Figure()
    # Add trace to the figure
    fig_daily.add_trace(go.Scatter(x=df_region['date_day'],
                                y=df_region['New'],
                                fill='tozeroy',
                                mode='lines',
                                #name='Daily confirmed case',
                                name='Daily confirmed attendances',
                                line=dict(color='#f03f42', width=0),
                                text=[datetime.strftime(d, '%b %d %Y GMT+10')
                                                     for d in df_region['date_day']],
                                #hovertext=['Daily confirmed cases {:,d} <br>'.format(
                                hovertext=['Daily confirmed attendances {:,d} <br>'.format(
                                  i) for i in df_region['New']],
                                hovertemplate=
                                                      '%{hovertext}' +
                                                     '<extra></extra>'))
    fig_daily.add_trace(go.Scatter(x=df_region['date_day'],
                                y=df_region['rolling_mean'],
                                mode='lines',
                                line_shape='spline',
                                name='7-day rolling mean',
                                line=dict(color='#f03f42', width=2),
                                text=[datetime.strftime(d, '%b %d %Y GMT+10')
                                                     for d in df_region['date_day']],
                                hovertext=['7-day average confirmed attendances {:.0f} <br>'.format(
                                  i) for i in df_region['rolling_mean']],
                                hovertemplate=
                                                      '%{hovertext}' +
                                                     '<extra></extra>'))
    fig_daily.add_trace(go.Scatter(x=df_region['date_day'],
                                y=df_region['New_recover'],
                                fill='tozeroy',
                                mode='lines',
                                name='Daily recovered attendances',
                                line=dict(color='#2ecc77', width=0),
                                text=[datetime.strftime(d, '%b %d %Y GMT+10')
                                                     for d in df_region['date_day']],
                                hovertext=['Daily recovered attendances {:,d} <br>'.format(
                                  i) for i in df_region['New_recover']],
                                hovertemplate=
                                                      '%{hovertext}' +
                                                     '<extra></extra>'))
    fig_daily.add_trace(go.Scatter(x=df_region['date_day'],
                                y=df_region['New_death'],
                                fill='tozeroy',
                                mode='lines',
                                name='Daily lost attendances',
                                line=dict(color='#7f7f7f', width=0),
                                text=[datetime.strftime(d, '%b %d %Y GMT+10')
                                                     for d in df_region['date_day']],
                                hovertext=['Daily lost attendances {:,d} <br>'.format(
                                  i) for i in df_region['New_death']],
                                hovertemplate=
                                                      '%{hovertext}' +
                                                     '<extra></extra>'))
      
    # Customise layout
    fig_daily.update_layout(
            margin=go.layout.Margin(
                l=10,
                r=10,
                b=10,
                t=5,
                pad=0
            ),
            annotations=[
                dict(
                    x=.5,
                    y=.4,
                    xref="paper",
                    yref="paper",
                    text=Region,
                    opacity=0.5,
                    font=dict(family='Roboto, sans-serif',
                        size=40,
                        color="grey"
                    ),
                )
            ],
            #yaxis_title="Daily case numbers",
            yaxis_title="Daily attendance numbers",
            yaxis=dict(
                showline=False, linecolor='#272e3e',
                zeroline=False,
                gridcolor='rgba(203, 210, 211,.3)',
                gridwidth=.1,
                tickmode='array',
            ),
            xaxis_title="Select a location from the table (Toggle the legend to see specific curve)",
            xaxis=dict(
                showline=False, linecolor='#272e3e',
                showgrid=False,
                gridcolor='rgba(203, 210, 211,.3)',
                gridwidth=.1,
                zeroline=False
            ),
            xaxis_tickformat='%b %d',
            #transition = {'duration':500},
            hovermode='x unified',
            legend_orientation="h",
            legend=dict(x=.02, y=1.15, bgcolor="rgba(0,0,0,0)",),
            plot_bgcolor='#ffffff',
            paper_bgcolor='#ffffff',
            font=dict(color='#292929', size=10)
            )

    return fig_daily

@app.callback(
    Output('datatable-interact-logplot', 'figure'),
    input_list
)
def update_logplot(value, derived_virtual_selected_rows, selected_row_ids,
  Brazil_derived_virtual_selected_rows, Brazil_selected_row_ids,
  Chile_derived_virtual_selected_rows, Chile_selected_row_ids,
  Germany_derived_virtual_selected_rows, Germany_selected_row_ids,
  Spain_derived_virtual_selected_rows, Spain_selected_row_ids,
  ):
   
    if value == 'Worldwide':
      if derived_virtual_selected_rows is None:
        derived_virtual_selected_rows = []

      if selected_row_ids:
        if selected_row_ids[0] == 'Mainland China':
          Region = 'China'
        else:
          Region = selected_row_ids[0]
      else:
        Region = 'Worldwide'
    
    elif value == 'Brazil':
      if Brazil_derived_virtual_selected_rows is None:
        Brazil_derived_virtual_selected_rows = []

      if Brazil_selected_row_ids:
        Region = Brazil_selected_row_ids[0]
      else:
        Region = 'Brazil'

    elif value == 'Chile':
      if Chile_derived_virtual_selected_rows is None:
        Chile_derived_virtual_selected_rows = []

      if Chile_selected_row_ids:
        Region = Chile_selected_row_ids[0]
      else:
        Region = 'Chile'

    elif value == 'Germany':
      if Germany_derived_virtual_selected_rows is None:
        Germany_derived_virtual_selected_rows = []

      if Germany_selected_row_ids:
        Region = Germany_selected_row_ids[0]
      else:
        Region = 'Germany'

    elif value == 'Spain':
      if Spain_derived_virtual_selected_rows is None:
        Spain_derived_virtual_selected_rows = []

      if Spain_selected_row_ids:
        Region = Spain_selected_row_ids[0]
      else:
        Region = 'Spain'

    elapseDay = daysOutbreak
    # Create empty figure canvas
    fig_curve = go.Figure()

    fig_curve.add_trace(go.Scatter(x=pseduoDay,
                                   y=y1,
                                   line=dict(color='rgba(0, 0, 0, .3)', width=1, dash='dot'),
                                   text=[
                                       '85% growth rate' for i in pseduoDay],
                                   hovertemplate='<b>%{text}</b><br>' +
                                                 'Doubles every 1.1 days<br>' +
                                                 '<extra></extra>'
                            )
    )
    fig_curve.add_trace(go.Scatter(x=pseduoDay,
                                   y=y2,
                                   line=dict(color='rgba(0, 0, 0, .3)', width=1, dash='dot'),
                                   text=[
                                        '35% growth rate' for i in pseduoDay],
                                   hovertemplate='<b>%{text}</b><br>' +
                                                 'Doubles every 2.3 days<br>' +
                                                 '<extra></extra>'
                            )
    )
    fig_curve.add_trace(go.Scatter(x=pseduoDay,
                                   y=y3,
                                   line=dict(color='rgba(0, 0, 0, .3)', width=1, dash='dot'),
                                   text=[
                                        '15% growth rate' for i in pseduoDay],
                                   hovertemplate='<b>%{text}</b><br>' +
                                                 'Doubles every 5 days<br>' +
                                                 '<extra></extra>'
                            )
    )
    fig_curve.add_trace(go.Scatter(x=pseduoDay,
                                   y=y4,
                                   line=dict(color='rgba(0, 0, 0, .3)', width=1, dash='dot'),
                                   text=[
                                        '5% growth rate' for i in pseduoDay],
                                   hovertemplate='<b>%{text}</b><br>' +
                                                 'Doubles every 14.2 days<br>' +
                                                 '<extra></extra>'
                            )
    )

    # Add trace to the figure
    if Region in set(dfs_curve['Region']):

        dotx = [np.array(dfs_curve.loc[dfs_curve['Region'] == Region,'DayElapsed'])[0]]
        doty = [np.array(dfs_curve.loc[dfs_curve['Region'] == Region,'Confirmed'])[0]]

        for regionName in ['Worldwide', 'Brazil', 'Chile', 'Germany', 'Spain']:

          dotgrayx = [np.array(dfs_curve.loc[dfs_curve['Region'] == regionName, 'DayElapsed'])[0]]
          dotgrayy = [np.array(dfs_curve.loc[dfs_curve['Region'] == regionName, 'Confirmed'])[0]]


          fig_curve.add_trace(go.Scatter(x=dfs_curve.loc[dfs_curve['Region'] == regionName]['DayElapsed'],
                                         y=dfs_curve.loc[dfs_curve['Region'] == regionName]['Confirmed'],
                                         mode='lines',
                                         line_shape='spline',
                                         name=regionName,
                                         opacity=0.3,
                                         line=dict(color='#636363', width=1.5),
                                         text=[
                                            i for i in dfs_curve.loc[dfs_curve['Region'] == regionName]['Region']],
                                         hovertemplate='<b>%{text}</b><br>' +
                                                       '%{y:,d}<br>'
                                                       '<br>after %{x} clients<br>'
                                                       '<extra></extra>'
                             )
          )
          fig_curve.add_trace(go.Scatter(x=dotgrayx,
                                         y=dotgrayy,
                                         mode='markers',
                                         marker=dict(size=6, color='#636363',
                                         line=dict(width=1, color='#636363')),
                                         opacity=0.5,
                                         text=[regionName],
                                         hovertemplate='<b>%{text}</b><br>' +
                                                       '%{y:,d}<br>'
                                                       '<br>after %{x} clients<br>'
                                                       '<extra></extra>'
                            )
          )
          
        fig_curve.add_trace(go.Scatter(x=dfs_curve.loc[dfs_curve['Region'] == Region]['DayElapsed'],
                                       y=dfs_curve.loc[dfs_curve['Region'] == Region]['Confirmed'],
                                       mode='lines',
                                       line_shape='spline',
                                       name=Region,
                                       line=dict(color='#f03f42', width=3),
                                       text=[
                                           i for i in dfs_curve.loc[dfs_curve['Region'] == Region]['Region']],
                                       hovertemplate='<b>%{text}</b><br>' +
                                                     '%{y:,d}<br>'
                                                     '<br>after %{x} clients<br>'
                                                     '<extra></extra>'
                            )
          )
        fig_curve.add_trace(go.Scatter(x=dotx,
                                       y=doty,
                                       mode='markers',
                                       marker=dict(size=7, color='#f03f42',
                                       line=dict(width=1, color='#f03f42')),
                                       text=[Region],
                                       hovertemplate='<b>%{text}</b><br>' +
                                                     '%{y:,d}<br>'
                                                     '<br>after %{x} clients<br>'
                                                     '<extra></extra>'
                            )
        )

    else:
        for regionName in ['Worldwide', 'Brazil', 'Chile', 'Germany', 'Spain']:

          dotgrayx = [np.array(dfs_curve.loc[dfs_curve['Region'] == regionName, 'DayElapsed'])[0]]
          dotgrayy = [np.array(dfs_curve.loc[dfs_curve['Region'] == regionName, 'Confirmed'])[0]]

          fig_curve.add_trace(go.Scatter(x=dfs_curve.loc[dfs_curve['Region'] == regionName]['DayElapsed'],
                                         y=dfs_curve.loc[dfs_curve['Region'] == regionName]['Confirmed'],
                                         mode='lines',
                                         line_shape='spline',
                                         name=regionName,
                                         opacity=0.3,
                                         line=dict(color='#636363', width=1.5),
                                         text=[
                                            i for i in dfs_curve.loc[dfs_curve['Region'] == regionName]['Region']],
                                         hovertemplate='<b>%{text}</b><br>' +
                                                       '%{y:,d}<br>'
                                                       '<br>after %{x} clients<br>'
                                                       '<extra></extra>'
                             )
          )

          fig_curve.add_trace(go.Scatter(x=dotgrayx,
                                         y=dotgrayy,
                                         mode='markers',
                                         marker=dict(size=6, color='#636363',
                                         line=dict(width=1, color='#636363')),
                                         opacity=0.5,
                                         text=[regionName],
                                         hovertemplate='<b>%{text}</b><br>' +
                                                       '%{y:,d}<br>'
                                                       '<br>after %{x} clients<br>'
                                                       '<extra></extra>'
                            )
          )

    # Customise layout
    fig_curve.update_xaxes(range=[0, elapseDay-19])
    fig_curve.update_yaxes(range=[1.9, 7.5])
    fig_curve.update_layout(
        xaxis_title="Number of clients",
        yaxis_title="Faturamento (Logarithmic)",
        margin=go.layout.Margin(
            l=10,
            r=10,
            b=10,
            t=5,
            pad=0
            ),
        annotations=[
            dict(
                x=.5,
                y=.4,
                xref="paper",
                yref="paper",
                text=Region if Region in set(dfs_curve['Region']) else "Not over 10 clients",
                opacity=0.5,
                font=dict(family='Roboto, sans-serif',
                          size=40,
                          color="grey"),
            )
        ],
        yaxis_type="log",
        yaxis=dict(
            showline=False, 
            linecolor='#272e3e',
            zeroline=False,
            gridcolor='rgba(203, 210, 211,.3)',
            gridwidth = .1,
        ),
        xaxis=dict(
            showline=False, 
            linecolor='#272e3e',
            gridcolor='rgba(203, 210, 211,.3)',
            gridwidth = .1,
            zeroline=False
        ),
        showlegend=False,
        # hovermode = 'x unified',
        transition = {'duration':500},
        plot_bgcolor='#ffffff',
        paper_bgcolor='#ffffff',
        font=dict(color='#292929', size=10)
    )

    return fig_curve

@app.callback(
    Output('datatable-interact-deathplot', 'figure'),
    input_list
)
def update_deathplot(value, derived_virtual_selected_rows, selected_row_ids,
  Brazil_derived_virtual_selected_rows, Brazil_selected_row_ids,
  Chile_derived_virtual_selected_rows, Chile_selected_row_ids,
  Germany_derived_virtual_selected_rows, Germany_selected_row_ids,
  Spain_derived_virtual_selected_rows, Spain_selected_row_ids,
  ):
   
    if value == 'Worldwide':
      if derived_virtual_selected_rows is None:
        derived_virtual_selected_rows = []

      if selected_row_ids:
        if selected_row_ids[0] == 'Mainland China':
          Region = 'China'
        else:
          Region = selected_row_ids[0]
      else:
        Region = 'Worldwide'
    
    elif value == 'Brazil':
      if Brazil_derived_virtual_selected_rows is None:
        Brazil_derived_virtual_selected_rows = []

      if Brazil_selected_row_ids:
        Region = Brazil_selected_row_ids[0]
      else:
        Region = 'Brazil'

    elif value == 'Chile':
      if Chile_derived_virtual_selected_rows is None:
        Chile_derived_virtual_selected_rows = []

      if Chile_selected_row_ids:
        Region = Chile_selected_row_ids[0]
      else:
        Region = 'Chile'

    elif value == 'Germany':
      if Germany_derived_virtual_selected_rows is None:
        Germany_derived_virtual_selected_rows = []

      if Germany_selected_row_ids:
        Region = Germany_selected_row_ids[0]
      else:
        Region = 'Germany'

    elif value == 'Spain':
      if Spain_derived_virtual_selected_rows is None:
        Spain_derived_virtual_selected_rows = []

      if Spain_selected_row_ids:
        Region = Spain_selected_row_ids[0]
      else:
        Region = 'Spain'

    elapseDay = daysOutbreak
    # Create empty figure canvas
    fig_curve_death = go.Figure()

    fig_curve_death.add_trace(go.Scatter(x=pseduoDay,
                                   y=z1,
                                   line=dict(color='rgba(0, 0, 0, .3)', width=1, dash='dot'),
                                   text=[
                                       '85% growth rate' for i in pseduoDay],
                                   hovertemplate='<b>%{text}</b><br>' +
                                                 'Doubles every 1.1 days<br>' +
                                                 '<extra></extra>'
                            )
    )
    fig_curve_death.add_trace(go.Scatter(x=pseduoDay,
                                   y=z2,
                                   line=dict(color='rgba(0, 0, 0, .3)', width=1, dash='dot'),
                                   text=[
                                        '35% growth rate' for i in pseduoDay],
                                   hovertemplate='<b>%{text}</b><br>' +
                                                 'Doubles every 2.3 days<br>' +
                                                 '<extra></extra>'
                            )
    )
    fig_curve_death.add_trace(go.Scatter(x=pseduoDay,
                                   y=z3,
                                   line=dict(color='rgba(0, 0, 0, .3)', width=1, dash='dot'),
                                   text=[
                                        '15% growth rate' for i in pseduoDay],
                                   hovertemplate='<b>%{text}</b><br>' +
                                                 'Doubles every 5 days<br>' +
                                                 '<extra></extra>'
                            )
    )
    fig_curve_death.add_trace(go.Scatter(x=pseduoDay,
                                   y=z4,
                                   line=dict(color='rgba(0, 0, 0, .3)', width=1, dash='dot'),
                                   text=[
                                        '5% growth rate' for i in pseduoDay],
                                   hovertemplate='<b>%{text}</b><br>' +
                                                 'Doubles every 14.2 days<br>' +
                                                 '<extra></extra>'
                            )
    )

    # Add trace to the figure
    if Region in set(dfs_curve_death['Region']):

        dotx_death = [np.array(dfs_curve_death.loc[dfs_curve_death['Region'] == Region,'DayElapsed_death'])[0]]
        doty_death = [np.array(dfs_curve_death.loc[dfs_curve_death['Region'] == Region,'Deaths'])[0]]

        for regionName in ['Worldwide', 'Brazil', 'Chile', 'Germany', 'Spain']:

          dotgrayx_death = [np.array(dfs_curve_death.loc[dfs_curve_death['Region'] == regionName, 'DayElapsed_death'])[0]]
          dotgrayy_death = [np.array(dfs_curve_death.loc[dfs_curve_death['Region'] == regionName, 'Deaths'])[0]]


          fig_curve_death.add_trace(go.Scatter(x=dfs_curve_death.loc[dfs_curve_death['Region'] == regionName]['DayElapsed_death'],
                                         y=dfs_curve_death.loc[dfs_curve_death['Region'] == regionName]['Deaths'],
                                         mode='lines',
                                         line_shape='spline',
                                         name=regionName,
                                         opacity=0.3,
                                         line=dict(color='#636363', width=1.5),
                                         text=[
                                            i for i in dfs_curve_death.loc[dfs_curve_death['Region'] == regionName]['Region']],
                                         hovertemplate='<b>%{text}</b><br>' +
                                                       '%{y:,d}<br>'
                                                       '<br>after %{x} clients<br>'
                                                       '<extra></extra>'
                             )
          )
          fig_curve_death.add_trace(go.Scatter(x=dotgrayx_death,
                                         y=dotgrayy_death,
                                         mode='markers',
                                         marker=dict(size=6, color='#636363',
                                         line=dict(width=1, color='#636363')),
                                         opacity=0.5,
                                         text=[regionName],
                                         hovertemplate='<b>%{text}</b><br>' +
                                                       '%{y:,d}<br>'
                                                       '<br>after %{x} clients<br>'
                                                       '<extra></extra>'
                            )
          )
          
        fig_curve_death.add_trace(go.Scatter(x=dfs_curve_death.loc[dfs_curve_death['Region'] == Region]['DayElapsed_death'],
                                       y=dfs_curve_death.loc[dfs_curve_death['Region'] == Region]['Deaths'],
                                       mode='lines',
                                       line_shape='spline',
                                       name=Region,
                                       line=dict(color='#7f7f7f', width=3),
                                       text=[
                                           i for i in dfs_curve_death.loc[dfs_curve_death['Region'] == Region]['Region']],
                                       hovertemplate='<b>%{text}</b><br>' +
                                                     '%{y:,d}<br>'
                                                     '<br>after %{x} clients<br>'
                                                     '<extra></extra>'
                            )
          )
        fig_curve_death.add_trace(go.Scatter(x=dotx_death,
                                       y=doty_death,
                                       mode='markers',
                                       marker=dict(size=7, color='#7f7f7f',
                                       line=dict(width=1, color='#7f7f7f')),
                                       text=[Region],
                                       hovertemplate='<b>%{text}</b><br>' +
                                                     '%{y:,d}<br>'
                                                     '<br>after %{x} clients<br>'
                                                     '<extra></extra>'
                            )
        )

    else:
        for regionName in ['Worldwide', 'Brazil', 'Chile', 'Germany', 'Spain']:

          dotgrayx_death = [np.array(dfs_curve_death.loc[dfs_curve_death['Region'] == regionName, 'DayElapsed_death'])[0]]
          dotgrayy_death = [np.array(dfs_curve_death.loc[dfs_curve_death['Region'] == regionName, 'Deaths'])[0]]

          fig_curve_death.add_trace(go.Scatter(x=dfs_curve_death.loc[dfs_curve_death['Region'] == regionName]['DayElapsed_death'],
                                         y=dfs_curve_death.loc[dfs_curve_death['Region'] == regionName]['Deaths'],
                                         mode='lines',
                                         line_shape='spline',
                                         name=regionName,
                                         opacity=0.3,
                                         line=dict(color='#636363', width=1.5),
                                         text=[
                                            i for i in dfs_curve_death.loc[dfs_curve_death['Region'] == regionName]['Region']],
                                         hovertemplate='<b>%{text}</b><br>' +
                                                       '%{y:,d}<br>'
                                                       '<br>after %{x} clients<br>'
                                                       '<extra></extra>'
                             )
          )

          fig_curve_death.add_trace(go.Scatter(x=dotgrayx_death,
                                         y=dotgrayy_death,
                                         mode='markers',
                                         marker=dict(size=6, color='#636363',
                                         line=dict(width=1, color='#636363')),
                                         opacity=0.5,
                                         text=[regionName],
                                         hovertemplate='<b>%{text}</b><br>' +
                                                       '%{y:,d}<br>'
                                                       '<br>after %{x} clients<br>'
                                                       '<extra></extra>'
                            )
          )

    # Customise layout
    fig_curve_death.update_xaxes(range=[0, elapseDay-19])
    fig_curve_death.update_yaxes(range=[0.477, 5.8])
    fig_curve_death.update_layout(
        #xaxis_title="Number of days since 3 deaths recorded",
        #yaxis_title="Death cases (Logarithmic)",
        xaxis_title="Number of clients",
        yaxis_title="Lost cases (Logarithmic)",
        margin=go.layout.Margin(
            l=10,
            r=10,
            b=10,
            t=5,
            pad=0
            ),
        annotations=[dict(
            x=.5,
            y=.4,
            xref="paper",
            yref="paper",
            #text=Region if Region in set(dfs_curve['Region']) else "Not over 3 death cases",
            text=Region if Region in set(dfs_curve['Region']) else "Not over 10 clients",
            opacity=0.5,
            font=dict(family='Roboto, sans-serif',
                          size=40,
                          color="grey"),
                    )
        ],
        yaxis_type="log",
        yaxis=dict(
            showline=False, 
            linecolor='#272e3e',
            zeroline=False,
            gridcolor='rgba(203, 210, 211,.3)',
            gridwidth = .1,
        ),
        xaxis=dict(
            showline=False, 
            linecolor='#272e3e',
            gridcolor='rgba(203, 210, 211,.3)',
            gridwidth = .1,
            zeroline=False
        ),
        showlegend=False,
        # hovermode = 'x unified',
        transition = {'duration':500},
        plot_bgcolor='#ffffff',
        paper_bgcolor='#ffffff',
        font=dict(color='#292929', size=10)
    )

    return fig_curve_death



if __name__ == "__main__":
    app.run_server(debug=True)

