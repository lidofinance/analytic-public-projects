import requests
import pandas as pd
import matplotlib as plt
pd.options.display.float_format = '{:,.2f}'.format

def get_general_info():
    headers = {'Content-type': 'application/json'}
    largest_accs = '{"jsonrpc": "2.0","id": 1,"method": "getTokenLargestAccounts","params": ["7dHbWXmci3dT8UFYWYZweBLXgycu7Y3iL6trKn1Y7ARj"]}'
    largest_accs_response = requests.post('https://api.mainnet-beta.solana.com', headers=headers, data=largest_accs)
    accs = largest_accs_response.json()
    stSOL_supply = '{"jsonrpc": "2.0","id": 1,"method": "getTokenSupply","params": ["7dHbWXmci3dT8UFYWYZweBLXgycu7Y3iL6trKn1Y7ARj"]}'
    stSOL_supply_responce = requests.post('https://api.mainnet-beta.solana.com', headers=headers, data=stSOL_supply)
    supply = stSOL_supply_responce.json()

    accounts_match = [
        {'token_acc': 'F9kWLTs28mWKmmvKDhAvtHuVwYKx6L4yG7C3n4WyLVh6', 'name': 'P2P stake authority account',
         'owner': 'Dkx85wVaUaDy9i9XWFdZvYrw5h2WMP1N8TqXPBdXY5Wh'},
        {'token_acc': '4PgzyzLtds9bKZ2to9PMnKqJzKEUpjvNUaeN23phegax', 'name': 'Saber stSOL/wSOL pool',
         'owner': '8eyi347MTDeH5F6eVv2qjPxVnU685FFZLDGcj5QWHZ6y'},
        {'token_acc': 'FqLtqRJvoVNYU5Xpcgp5FNPv8cXCZw7CiNddjQ4nqkRo', 'name': 'Mercurial stSOL/SOL pool',
         'owner': 'pG6noYMPVR9ykNgD4XSNa6paKKGGwciU2LckEQPDoSW'},
        {'token_acc': 'CeSEpgqc3zV8xDr7Q6PiwJju6a6e92wpAv7Kg6QyFfQB', 'name': 'Orca stSOL/wstETH pool',
         'owner': 'EtwQJxu8wih29vMpdTa74K9W9tgtL4LT6hbWBkhHwvU5'},
        {'token_acc': 'BwxarsHS9y6MB7hJq4Xhgm99ma3wqkjUwuxYbm6m9MEX', 'name': 'Radium stSOL/USDC pool (not sure)',
         'owner': 'EtducGnLSftGewA6pn4g48rBfdAU4XAoxZrTgpdY7GzR'},
        {'token_acc': '4gqecEySZu6SEgCNhBJm7cEn2TFqCMsMNoiyski5vMTD', 'name': 'Radium stSOL/USDC pool (not sure)',
         'owner': 'x1vRSsrhXkSn7xzJfu9mYP2i19SPqG1gjyj3vUWhim1'},
        {'token_acc': '55Q9uVyREQ48DiMJCKoJ5JmZSHtqnRPD4LbY7KtpBUyM', 'name': 'Party Parrot stSOL/PRT pool (not sure)',
         'owner': 'FR19vMeG5dQWJgposu8RLyBuxQMsfur7EKfM3zdPNAeN'},
        {'token_acc': 'DhePnJszhyhULHUJkJptFGfu74eJn1J3Wh1Rd3Dvq77M', 'name': 'Program, Solchicks 188 nft holder',
         'owner': '6AbmRzfaTEzhSPHg9dQKaX8HwgofmKAJwdLPzjcLT5Fh'},
        {'token_acc': 'Cr64ifTrqrun9oTuAT7yTWoyBjaiZHYpqG7NfRXg3mbQ', 'name': 'Program which marked as signer in many transaction, lot of NFT tokens',
         'owner': '6AbmRzfaTEzhSPHg9dQKaX8HwgofmKAJwdLPzjcLT5Fh'},
        {'token_acc': 'MYkNCXuH8FJ3vLk36NJoHaGXa9VVCSKmzgdTxRGad9W', 'name': 'Program which marked as signer in many transaction',
         'owner': '6AbmRzfaTEzhSPHg9dQKaX8HwgofmKAJwdLPzjcLT5Fh'}
    ]

    accounts = []
    for x in range(len(accs['result']['value'])):
        row = {}
        row['address'] = accs['result']['value'][x]['address']
        row['amount'] = int(accs['result']['value'][x]['amount']) / 10 ** 9
        row['prcnt_of_total'] = int(accs['result']['value'][x]['amount']) / int(
            supply['result']['value']['amount']) * 100
        for acc in range(len(accounts_match)):
            if accs['result']['value'][x]['address'] == accounts_match[acc]['token_acc']:
                row['details'] = accounts_match[acc]['name']
        accounts.append(row)
    largest_acc_table = pd.DataFrame(accounts)
    stSOL_price = \
    requests.get('https://api.coingecko.com/api/v3/simple/price?ids=lido-staked-sol&vs_currencies=usd').json()[
        'lido-staked-sol']['usd']
    print('Current stSOL supply is: {:.2f}'.format(int(supply['result']['value']['amount']) / (10 ** 9)))
    print('Current stSOL supply in usd is: {:.2f}'.format(
        int(supply['result']['value']['amount']) / (10 ** 9) * stSOL_price))
    return largest_acc_table

def saber_pool_info():
    prices=requests.get('https://api.coingecko.com/api/v3/simple/price?ids=lido-staked-sol%2Csolana%2Cwrapped-steth%2Cusd-coin%2Cparrot-protocol&vs_currencies=usd')
    headers = {'Content-type': 'application/json'}
    saber_WSOL_amnt = '{"jsonrpc": "2.0","id": 1,"method": "getTokenAccountBalance","params": ["AtymwxoVN9peZo7EXTcDz9jKVc4vRmisJKKrNfe3ewBa"]}'
    saber_WSOL_response = requests.post('https://api.mainnet-beta.solana.com', headers=headers, data=saber_WSOL_amnt)
    saber_stSOL_amnt='{"jsonrpc": "2.0","id": 2,"method": "getTokenAccountBalance","params": ["4PgzyzLtds9bKZ2to9PMnKqJzKEUpjvNUaeN23phegax"]}'
    saber_stSOL_response = requests.post('https://api.mainnet-beta.solana.com', headers=headers, data=saber_stSOL_amnt)
    saber_pool=[{'name':'wSOL','amount':saber_WSOL_response.json()['result']['value']['uiAmount'],'price':prices.json()['solana']['usd'],'denom_price':int(saber_WSOL_response.json()['result']['value']['uiAmount'])*int(prices.json()['solana']['usd'])},
               {'name':'stSOL','amount':saber_stSOL_response.json()['result']['value']['uiAmount'],'price':prices.json()['lido-staked-sol']['usd'],'denom_price':int(saber_stSOL_response.json()['result']['value']['uiAmount'])*int(prices.json()['lido-staked-sol']['usd'])}]
    return saber_pool

def print_saber_info():
    saber=pd.DataFrame(saber_pool_info())
    print(saber)
    print(saber.plot.pie(y='amount',figsize=(5, 5), labels=['wSOL','stSol'], explode=(0.01,0),autopct='%1.1f%%',title='Saber pool amount'))
    print(saber.plot.pie(y='denom_price', figsize=(5, 5), labels=['wSOL','stSol'], explode=(0.01,0),autopct='%1.1f%%', title='Saber pool amount in usd '))

def mercurial_pool_info():
    prices=requests.get('https://api.coingecko.com/api/v3/simple/price?ids=lido-staked-sol%2Csolana%2Cwrapped-steth%2Cusd-coin%2Cparrot-protocol&vs_currencies=usd')
    headers = {'Content-type': 'application/json'}
    mercurial_WSOL_amnt = '{"jsonrpc": "2.0","id": 1,"method": "getTokenAccountBalance","params": ["9gizzFG33czvcTzn5N4V23uunV6YR55UNW8ow6qNPoX3"]}'
    mercurial_WSOL_response = requests.post('https://api.mainnet-beta.solana.com', headers=headers, data= mercurial_WSOL_amnt)
    mercurial_stSOL_amnt='{"jsonrpc": "2.0","id": 2,"method": "getTokenAccountBalance","params": ["FqLtqRJvoVNYU5Xpcgp5FNPv8cXCZw7CiNddjQ4nqkRo"]}'
    mercurial_stSOL_response = requests.post('https://api.mainnet-beta.solana.com', headers=headers, data=mercurial_stSOL_amnt)
    mercurial_pool=[{'name':'wSOL','amount': mercurial_WSOL_response.json()['result']['value']['uiAmount'],'price':prices.json()['solana']['usd'],'denom_price':int(mercurial_WSOL_response.json()['result']['value']['uiAmount'])*int(prices.json()['solana']['usd'])},
               {'name':'stSOL','amount': mercurial_stSOL_response.json()['result']['value']['uiAmount'],'price':prices.json()['lido-staked-sol']['usd'],'denom_price':int(mercurial_stSOL_response.json()['result']['value']['uiAmount'])*int(prices.json()['lido-staked-sol']['usd'])}]
    return mercurial_pool


def print_mercurial_info():
    mercurial=pd.DataFrame(mercurial_pool_info())
    print(mercurial)
    print(mercurial.plot.pie(y='amount', figsize=(5, 5), labels=['wSOL','stSol'], explode=(0.01,0),autopct='%1.1f%%',title='Mercurial pool amount'))
    print(mercurial.plot.pie(y='denom_price', figsize=(5, 5), labels=['wSOL','stSol'], explode=(0.01,0),autopct='%1.1f%%', title='Mercurial pool amount in usd '))

def orca_pool_info():
    prices=requests.get('https://api.coingecko.com/api/v3/simple/price?ids=lido-staked-sol%2Csolana%2Cwrapped-steth%2Cusd-coin%2Cparrot-protocol&vs_currencies=usd')
    headers = {'Content-type': 'application/json'}
    orca_wstETH_amnt = '{"jsonrpc": "2.0","id": 1,"method": "getTokenAccountBalance","params": ["Fb3XpEJgghTURUGd1wphWr93ruX5egnesfdZtjWCxJFy"]}'
    orca_wstETH_response = requests.post('https://api.mainnet-beta.solana.com', headers=headers, data= orca_wstETH_amnt)
    orca_stSOL_amnt='{"jsonrpc": "2.0","id": 2,"method": "getTokenAccountBalance","params": ["CeSEpgqc3zV8xDr7Q6PiwJju6a6e92wpAv7Kg6QyFfQB"]}'
    orca_stSOL_response = requests.post('https://api.mainnet-beta.solana.com', headers=headers, data=orca_stSOL_amnt)
    orca_pool=[{'name':'wstETH','amount': orca_wstETH_response.json()['result']['value']['uiAmount'],'price':prices.json()['wrapped-steth']['usd'],'denom_price':int(orca_wstETH_response.json()['result']['value']['uiAmount'])*int(prices.json()['wrapped-steth']['usd'])},
               {'name':'stSOL','amount': orca_stSOL_response.json()['result']['value']['uiAmount'],'price':prices.json()['lido-staked-sol']['usd'],'denom_price':int(orca_stSOL_response.json()['result']['value']['uiAmount'])*int(prices.json()['lido-staked-sol']['usd'])}]
    return orca_pool

def print_orca_info():
    orca=pd.DataFrame(orca_pool_info())
    print(orca)
    print(orca.plot.pie(y='amount', figsize=(5, 5), labels=['wstETH','stSol'], explode=(0.01,0),autopct='%1.1f%%',title='Orca pool amount'))
    print(orca.plot.pie(y='denom_price', figsize=(5, 5), labels=['wstETH','stSol'], explode=(0.01,0),autopct='%1.1f%%', title='Orca pool amount in usd '))