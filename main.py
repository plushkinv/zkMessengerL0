import json
from statistics import mean
import time
from web3 import Web3
import requests
import random
from datetime import datetime
import config
import fun
from fun import log, save_wallet_to, address


current_datetime = datetime.now()
print(f"\n\n {current_datetime}")
print(f'============================================= Плюшкин Блог =============================================')
print(f'subscribe to : https://t.me/plushkin_blog \n============================================================================================================\n')


send_messadge_abi = json.load(open('abi/send_messadge_abi.json'))
keys_list = []
with open("private_keys.txt", "r") as f:
    for row in f:
        private_key = row.strip()
        if private_key:
            keys_list.append(private_key)

random.shuffle(keys_list)
i=0
for private_key in keys_list:
    i += 1
    if config.proxy_use == 2:
        while True:
            try:
                requests.get(url=config.proxy_changeIPlink)
                fun.timeOut("teh")
                result = requests.get(url="https://yadreno.com/checkip/", proxies=config.proxies)
                print(f'Ваш новый IP-адрес: {result.text}')
                break
            except Exception as error:
                print(' !!! Не смог подключиться через Proxy, повторяем через 2 минуты... ! Чтобы остановить программу нажмите CTRL+C или закройте терминал')
                time.sleep(120)

    web3 = Web3(Web3.HTTPProvider(fun.address['polygon']['rpc'], request_kwargs=config.request_kwargs))
    account = web3.eth.account.from_key(private_key)
    wallet = account.address

    log(f"I-{i}: Начинаю работу с {wallet}")


    polygon_ac = 0
    BSC_ac = 0



    networks_from = config.networks_from
    random.shuffle(networks_from)

    balance_USD = 0
    for network_from in networks_from:
        web3 = Web3(Web3.HTTPProvider(fun.address[network_from]['rpc'], request_kwargs=config.request_kwargs))
        balance_USD = fun.get_token_balance_USD(wallet,network_from,fun.address[network_from]['native'])        
        if balance_USD >= 1:
            log(f'В {network_from} есть газ, не знаю хватит или нет, буду пробовать из нее отпарвлять сообщение' )
            break

    if balance_USD == 0:
        log (f'Не нашел деньги в этом кошельке')
        save_wallet_to("no_money", private_key)
        continue
    

    if network_from == "polygon":
        networks_to = config.networks_polygon_to

    if network_from == "bsc":
        networks_to = config.networks_bsc_to

        
    network_to=random.choice(networks_to)
    log(f'Хочу отправить из {network_from} ->> в {network_to} ')


    message = "ZK light client is live on LayerZero! 🌈"
    adapter_params = "0x00010000000000000000000000000000000000000000000000000000000000030d40"
    zkMessenger_address = Web3.to_checksum_address(address[network_from]['zkMessenger'])
    zkMessenger_contract = web3.eth.contract(address=zkMessenger_address, abi=send_messadge_abi)

    zkFee = zkMessenger_contract.functions.fees(address[network_to]['zk_chain_id']).call()
    
    lzFee = zkMessenger_contract.functions.estimateFee(
        address[network_to]['zk_chain_id'],
        wallet, 
        message,
        adapter_params
        ).call()
    
    # print(zkFee)
    # print(lzFee)
    # exit()

    balance = 0
    balance = web3.eth.get_balance(wallet)
    if balance < lzFee+zkFee * 1.1:
        fun.log_error(f'Не достаточно нативки для оплаты газа')
        save_wallet_to("no_money", private_key)
        continue 

    
    try:
        if  fun.address[network_from]['type']:
            maxPriorityFeePerGas = web3.eth.max_priority_fee
            fee_history = web3.eth.fee_history(10, 'latest', [10, 90])
            baseFee=round(mean(fee_history['baseFeePerGas']))
            maxFeePerGas = maxPriorityFeePerGas + round(baseFee * config.gas_kef)
            transaction = zkMessenger_contract.functions.sendMessage(
                        address[network_to]['zk_chain_id'], 
                        wallet,
                        message,
                        adapter_params
                ).build_transaction({
                'from': wallet,
                'value': lzFee+zkFee,
                'maxFeePerGas': maxFeePerGas,
                'maxPriorityFeePerGas': maxPriorityFeePerGas,   
                'nonce': web3.eth.get_transaction_count(wallet),
            })
        else:
            gasPrice = web3.eth.gas_price
            transaction = zkMessenger_contract.functions.sendMessage(
                        address[network_to]['zk_chain_id'], 
                        wallet,
                        message,
                        adapter_params
                ).build_transaction({
                'from': wallet,
                'value': lzFee+zkFee,
                'gasPrice': gasPrice,
                'nonce': web3.eth.get_transaction_count(wallet),
            })
            gasLimit = web3.eth.estimate_gas(transaction)
            transaction['gas'] = int(gasLimit * config.gas_kef) 


        # Подписываем и отправляем транзакцию
        signed_txn = web3.eth.account.sign_transaction(transaction, private_key)
        tx_hash = web3.to_hex(web3.eth.send_raw_transaction(signed_txn.rawTransaction))
        tx_result = web3.eth.wait_for_transaction_receipt(tx_hash)

        if tx_result['status'] == 1:
            fun.log_ok(f'message send OK: {tx_hash}')
        else:
            fun.log_error(f'message send  false: {tx_hash}')
            save_wallet_to("message_send_error", private_key)

    except Exception as error:
        error_str = str(error)
        fun.log_error(f'message send  false: {error}')
        save_wallet_to("message_send_error", private_key)



        
    fun.timeOut()

log("Ну типа все!")