import requests
import datetime
import pandas as pd

def get_last_available_day()->int:
    '''Retrun last available day for data fetching'''
    responce=requests.get('https://api.rated.network/v0/eth/validators/1/effectiveness?size=10')
    return responce.json()['data'][0]['day']


def get_validator_by_index(index,size)->list:
   '''Return list of dicts with all validator info based on its index'''
   link = f'https://api.rated.network/v0/eth/validators/{index}/effectiveness?size={size}'
   responce=requests.get(link)
   return responce.json()['data']


def get_validator_by_pubkey(pubkey,size)->list:
   '''Return list of dicts with all validator info based on its pubkey'''
   link = f'https://api.rated.network/v0/eth/validators/{pubkey}/effectiveness?size={size}'
   responce=requests.get(link)
   return responce.json()['data']


def get_validator_by_deposit_address(address,size)->list:
    '''Return list of dicts with all validator info based on its deposit address'''
    link = f'https://api.rated.network/v0/eth/operators/{address}/effectiveness?size={size}'
    responce = requests.get(link)
    return responce.json()['data']


def get_validators_info(address_list:list,type:str)->list:
    '''Return list of dicts of with all validators data passed based on
    list of indices, pubkeys or deposit addresses,'''
    validators_data=[]
    size=get_last_available_day()
    if type == 'pubkey':
        for key in range(len(address_list)):
            pubkey_data=get_validator_by_pubkey(address_list[key],size)
            validators_data += pubkey_data
            print(f'{key+1} out of {len(address_list)} done')
            return validators_data
    if type == 'index':
        for key in range(len(address_list)):
            index_data=get_validator_by_index(address_list[key],size)
            validators_data += index_data
            print(f'{key+1} out of {len(address_list)} done')
            return validators_data
    if type == 'deposit':
        for key in range(len(address_list)):
            deposit_data=get_validator_by_deposit_address(address_list[key],size)
            validators_data += deposit_data
            print(f'{key+1} out of {len(address_list)} done')
            return validators_data
    else:
        print('Please provide type as one of ["pubkey","index","deposit"]')
        return None



def create_date_df():
    '''Create list of dates with indexes starting from genesis up to current date '''
    daterange = pd.date_range('2020-12-04',datetime.date.today()- datetime.timedelta(days=1))
    index_list=list(range(1,get_last_available_day()+1))
    return daterange.to_series(index=index_list).reset_index(level=0).rename(columns={'index':'day',0:'date'})


def create_df_with_dates(validators_info:list):
    '''Convert validators info into dataframe and add dates to it'''
    validators_info_df=pd.DataFrame(validators_info)
    dates_df=create_date_df()
    validators_info_df = validators_info_df.merge(dates_df, how='inner', on='day')
    validators_info_df
    return validators_info_df


def get_validators_info_dataframe(address_list:list,type:str,csv:str=''):
    '''Take address list and their type as parametr and return DataFrame with all validators info with dates
      if optional parametr csv is passed also save it in csv file'''
    validator_info=get_validators_info(address_list,type)
    validator_info_df=create_df_with_dates(validator_info)
    if csv:
        validator_info_df.to_csv(csv,sep=',', encoding='utf-8', index=False)
    return validator_info_df


"""
Use function below to upload all data, pass list of indices, pubkeys or deposit adresses
specify what exatcly you passed in "type" parametr as one of ["pubkey","index","deposit"].
If you need to save result in csv also pass desired file name in format "file_name.csv" as csv parametr.
"""
get_validators_info_dataframe()

