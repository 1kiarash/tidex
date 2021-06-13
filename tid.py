import requests
import json
import time

#api form: "https://api.tidex.com/api/3/<method name>/<pair listing>."
#e2c_btc will cost 0.1 e2c

'''All information is cached every 2 seconds, so there's no point in making more frequent requests'''


convert_curr_btc_api = "https://api.tidex.com/api/3/ticker/e2c_btc"
convert_curr_eth_api = "https://api.tidex.com/api/3/ticker/e2c_eth"

btc_api = "https://api.coinbase.com/v2/prices/BTC-USD/spot"
eth_api = "https://api.coinbase.com/v2/prices/ETH-USD/spot"
btc_case = {'sell1' : 0 , 'sell2': 0 }
eth_case = {'sell1' : 0 , 'sell2': 0 }
best_price = 0.6

def curlike(url):
    response = requests.get(url)
    return response.content

def btc_data_saver(data):
    log_file = open("btc_logfile.txt" , "a")    
    log_file.write( str(data) + "\t" + str(time.time()) + "\n" )
    log_file.close()

def eth_data_saver(data):
    log_file = open("eth_logfile.txt" , "a")    
    log_file.write( str(data) + "\t" + str(time.time()) + "\n" )
    log_file.close()

def btc_evaluation (data): # check for any change in price
    btc_case['sell1'] = btc_data['e2c_btc']['sell']                   
    if btc_case['sell1'] != btc_case['sell2']:
       btc_data_saver(btc_case['sell1'])
       btc_case['sell2'] = btc_case['sell1']
        
    if (btc_case['sell1']*float(btc_price['data']['amount'])) >= best_price:
        text_me(btc_case['sell1']*float(btc_price['data']['amount']))

def eth_evaluation (data): # check for any change in price in eth
    eth_case['sell1'] = eth_data['e2c_eth']['sell']                   
    if eth_case['sell1'] != eth_case['sell2']:
       eth_data_saver(eth_case['sell1'])
       eth_case['sell2'] = eth_case['sell1']
        
    if (eth_case['sell1']*float(eth_price['data']['amount'])) >= best_price:
        text_me(eth_case['sell1']*float(eth_price['data']['amount']))
    else:
        return 0
    
def text_me(data):
    auth_key = '4369417141692B757A596F76744F477362317A7A57575535676352326666734D'
    url = "https://api.kavenegar.com/v1/%s/sms/send.json?" %auth_key
    payload = {'receptor' : '#phonenumber' ,
                'message' : '%f%D9%88%D9%82%D8%AA%D8%B4%D9%87%20%D8%A8%D8%AE%D8%B1%DB%8C%21%0A-%DA%A9%DB%8C%D8%A7' % data
                }
    res = requests.post(url,data=payload)
    print(res)
while(True):    
    btc_data = json.loads(curlike(convert_curr_btc_api)) #e2c price in btc
    eth_data = json.loads(curlike(convert_curr_eth_api)) #e2c price in eth
    btc_price = json.loads(curlike(btc_api)) # btc price in USD
    eth_price = json.loads(curlike(eth_api)) # eth price in USD
    highest_btc = btc_data['e2c_btc']['high'] #highest price of e2c based on btc from day 0
    lowest_btc = btc_data['e2c_btc']['low']   #lowest price of e2c based on btc from day 0
    highest_eth = eth_data['e2c_eth']['high'] #highest price of e2c based on eth from day 0 
    lowest_eth = eth_data['e2c_eth']['low']   #lowest price of e2c based on eth from day 0
    btc_evaluation(btc_data)
    eth_evaluation(eth_data)
    time.sleep(60)


#TODO parse the response and find the best price
