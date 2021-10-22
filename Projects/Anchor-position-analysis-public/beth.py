import requests
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import datetime
import seaborn as sns
from scipy.stats import pearsonr,spearmanr


maxLTV = 0.6 # the maximum LTV ratio of collateral

risk_rating = ['A','B+','B','B-','C','D','liquidation']

def get_scale(collateral_loan_ratio):
    risk_ratio1 = [str(f'{100/i:.0f}%') for i in collateral_loan_ratio]
    risk_ratio2 = ['0']+risk_ratio1[:-1]
    risk_ratio = [f'{risk_ratio2[i]} - {risk_ratio1[i]}' for i in range(len(risk_ratio1))]
    risk_ratio.append('>=100%')
    collateral_loan_ratio_list1 = [str(f'{i:.2f}x') for i in collateral_loan_ratio]
    collateral_loan_ratio_list2 = ['>']+collateral_loan_ratio_list1[:-1]
    collateral_loan_ratio_list = [f'{collateral_loan_ratio_list2[i]} - {collateral_loan_ratio_list1[i]}' for i in range(len(collateral_loan_ratio_list2))]
    collateral_loan_ratio_list.append('=1.00x')
    risk_rating = ['A','B+','B','B-','C','D','liquidation']

    return pd.DataFrame(data={'collateral/loan ratio' : collateral_loan_ratio_list, 'risk ratio' : risk_ratio, 'risk rating' : risk_rating})

def get_scale_dic(collateral_loan_ratio):
    return [round(100/i,2) for i in collateral_loan_ratio]

def loan_collector():
    """This function collect information about all loans in anchor market protocol, and return list of dictionaries, 
    which contains wallet id and loan of this wallet."""
    #Amount of addresses per query is limited by 30 in anchor market smart contract
    initial_loan_query = requests.get('https://lcd.terra.dev/wasm/contracts/terra1sepfj7s0aeg5967uxnfk4thzlerrsktkpelm5s/store?query_msg={%22borrower_infos%22:%20{%22limit%22:30}}').json()['result']['borrower_infos']
    loans_list = []
    #We manually perform the first iteration of the while loop since in the case of the first iteration, 
    #we do not specify the "start_after"  parameter, in order to receive latest addresses with loans.
    for x in range(len(initial_loan_query)):
        loans_list.append({'wallet_id': initial_loan_query[x]['borrower'], 'ust_loan': initial_loan_query[x]['loan_amount']})
    support_cycle_loan_query = initial_loan_query
    
    #After first iteration we start while loop,which is executed as long as api provide us with 30 adresses. 
    while len(support_cycle_loan_query) == 30:
        link = 'https://lcd.terra.dev/wasm/contracts/terra1sepfj7s0aeg5967uxnfk4thzlerrsktkpelm5s/store?query_msg={%22borrower_infos%22:%20{%22limit%22:30,%22start_after%22:%22'+support_cycle_loan_query[29]['borrower']+'%22}}'
        cycle_loan_query = requests.get(link).json()['result']['borrower_infos']
        for x in range(len(cycle_loan_query)):
            loans_list.append({'wallet_id': cycle_loan_query[x]['borrower'], 'ust_loan': cycle_loan_query[x]['loan_amount']})
        support_cycle_loan_query = cycle_loan_query
                
    return loans_list

def collateral_collector():
    """This function collects information about all collaterals in anchor overseer protocol, and returns a list of dictionaries,
    with wallet id and collaterals in bLuna/bETH. This function uses the same algorithm as "loan_collector" function, 
    but in this case, we connect to Anchor Overseer contract"""
    initial_collateral_query = requests.get('https://lcd.terra.dev/wasm/contracts/terra1tmnqgvg567ypvsvk6rwsga3srp7e3lg6u0elp8/store?query_msg={%22all_collaterals%22:%20{%22limit%22:30}}').json()['result']["all_collaterals"]
    collaterals_list = []
    for x in range(len(initial_collateral_query)):
        #Since collateral could be only bETH, only bLuna, or both bLuna and bETH, we add "if" clause, 
        #in order to correctly save the data         
        if len(initial_collateral_query[x]['collaterals']) > 1:
            collaterals_list.append({'wallet_id': initial_collateral_query[x]['borrower'],
                                     initial_collateral_query[x]['collaterals'][0][0]:
                                         initial_collateral_query[x]['collaterals'][0][1],
                                     initial_collateral_query[x]['collaterals'][1][0]:
                                         initial_collateral_query[x]['collaterals'][1][1]})
        else:
            collaterals_list.append({'wallet_id': initial_collateral_query[x]['borrower'],
                                     initial_collateral_query[x]['collaterals'][0][0]:
                                         initial_collateral_query[x]['collaterals'][0][1]})

    support_cycle_collateral_query = initial_collateral_query
           
    while len(support_cycle_collateral_query) == 30:
        link = 'https://lcd.terra.dev/wasm/contracts/terra1tmnqgvg567ypvsvk6rwsga3srp7e3lg6u0elp8/store?query_msg={%22all_collaterals%22:%20{%22limit%22:30,%22start_after%22:%22'+support_cycle_collateral_query[29]['borrower']+'%22}}'
        cycle_collateral_query = requests.get(link).json()['result']["all_collaterals"]
        for x in range(len(cycle_collateral_query)):
            if len(cycle_collateral_query[x]['collaterals']) > 1:
                collaterals_list.append({'wallet_id': cycle_collateral_query[x]['borrower'],
                                         cycle_collateral_query[x]['collaterals'][0][0]:
                                             cycle_collateral_query[x]['collaterals'][0][1],
                                         cycle_collateral_query[x]['collaterals'][1][0]:
                                             cycle_collateral_query[x]['collaterals'][1][1]})
            else:
                collaterals_list.append({'wallet_id': cycle_collateral_query[x]['borrower'],
                                         cycle_collateral_query[x]['collaterals'][0][0]:
                                             cycle_collateral_query[x]['collaterals'][0][1]})
        
        support_cycle_collateral_query = cycle_collateral_query
    
    return collaterals_list

def load_data_csv(filename):
    """This function create both csv file and dataframe with data about all wallets which uses bETH as collateral to their loan"""
    #We collect data about all loans and collaterals, and merge it to 1 DataFrame on wallet_id field
    loan_table = pd.DataFrame(loan_collector())
    collateral_table = pd.DataFrame(collateral_collector())
    raw_data = loan_table.merge(collateral_table, on='wallet_id', how='left')

    #Rename columns from smart contract adresses to name of tokens, and convert them to numeric format
    bAssets = {'wallet_id': 'borrower','ust_loan':'ust_loan','terra1kc87mu460fwkqte29rquh4hc20m54fxwtsx7gp': 'bLunacollateral',
               'terra1dzhzukyezv0etz22ud940z7adyv7xgcjkahuun': 'bETHcollateral'}
    raw_data.rename(columns=bAssets, inplace=True)
    raw_data['bLunacollateral'] = pd.to_numeric(raw_data['bLunacollateral'], errors="coerce").fillna(0)
    raw_data['bETHcollateral'] = pd.to_numeric(raw_data['bETHcollateral'], errors="coerce").fillna(0)

    #Remove wallets, which uses only bLuna as collateral 
    indexNames = raw_data[ raw_data['bETHcollateral'] == 0].index
    raw_data.drop(indexNames , inplace=True)

    #Sorting values by amount of  collatered bETH and calculate cumulative percent
    raw_data = raw_data.sort_values(by = 'bETHcollateral', ascending = False)
    raw_data['percent'] = raw_data.bETHcollateral.cumsum()/raw_data.bETHcollateral.sum()

    #Reorder columns, and save result as csv file
    raw_data = raw_data[['borrower','bETHcollateral','percent','ust_loan','bLunacollateral']]
    filtered_data=raw_data
    filtered_data.to_csv(filename, sep=',', encoding='utf-8',index=False)
    return filtered_data


def get_data_csv(filename): 
    """This function gets information from csv file"""    
    data = pd.read_csv(filename)
    data.columns = ['borrower','bETHcollateral','percent', 'ust_loan','bLunacollateral']
    data['ust_loan'] = pd.to_numeric(data.ust_loan)/pow(10,6)
    data['bLunacollateral'] = pd.to_numeric(data.bLunacollateral)/pow(10,6)
    data['bETHcollateral'] =  pd.to_numeric(data.bETHcollateral)/pow(10,6)        
               
    return data

def get_filtered_list(data, alfa = 1):
    data['percent'] = data.bETHcollateral.cumsum()/data.bETHcollateral.sum()
    return data[data.percent<=alfa].index.to_list()

def get_bluna_price():
        #feed price bLuna
    response = requests.get("https://lcd.terra.dev/wasm/contracts/terra1cgg6yef7qcdm070qftghfulaxmllgmvk77nc7t/store?query_msg=%7B%20%20%20%22price%22%3A%20%7B%20%20%20%20%20%22base%22%3A%20%22terra1kc87mu460fwkqte29rquh4hc20m54fxwtsx7gp%22%2C%20%20%22quote%22%3A%20%22uusd%22%20%20%20%20%7D%20%7D")
    bluna_price = pd.to_numeric(response.json()['result']['rate'])
    return bluna_price  

def get_beth_price():        
        #feed price bETH
    response = requests.get("https://lcd.terra.dev/wasm/contracts/terra1cgg6yef7qcdm070qftghfulaxmllgmvk77nc7t/store?query_msg=%7B%20%20%20%22price%22%3A%20%7B%20%20%20%20%20%22base%22%3A%20%22terra1dzhzukyezv0etz22ud940z7adyv7xgcjkahuun%22%2C%20%20%22quote%22%3A%20%22uusd%22%20%20%20%20%7D%20%7D")
    beth_price = pd.to_numeric(response.json()['result']['rate'])
    return beth_price


def get_risks(data, beth_price, bluna_price,collateral_loan_ratio):
    """This function calculates the risk level for each position and returns the positions sorted by risk""" 
    dfrisk = pd.DataFrame(data = data)
        
    dfrisk['bETHcollateral_USD'] = dfrisk['bETHcollateral']*beth_price
        
    dfrisk['bLunacollateral_USD'] = dfrisk['bLunacollateral']*bluna_price

    dfrisk['LTV_ratio'] = 100*dfrisk['ust_loan']/(dfrisk['bLunacollateral_USD'] + dfrisk['bETHcollateral_USD'])
    dfrisk['risk_ratio'] = 100*dfrisk['ust_loan']/((dfrisk['bLunacollateral_USD'] + dfrisk['bETHcollateral_USD'])*maxLTV)
    dfrisk['ust_loan'] = round(dfrisk['ust_loan'],2)
    risk_rating_list = get_scale_dic(collateral_loan_ratio)
    dfrisk['risk_rating'] = [(x < risk_rating_list[0] and 'A') 
                       or (risk_rating_list[0] <= x < risk_rating_list[1] and 'B+') 
                       or (risk_rating_list[1] <= x < risk_rating_list[2] and 'B') 
                       or (risk_rating_list[2] <= x < risk_rating_list[3] and 'B-') 
                       or (risk_rating_list[3] <= x < risk_rating_list[4] and 'C') 
                       or (risk_rating_list[4] <= x < risk_rating_list[5] and 'D') 
                       or (risk_rating_list[5] <=x and 'liquidation') for x in dfrisk['risk_ratio']]

    dfrisk['percent_bETH'] = (100*dfrisk['bETHcollateral_USD']
                                  /(dfrisk['bETHcollateral_USD'] + dfrisk['bLunacollateral_USD']))

    return dfrisk.query('bETHcollateral > 0').sort_values(by = 'risk_ratio', ascending = False) 

def get_distr(data):
    """This function calculates and returns a pivot table by risk levels"""    
    risk_distr =  data.pivot_table(index = 'risk_rating', values = ['bETHcollateral'], aggfunc = ['sum', 'count'])
    risk_distr.columns = ['bETH','cnt']

    risk_distr['percent'] = (risk_distr['bETH']/risk_distr['bETH'].sum())*100
    risk_distr['average'] = risk_distr['bETH']/risk_distr['cnt']

    median_a0 = data.query('risk_rating == "A"')['bETHcollateral'].median()
    data.loc[data['risk_rating']=='A','median'] = median_a0
    median_b0 = data.query('risk_rating == "B+"')['bETHcollateral'].median()
    data.loc[data['risk_rating']=='B+','median'] = median_b0
    median_b1 = data.query('risk_rating == "B"')['bETHcollateral'].median()
    data.loc[data['risk_rating']=='B','median'] = median_b1
    median_b2 = data.query('risk_rating == "B-"')['bETHcollateral'].median()
    data.loc[data['risk_rating']=='B-','median'] = median_b2
    median_c0 = data.query('risk_rating == "C"')['bETHcollateral'].median()
    data.loc[data['risk_rating']=='C','median'] = median_c0
    median_d0 = data.query('risk_rating == "D"')['bETHcollateral'].median()
    data.loc[data['risk_rating']=='D','median'] = median_d0
    median_il = data.query('risk_rating == "is liquidating"')['bETHcollateral'].median()
    data.loc[data['risk_rating']=='liquidation','median'] = median_il

    median_distr =  data.pivot_table(index = 'risk_rating', values = ['median'], aggfunc = 'min')

    risk_distr = risk_distr.merge(median_distr, on = 'risk_rating', how = 'outer') 

    return risk_distr.reindex(['A','B+','B','B-','C','D','liquidation']).fillna(0)


def get_change_price_step(df,risk_distr, i, j, collateral_loan_ratio):
    """This function calculates risks with a single step price change """
    beth_price = df.bETHcollateral_USD.sum()/df.bETHcollateral.sum()  
    bluna_price = df.bLunacollateral_USD.sum()/df.bLunacollateral.sum()   
    df[f'bETH_{i}_{j}'] = df['bETHcollateral']*(beth_price - beth_price*(i/100))
    df[f'bLuna_{i}_{j}'] = df['bLunacollateral']*(bluna_price - bluna_price*(j/100))
    df[f'Loan_risk_{i}_{j}'] = 100*df['ust_loan']/((df[f'bLuna_{i}_{j}'] + df[f'bETH_{i}_{j}'])*maxLTV)
    risk_rating_list = get_scale_dic(collateral_loan_ratio)
    df['risk_rating'] = [(x < risk_rating_list[0] and 'A') 
                       or (risk_rating_list[0] <= x < risk_rating_list[1] and 'B+') 
                       or (risk_rating_list[1] <= x < risk_rating_list[2] and 'B') 
                       or (risk_rating_list[2] <= x < risk_rating_list[3] and 'B-') 
                       or (risk_rating_list[3] <= x < risk_rating_list[4] and 'C') 
                       or (risk_rating_list[4] <= x < risk_rating_list[5] and 'D') 
                       or (risk_rating_list[5] <=x and 'liquidation') for x in df[f'Loan_risk_{i}_{j}']]
    risk_distr_amount =  df.pivot_table(index = 'risk_rating', values = ['bETHcollateral'], aggfunc = ['sum'])
    risk_distr_amount[f'a_{i}_{j}'] = risk_distr_amount[('sum', 'bETHcollateral')]
    risk_distr_count =  df.pivot_table(index = 'risk_rating', values = ['bETHcollateral'], aggfunc = ['count'])
    risk_distr_count[f'c_{i}_{j}'] = risk_distr_count[('count', 'bETHcollateral')]
    risk_distr_percent =  df.pivot_table(index = 'risk_rating', values = ['bETHcollateral'], aggfunc = ['sum'])
    risk_distr_percent[f'a_{i}_{j}'] = risk_distr_percent[('sum', 'bETHcollateral')]
    risk_distr_percent[f'p_{i}_{j}'] = 100*(risk_distr_percent[f'a_{i}_{j}']/risk_distr_percent[f'a_{i}_{j}'].sum())
    
    return risk_distr_amount[f'a_{i}_{j}'].to_frame(),risk_distr_count[f'c_{i}_{j}'].to_frame(), risk_distr_percent[f'p_{i}_{j}'].to_frame()

def get_change_price_interval(df, risk_distr, interval_end, step, coef_dep, collateral_loan_ratio):
    """This function calculates risks with price change into an interval"""
    risk_distr_step_amount = risk_distr[['bETH']]
    risk_distr_step_count = risk_distr[['cnt']]
    risk_distr_step_percent = risk_distr[['percent']]

    for beth_step in range(1,interval_end + 1, step): #beth_price change
        bLuna_step = beth_step*coef_dep
        risk_distr_step_amount_ = get_change_price_step(df,risk_distr_step_amount, beth_step, bLuna_step, collateral_loan_ratio)[0]
        risk_distr_step_count_ = get_change_price_step(df,risk_distr_step_count, beth_step, bLuna_step, collateral_loan_ratio)[1]
        risk_distr_step_percent_ = get_change_price_step(df,risk_distr_step_percent, beth_step, bLuna_step,collateral_loan_ratio)[2]
        risk_distr_step_amount = risk_distr_step_amount.merge(risk_distr_step_amount_, on = 'risk_rating', how = 'outer')  
        risk_distr_step_count = risk_distr_step_count.merge(risk_distr_step_count_, on = 'risk_rating', how = 'outer')
        risk_distr_step_percent = risk_distr_step_percent.merge(risk_distr_step_percent_, on = 'risk_rating', how = 'outer')
    risk_distr_step_amount = risk_distr_step_amount.drop(risk_distr_step_amount.columns[[0]], axis=1)
    risk_distr_step_count = risk_distr_step_count.drop(risk_distr_step_count.columns[[0]], axis=1)
    risk_distr_step_percent = risk_distr_step_percent.drop(risk_distr_step_percent.columns[[0]], axis=1)
    
    return risk_distr_step_amount.fillna(0),risk_distr_step_count.fillna(0),risk_distr_step_percent.fillna(0)

def plot_cde(dfresult):    
    """This function builds and returns the charts for structure of risk""" 
    risk_cde = dfresult.loc[['C','D', 'liquidation']]    
    risk_cde.loc['C+D+liquidation'] = risk_cde.sum(axis=0)
    risk_cde.loc['D+liquidation'] = risk_cde.loc[['D', 'liquidation']].sum(axis=0)
        
    risk_cde = risk_cde.T
    risk_cde = risk_cde.fillna(0)
    
    rsize = risk_cde['D'].size + 1
    s1 = pd.Series(range(1, rsize))
    s1.index = risk_cde.index  
    
    risk_cde["X"] = s1 
    risk_cde['X'] = risk_cde['X'].fillna(0)

    return risk_cde.plot(x="X", y=["D+liquidation","liquidation","C+D+liquidation"], figsize = (15,5)) 


def load_prices():
    df = pd.concat([
        pd.read_csv('price1.csv', parse_dates = ['BLOCK_TIMESTAMP']),
        pd.read_csv('price2.csv',  parse_dates = ['BLOCK_TIMESTAMP']),
        pd.read_csv('price3.csv',  parse_dates = ['BLOCK_TIMESTAMP']),
        pd.read_csv('price4.csv',  parse_dates = ['BLOCK_TIMESTAMP'])
    ])
    df.columns= ['block','timestamp','bLuna','bETH']
    df = df[['timestamp','bLuna','bETH']].sort_values(by ='timestamp')
    df = df.pivot_table(index='timestamp', values = ['bLuna','bETH'], aggfunc = 'mean')
    df = df.dropna()
    return df

def get_daily_data():
    df = load_prices()
    df['date'] = [d.date() for d in df.index]
    return df

def get_hourly_data():
    df = load_prices()
    df['hourly']= [datetime.datetime(t.year, t.month, t.day, t.hour) for t in df.index]
    return df

def get_corr_analysis(data1,data2, df):
    sns.scatterplot(x=data1, y=data2, data=df)
    corr, _ = pearsonr(df[data1], df[data2])
    print('Pearsons correlation: %.3f' % corr)