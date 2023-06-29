
#то что ниже обязательно заполнить своими данными
proxy_use = 0 #  0 - не использовать, 1 - прокси без ссылки , 2 - прокси со ссылкой для смены ip
proxy_login = 'pfds464'
proxy_password = '9c3a07'
proxy_address = 'no.com'
proxy_port = '157'
proxy_changeIPlink = "http:/5cce3b204"


#то что ниже желательно настроить под себя
networks_from = ['polygon', 'bsc']  # выберите сети откуда посылаем сообщение
networks_bsc_to = ['polygon', 'nova', 'moonbeam']  # выберите сети куда , если из БСК
networks_polygon_to = ['nova', 'fantom']  # выберите сети куда если из полигона



#укажите паузу в работе между кошельками, минимальную и максимальную. 
#При смене каждого кошелька будет выбрано случайное число. Значения указываются в секундах
timeoutMin = 10 #минимальная 
timeoutMax = 30 #максимальная
#задержки между операциями в рамках одного кошелька
timeoutTehMin = 3 #минимальная 
timeoutTehMax = 10 #максимальная



#то что ниже можно менять только если понимаешь что делаешь
proxies = { 'all': f'http://{proxy_login}:{proxy_password}@{proxy_address}:{proxy_port}',}
if proxy_use:
    request_kwargs = {"proxies":proxies, "timeout": 120}
else:
    request_kwargs = {"timeout": 120}
gas_kef=1.5 #коэфициент допустимого расхода газа на подписание транзакций. можно выставлять от 1.3 до 2

rpc_links = {
    'polygon': 'https://polygon-rpc.com/',
    'arbitrum': 'https://arb1.arbitrum.io/rpc',
    'optimism':  'https://rpc.ankr.com/optimism',
    'bsc': 'https://bscrpc.com',
    'fantom': 'https://rpc.ftm.tools/',
    'avax': 'https://api.avax.network/ext/bc/C/rpc',
    'nova': 'https://nova.arbitrum.io/rpc',
    'moonbeam': 'https://rpc.api.moonbeam.network',
}


#то что ниже - поддерживать в актуальном состоянии
prices = {
    "MATIC": 0.645,
    "AVAX": 11.8,
    "BNB": 246,
    "ETH": 1900,
}



