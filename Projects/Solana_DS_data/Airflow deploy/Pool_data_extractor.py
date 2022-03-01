import requests
import pandas as pd

http_client='https://aged-aged-sun.solana-mainnet.quiknode.pro/a0cfa150fb95f8e69756a99a9a0bdf5755bc2bad/'
pools_list=['2m9ZT6smigrmNKxSRe7to6HnYGMYTztsDiuoJM4k336j','5sjkv6HD8wycocJ4tC4U36HHbvgcXYqcyiPRUkncnwWs','6a1CsrpeZubDjEJE9s1CMVheB6HWM5d7m1cj2jkhyXhj',
                '9bCjWxNQ2WQFuQzsV7g5S3m8qCQ8ub6pd13nWUoXz2eh','9euZD3C1d7e2fLKnUxHc7oUUDJcYnguMT6cRzLY9y4o7','9F3J6RY7PTkDb3SUUpg725uXyCceBGCpZrtmYGJwgMwF',
                '85pJTrAVdjHNvgCcUtefwkSe9RDKnHueyvs2uTocWmWs','B32UuhPSp6srSBbRTh4qZNjkegsehY9qXTwQgnPWYMZy',
                'BcDSFjLGyZZdfyaU59PrKofogWXMByEx8sGF5pQs5eF1','BQ5PvBUWWio1A19yHAck1LJKRC2ewQaCcT4VRCQuVcUy','Br4WZq7N5gFK3WX8Ls1U15ePnQ1DnSKwx5k62X51LeLB',
                'CUQbwmFXySWXpBgycGTTj3gQNY8AnjD4DJRjgLeG1bVK','EfK84vYEKT1PoTJr6fBVKFbyA7ZoftfPo2LQPAJG1exL',
                'EufS4F27HudL7rc8mBSUJCSZHVPDPLMo51MAVbSUvKZV','F8caiu7pwDYaK6S1BUtuxB9d5hicn7bQV5SMt9zPzog','G4Bjsy5oYVQifvf8pRteX7Lk8YMe9EKf6BRhwGiCK76B',
                'Lid8SLUxQ9RmF7XMqUA8c24RitTwzja8VSKngJxRcUa','pG6noYMPVR9ykNgD4XSNa6paKKGGwciU2LckEQPDoSW']

def get_txn(signature):
    """This function  fetch transaction based on its signature"""
    headers = {'Content-type': 'application/json'}
    data = '{"jsonrpc": "2.0","id": 1,"method": "getTransaction","params": ["'+signature+'"]}'
    response = requests.post(http_client, headers=headers, data=data)
    return response.json()['result']

def get_all_signatures(address):
    """This function fetch all transaction sugnature based on address (note that signature is not full transaction info, it is just
    address via which you could get info about transaction) """
    all_signatures = []
    headers = {'Content-type': 'application/json'}
    first_data = '{"jsonrpc": "2.0","id": 1,"method": "getSignaturesForAddress","params": ["' + address + '"]}'
    first_responce = requests.post(http_client, headers=headers, data=first_data)
    all_signatures += first_responce.json()['result']
    support_cycle_responce = first_responce.json()['result']
    try:
        while len(support_cycle_responce) == 1000 or len(support_cycle_responce)==0:
            last_txn = support_cycle_responce[-1]['signature']
            cycle_data = '{"jsonrpc": "2.0","id": 1,"method": "getSignaturesForAddress","params": ["' + address + '",{"before":"' + last_txn + '"}]}'
            cycle_responce = requests.post(http_client, headers=headers, data=cycle_data)
            all_signatures += cycle_responce.json()['result']
            support_cycle_responce = cycle_responce.json()['result']

    except KeyError:
        print(cycle_responce.json())

    return all_signatures


def get_all_signatures_until_certain(address, until):
    """This function fetch all transaction sugnature based on address (note that signature is not full transaction info, it is just
    address via which you could get info about transaction """
    all_signatures = []
    headers = {'Content-type': 'application/json'}
    first_data = '{"jsonrpc": "2.0","id": 1,"method": "getSignaturesForAddress","params": ["' + address + '"]}'
    first_responce = requests.post(http_client, headers=headers, data=first_data)
    all_signatures += first_responce.json()['result']
    support_cycle_responce = first_responce.json()['result']
    try:
        while len(support_cycle_responce) == 1000:
            last_txn = support_cycle_responce[-1]['signature']
            cycle_data = '{"jsonrpc": "2.0","id": 1,"method": "getSignaturesForAddress","params": ["' + address + '",{"before":"' + last_txn + '","until":"' + until + '"}]}'
            cycle_responce = requests.post(http_client, headers=headers, data=cycle_data)
            all_signatures += cycle_responce.json()['result']
            support_cycle_responce = cycle_responce.json()['result']
    except KeyError:
        print(cycle_responce.json())

    return all_signatures

def get_1000_signatures(address):
    """This function fetch 1000 transaction sugnature based on address (note that signature is not full transaction info, it is just
    address via which you could get info about transaction """
    headers = {'Content-type': 'application/json'}
    data = '{"jsonrpc": "2.0","id": 1,"method": "getSignaturesForAddress","params": ["'+address+'"]}'
    responce = requests.post(http_client, headers=headers, data=data)
    return responce.json()['result']

def get_changes(txn):
    """This function return dictionary with all balances change within one transaction"""
    post_token_balance = txn['meta']['postTokenBalances']
    pre_token_balance = txn['meta']['preTokenBalances']
    keys = txn['transaction']['message']['accountKeys']
    for x in range(len(post_token_balance)):
        post_token_balance[x]['token_account'] = keys[x]
        for y in range(len(pre_token_balance)):
            if post_token_balance[x]['accountIndex'] == pre_token_balance[y]['accountIndex']:
                change = float(post_token_balance[x]['uiTokenAmount']['uiAmountString']) - float(
                    pre_token_balance[y]['uiTokenAmount']['uiAmountString'])
                post_token_balance[x]['uiTokenAmount']['change'] = change
    post_balances = txn['meta']['postBalances']
    pre_balances = txn['meta']['preBalances']
    changes = [(int(post_balances[x]) - int(pre_balances[x])) / (10 ** 9) for x in range(len(post_balances))]
    sol_arr = []
    for x in range(len(changes)):
        if changes[x] != 0:
            row = {}
            row['accountIndex'] = x
            row['token_account'] = keys[x]
            row['mint'] = 'SOL'
            row['uiTokenAmount'] = {'uiAmountString': post_balances[x] / 10 ** 9, 'change': changes[x]}
            sol_arr.append(row)

    post_balance = post_token_balance + sol_arr

    return post_balance


def get_row(signature):
    """This function prepares row with following info: trasaction hash, blocktime as unix stamp, token account owner address,
     token account address, token address, current balance on token account, and how token balance wa changed withib one trasaction"""
    txn = get_txn(signature)
    txn_arr = []
    if txn !=None:
        keys = txn['transaction']['message']['accountKeys']
        post_balance = get_changes(txn)

        for x in range(len(post_balance)):
            row = {}
            row['transaction'] = txn['transaction']['signatures'][0]
            row['blocktime'] = txn['blockTime']
            row['token_acc'] = keys[post_balance[x]['accountIndex']]
            row['token'] = post_balance[x]['mint']
            row['balance'] = post_balance[x]['uiTokenAmount']['uiAmountString']
            if 'change' in post_balance[x]['uiTokenAmount'].keys():
                row['change'] = post_balance[x]['uiTokenAmount']['change']
            else:
                row['change'] = post_balance[x]['uiTokenAmount']['uiAmountString']
            txn_arr.append(row)


    return txn_arr



def final_table(address):
    """This function create table with info about all balance changes for every account """
    holders_list=get_all_signatures(address)
    final_table=[]
    print(f'Fetched total {len(holders_list)} txns')
    for x in range(0,len(holders_list),1):
        all_txns=get_row(holders_list[x]['signature'])
        final_table += all_txns
        if x%100 == 0:
            print(f'{x} txns done')

    return final_table


def update_txns_pools(address,until):
    """This function create table with info about all balance changes for every account """
    holders_list = get_all_signatures_until_certain(address, until)
    update_table = []
    print(f'Fetched total {len(holders_list)} for {address}')
    for x in range(len(holders_list)):
        all_txns = get_row(holders_list[x]['signature'])
        update_table += all_txns
        if x % 1001 == 0:
            print(f'{x} txns done')

    update_df = pd.DataFrame(update_table)

    return update_df

def get_last_txn(pool_txns):
    pool_txns = pool_txns.sort_values(by='blocktime', ascending=True)
    last_txn=pool_txns.iloc[-1]['transaction']
    return last_txn

def update_last_txns():
    last_txn_arr = []
    for x in range(len(pools_list)):
        row = {}
        last_txn = get_1000_signatures(pools_list[x])[0]['signature']
        row['pool'] = pools_list[x]
        row['last_txn'] = last_txn
        last_txn_arr.append(row)
    last_txn_arr_df=pd.DataFrame(last_txn_arr)
    last_txn_arr_df.to_csv(f'last_txns.csv', sep=',', encoding='utf-8', index=False)
    return last_txn_arr

def update_pools(last_txns_file_name):
    pools_txns_df=pd.DataFrame(columns=['transaction', 'blocktime','token_acc','token','balance','change'])
    last_txns_df=pd.read_csv(last_txns_file_name)
    for x in range(len(pools_list)):
        last_txn=last_txns_df.iloc[x,1]
        update_df=update_txns_pools(pools_list[x],last_txn)
        pools_txns_df=pd.concat([pools_txns_df,last_txns_df])
        new_last_txn=get_last_txn(update_df)
        last_txns_df.iloc[x,1]=new_last_txn
    last_txns_df.to_csv(f'last_txns.csv', sep=',', encoding='utf-8', index=False)
    return  pools_txns_df

update_pools('last_txns.csv')

#todo:new pool adding flow