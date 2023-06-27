# global settings used by the app
# you will need to add a text file named 'CMCApiKey.txt' to the root folder that contains your production API Key

# import all necessary libraries and files

import pathlib

# everything will be based of this parent path:
absolute_path = str(pathlib.Path(__file__).parent.resolve()) # this is wherever THIS file is.

# relative paths
log_path = '/logs/'
db_path = '/db/'

# files
db_prefix = 'bitmo-01'
API_key_file_name = '/' + 'CMCApiKey.txt'

# Coin Market Cap API Environment (comment out the one you do not want and the rest of the script will set the correct values)

# TODO, add a choice as user input, when first starting the program as to the environment type.

#environment = 'offline'
environment = 'sandbox'
#environment = 'production'

environment_choice = 0

while not ((environment_choice == 1) or (environment_choice == 2) or (environment_choice == 3) or (environment_choice == 4)):

    print('Select your environment: ' + '\n' + 
          '1: Production' + '\n' +
          '2: Sandbox' + '\n' +
          '3: Offline' + '\n' + 
          '4: use config.py setting')

    environment_choice = input()

    try:
        environment_choice = int(environment_choice)

    except:
        print

if (environment_choice == 1):
    environment = 'production'
elif (environment_choice == 2):
    environment = 'sandbox'
elif (environment_choice == 3):
    environment = 'offline'

# make only 1 call to the API to get 1 set of data or loop through all the records to get EACH currency
# 0 = just once (some)
# 1 = ALL
all_or_some = 1

parameters = {
  'start':'1', # 1 is default so I don't believe this is needed.
  'limit':'5000', # how many currencies do you want returned. (max is 5000)
  'convert':'USD' # comma separated list of what currency bases you'd like these returned in. ('USD,CAD,JPY,')
}

if (environment == 'sandbox' or environment == 'offline'):
    db_name = db_prefix + '-sandbox.db'
    cmc_environment = {
        'environment': environment,
        'url': 'https://sandbox-api.coinmarketcap.com/v1/cryptocurrency/listings/latest',
        'APIkey': 'b54bcf4d-1bca-4e8e-9a24-22ff2c3d462c'
    }
elif (environment == 'production'):
    db_name = db_prefix + '-prod.db'
    # get the API key from the file
    key_location = absolute_path + API_key_file_name
    try:
        with open(key_location) as f:
            production_API_key = f.read()
    except:
        print('ERROR: Error reading CMC Api Key from file. Does the API Key file exist and is in the correct place?')
        exit() # exit the program if we cannot read the API key.
    cmc_environment = {
        'environment': environment,
        'url': 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest',
        'APIkey': production_API_key
    }

# this offline data is a copy from a sandbox API call
offline_data = {'status': {'timestamp': '2023-05-20T02:56:26.421Z', 'error_code': 0, 'error_message': None, 'elapsed': 1, 'credit_count': 1, 'notice': None}, 'data': [{'id': 537, 'name': 'zssxypanld', 'symbol': '3faq0fff5g3', 'slug': '2qi2dhviqdn', 'cmc_rank': 1152, 'num_market_pairs': 9012, 'circulating_supply': 4524, 'total_supply': 9586, 'max_supply': 5287, 'infinite_supply': None, 'last_updated': '2023-05-20T02:56:26.421Z', 'date_added': '2023-05-20T02:56:26.421Z', 'tags': ['hr0rvvccb37', '3venr3kyqlq', 'owh869tvo5', 'jrempnoviv', 'yhhsomvf9u', 'xhtjp8b3v9a', '3c0i8k8sykr', 'id3280wuaq', 'plr7zg3wqkh', '6outc6iwvtm'], 'platform': None, 'self_reported_circulating_supply': None, 'self_reported_market_cap': None, 'quote': {'USD': {'price': 0.7626970772131221, 'volume_24h': 9671, 'volume_change_24h': 0.809932229815516, 'percent_change_1h': 0.1317460655670688, 'percent_change_24h': 0.7846445023090705, 'percent_change_7d': 0.5482650274625924, 'market_cap': 0.18427627331759444, 'market_cap_dominance': 4746, 'fully_diluted_market_cap': 0.15154259679923632, 'last_updated': '2023-05-20T02:56:26.421Z'}}}, {'id': 437, 'name': 'vsjsfpo8iej', 'symbol': 'who7ydqh8z', 'slug': 'cmtwiepoh3o', 'cmc_rank': 5731, 'num_market_pairs': 8235, 'circulating_supply': 7898, 'total_supply': 8526, 'max_supply': 6743, 'infinite_supply': None, 'last_updated': '2023-05-20T02:56:26.421Z', 'date_added': '2023-05-20T02:56:26.421Z', 'tags': ['vbbhysh81ue', 'h17y65ifiig', 'c8mmo0r61l7', '6l4hm21e72r', 'r3asyvk5u8', 'wkz56hmqpvs', '78idt80vu4w', 'lfpah9afwnk', 'dq6a3url6ug', 'bvj1v7to5y8'], 'platform': None, 'self_reported_circulating_supply': None, 'self_reported_market_cap': None, 'quote': {'USD': {'price': 0.6600069539130193, 'volume_24h': 4161, 'volume_change_24h': 0.27858954907752476, 'percent_change_1h': 0.32887214137639487, 'percent_change_24h': 0.8729957100549637, 'percent_change_7d': 0.1179768543218942, 'market_cap': 0.17998694598806098, 'market_cap_dominance': 3122, 'fully_diluted_market_cap': 0.03340714120356192, 'last_updated': '2023-05-20T02:56:26.421Z'}}}, {'id': 896, 'name': 'ysu7zm1bt2g', 'symbol': 'v9kfiuwbw3', 'slug': 'qhbkevxtmyj', 'cmc_rank': 6741, 'num_market_pairs': 2416, 'circulating_supply': 5216, 'total_supply': 2100, 'max_supply': 5527, 'infinite_supply': None, 'last_updated': '2023-05-20T02:56:26.421Z', 'date_added': '2023-05-20T02:56:26.421Z', 'tags': ['s150zkh1wi', 'zd3ngtb1hfh', 'tuxxutehbc', 'gw2q3y3hmt6', 'plr4rv9m9j', '43v2wfsvr6f', 'yjyezzoktrb', 'zrl5fbobpyl', 'ffjrrpyb2e', 'cd8id8rus4i'], 'platform': None, 'self_reported_circulating_supply': None, 'self_reported_market_cap': None, 'quote': {'USD': {'price': 0.8394899278183376, 'volume_24h': 1744, 'volume_change_24h': 0.08859597746924264, 'percent_change_1h': 0.6279626613509826, 'percent_change_24h': 0.9554245783856419, 'percent_change_7d': 0.8004149909598408, 'market_cap': 0.016303090548090537, 'market_cap_dominance': 3340, 'fully_diluted_market_cap': 0.6624295677868448, 'last_updated': '2023-05-20T02:56:26.421Z'}}}, {'id': 8002, 'name': 'wgcnzxpuno', 'symbol': 'w4xww9t8ao', 'slug': 'ffklkzsfmhg', 'cmc_rank': 4142, 'num_market_pairs': 4281, 'circulating_supply': 1558, 'total_supply': 7190, 'max_supply': 1439, 'infinite_supply': None, 'last_updated': '2023-05-20T02:56:26.421Z', 'date_added': '2023-05-20T02:56:26.421Z', 'tags': ['phemmqofa5', 'xgvybgjl0ac', 'odunkminrj', '7h22s51pe2', '4oi0g2elnp6', 'ixciuz1y8yr', 'gqzkkg0u1uw', '2kquqwmof1o', 'ddrz2mdfog', '8wnvt8ewuc6'], 'platform': None, 'self_reported_circulating_supply': None, 'self_reported_market_cap': None, 'quote': {'USD': {'price': 0.7510380298936488, 'volume_24h': 2471, 'volume_change_24h': 0.9009840608910284, 'percent_change_1h': 0.6709170873990589, 'percent_change_24h': 0.33259786305069716, 'percent_change_7d': 0.5155808316076167, 'market_cap': 0.9279741325151885, 'market_cap_dominance': 2694, 'fully_diluted_market_cap': 0.5110910141960037, 'last_updated': '2023-05-20T02:56:26.421Z'}}}, {'id': 5044, 'name': 'y55b58ynz6', 'symbol': 'a020qud1pz6', 'slug': 'dq0co9fnewj', 'cmc_rank': 9322, 'num_market_pairs': 7068, 'circulating_supply': 8708, 'total_supply': 4093, 'max_supply': 6543, 'infinite_supply': None, 'last_updated': '2023-05-20T02:56:26.421Z', 'date_added': '2023-05-20T02:56:26.421Z', 'tags': ['00j1qh2lni41j', 'l97ck4245ci', 'ejwvlu64wcw', 'bl9v2g20m0n', '4p0k2jn6cgb', 'mwiuycecrhj', '7dcbp8061vb', 'jbcxg8oslb', 'tftvgum0u7', 'jblfqgvpl6'], 'platform': None, 'self_reported_circulating_supply': None, 'self_reported_market_cap': None, 'quote': {'USD': {'price': 0.44301261442701234, 'volume_24h': 1355, 'volume_change_24h': 0.8396437788464013, 'percent_change_1h': 0.8847035272725103, 'percent_change_24h': 0.9771119126472794, 'percent_change_7d': 0.9834034310764563, 'market_cap': 0.9427050280816007, 'market_cap_dominance': 8796, 'fully_diluted_market_cap': 0.4004477816154748, 'last_updated': '2023-05-20T02:56:26.421Z'}}}, {'id': 8358, 'name': '1dhokwaswmh', 'symbol': 'gigzadrrspp', 'slug': 'thtwudarsi', 'cmc_rank': 6728, 'num_market_pairs': 4445, 'circulating_supply': 4749, 'total_supply': 8095, 'max_supply': 7157, 'infinite_supply': None, 'last_updated': '2023-05-20T02:56:26.421Z', 'date_added': '2023-05-20T02:56:26.421Z', 'tags': ['s27klp77b6k', 'wygmltgbeda', '66gj6gzyl3y', '3mbpgvnes1h', 'yqzo5vanj2', 'wmqdcf8xguk', 'qwr5zbuclh', 'br4pwmsa1t', '982wjp4no4', '7xheqdg65ql'], 'platform': None, 'self_reported_circulating_supply': None, 'self_reported_market_cap': None, 'quote': {'USD': {'price': 0.5979353044797635, 'volume_24h': 6335, 'volume_change_24h': 0.14460684276646618, 'percent_change_1h': 0.29284367611217177, 'percent_change_24h': 0.2126502215454662, 'percent_change_7d': 0.6146681168414618, 'market_cap': 0.558063167132236, 'market_cap_dominance': 5797, 'fully_diluted_market_cap': 0.601166071056946, 'last_updated': '2023-05-20T02:56:26.421Z'}}}, {'id': 6685, 'name': 'yd9n9gm8u9', 'symbol': '1hfhd7z3d74', 'slug': 'u5g4v1a6ap', 'cmc_rank': 5426, 'num_market_pairs': 5373, 'circulating_supply': 2810, 'total_supply': 3477, 'max_supply': 3279, 'infinite_supply': None, 'last_updated': '2023-05-20T02:56:26.421Z', 'date_added': '2023-05-20T02:56:26.421Z', 'tags': ['zz5qd1xrhbk', 'hbnvle7ua6b', '3mzmzszjzu', '3gk96sajqn6', '3o49qvj9v7y', 'fiizp7ypdta', 'm15nrg24sh', 'oj3mxcam4', 'h7lv5k8k3ht', 'ltovxg558q'], 'platform': None, 'self_reported_circulating_supply': None, 'self_reported_market_cap': None, 'quote': {'USD': {'price': 0.8136490812135184, 'volume_24h': 6253, 'volume_change_24h': 0.4518038052897686, 'percent_change_1h': 0.5899433217625514, 'percent_change_24h': 0.9668564885732198, 'percent_change_7d': 0.6510809390608994, 'market_cap': 0.3565489102187982, 'market_cap_dominance': 7413, 'fully_diluted_market_cap': 0.7180425307337923, 'last_updated': '2023-05-20T02:56:26.421Z'}}}, {'id': 7084, 'name': 'p72gglw4nnl', 'symbol': 'qfh9jwf90dg', 'slug': 'dkr8b6l4qg8', 'cmc_rank': 9011, 'num_market_pairs': 9884, 'circulating_supply': 5566, 'total_supply': 4419, 'max_supply': 9158, 'infinite_supply': None, 'last_updated': '2023-05-20T02:56:26.421Z', 'date_added': '2023-05-20T02:56:26.421Z', 'tags': ['zszun38e1g', 'y83kdi2x28', 'nfe6qw43a1m', 'owfwbzkp2o', 'a9r45hrcs24', 'cyblrj4rkae', 'c2rkyl7ekae', 'coglhjurbd', '3bcv34rbaki', 'z8muxxxv5wg'], 'platform': None, 'self_reported_circulating_supply': None, 'self_reported_market_cap': None, 'quote': {'USD': {'price': 0.6216617162260505, 'volume_24h': 1703, 'volume_change_24h': 0.9007481719220787, 'percent_change_1h': 0.009786464069286849, 'percent_change_24h': 0.4534758999957238, 'percent_change_7d': 0.8051069642185993, 'market_cap': 0.08246918724293706, 'market_cap_dominance': 3701, 'fully_diluted_market_cap': 0.18304781848741936, 'last_updated': '2023-05-20T02:56:26.421Z'}}}, {'id': 5494, 'name': 'erhwnvhzgo8', 'symbol': 'osz5r6oid0q', 'slug': '3bx9np852no', 'cmc_rank': 330, 'num_market_pairs': 2806, 'circulating_supply': 5997, 'total_supply': 7340, 'max_supply': 6224, 'infinite_supply': None, 'last_updated': '2023-05-20T02:56:26.421Z', 'date_added': '2023-05-20T02:56:26.421Z', 'tags': ['myi0mijw68', 'b15iqw5fpkq', 'gktjav4k28e', 'zqcamwm0lws', 'khjn40zzesa', 'f0uwzqszgm', 'uyl2ngqdrop', 'ou40r4g6hha', '02fon8bejqhl', 'g4ogchzplpv'], 'platform': None, 'self_reported_circulating_supply': None, 'self_reported_market_cap': None, 'quote': {'USD': {'price': 0.5248030370891412, 'volume_24h': 4132, 'volume_change_24h': 0.5176921389477926, 'percent_change_1h': 0.9190815715250791, 'percent_change_24h': 0.6877775042622625, 'percent_change_7d': 0.055275956860872055, 'market_cap': 0.2103921826503885, 'market_cap_dominance': 2910, 'fully_diluted_market_cap': 0.09378449961915081, 'last_updated': '2023-05-20T02:56:26.421Z'}}}, {'id': 2402, 'name': 'ekv2bsdyq2j', 'symbol': 'fm7wgcpnsa4', 'slug': 'oc6922c3j3i', 'cmc_rank': 5016, 'num_market_pairs': 3814, 'circulating_supply': 2304, 'total_supply': 944, 'max_supply': 7809, 'infinite_supply': None, 'last_updated': '2023-05-20T02:56:26.421Z', 'date_added': '2023-05-20T02:56:26.421Z', 'tags': ['wjiuak1whtq', 'oe3jnhibsmq', 'gmgbtnd397e', 'ykcuqxxldx', 'xg1gv78n4ql', '921m9ar8z1d', 'blg5zw3iobu', 'liugq1k9kna', 'ntrypog2py', '7aqouxouxna'], 'platform': None, 'self_reported_circulating_supply': None, 'self_reported_market_cap': None, 'quote': {'USD': {'price': 0.5298370258726357, 'volume_24h': 2132, 'volume_change_24h': 0.5571739969631708, 'percent_change_1h': 0.12970955345088298, 'percent_change_24h': 0.6443666272738298, 'percent_change_7d': 0.7683914012534203, 'market_cap': 0.7099141878946196, 'market_cap_dominance': 4889, 'fully_diluted_market_cap': 0.4614038162546492, 'last_updated': '2023-05-20T02:56:26.421Z'}}}]}