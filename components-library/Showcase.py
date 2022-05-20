import cosmos.cosmosGeneral as cosmos
import ethereum.ethereumGeneral as ethereum
import polkadot.polkadotGeneral as polkadot
import polygon.polygonGeneral as polygon
import solana.solanaGeneral as solana

cosmos = cosmos.connect_to_cosmos('https://api.cosmos.network')
ethereum = ethereum.connect_to_ethereum('https://eth-mainnet.blastapi.io/0f7cf334-b525-440d-bb75-7393628d8165')
polkadot = polkadot.connect_to_moonriver('https://moonriver.api.onfinality.io/rpc?apikey=7317794a-740c-4fc7-a3c8-db10d40b0ab2')
polygon = polygon.connect_to_polygon('https://polygon-rpc.com')
solana = solana.connect_to_solana('https://api.mainnet-beta.solana.com')
