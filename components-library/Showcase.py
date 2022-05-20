import cosmos.cosmosGeneral as cosmos
import ethereum.ethereumGeneral as ethereum
import polkadot.polkadotGeneral as polkadot
import polygon.polygonGeneral as polygon
import solana.solanaGeneral as solana
import ethereum.tokens.ethereumGeneralTokens as eth_token
import ethereum.validators.ethereumGeneralValidators as eth_validators

cosmos = cosmos.connect_to_cosmos('https://api.cosmos.network')
ethereum = ethereum.connect_to_ethereum('https://eth-mainnet.blastapi.io/0f7cf334-b525-440d-bb75-7393628d8165')
polkadot = polkadot.connect_to_moonriver('https://moonriver.api.onfinality.io/rpc?apikey=7317794a-740c-4fc7-a3c8-db10d40b0ab2')
polygon = polygon.connect_to_polygon('https://polygon-rpc.com')
solana = solana.connect_to_solana('https://api.mainnet-beta.solana.com')


print(cosmos.get_latest_block())
print(ethereum.get_latest_block())
print(polkadot.get_latest_block())
print(polygon.get_latest_block())
print(solana.get_latest_block())

eth_token=eth_token.eth_token('https://eth-mainnet.blastapi.io/0f7cf334-b525-440d-bb75-7393628d8165')
eth_token.get_token_holders('0xae7ab96520DE3A18E5e111B5EaAb095312D7fE84')

validator= eth_validators.eth_validator('https://eth-mainnet.blastapi.io/0f7cf334-b525-440d-bb75-7393628d8165')
print(validator.get_validator_info_by_index(11231))