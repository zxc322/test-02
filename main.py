import telebot
import logging
from flask import Flask, request
from config import *
import json
from requests import Request, Session, post


bot = telebot.TeleBot(token)
server = Flask(__name__)
logger = telebot.logger
logger.setLevel(logging.DEBUG)
session = Session()
headers = {'Accepts': 'application.json', 'X-CMC_PRO_API_KEY': COINMARKETCAP_API_KEY}



def get_symbol():
    symbol = request.json['message']['text']
    return symbol.upper()

def return_price(symbol):
    symbol = get_symbol()
    parameters = {"symbol": symbol, 'convert': 'USD'}
    session.headers.update(headers)
    try:
        responce = session.get(COINMARKETCAP_API_URL, params=parameters)
        price = round(json.loads(responce.text)['data'][symbol]['quote']['USD']['price'], 3)
        full_price = f'Price is : {price}'
        return full_price
    except:
        return '---'


def full_coin_name(symbol):
    symbol = get_symbol()
    parameters = {"symbol": symbol, 'convert': 'USD'}
    session.headers.update(headers)
    try:
        responce = session.get(COINMARKETCAP_API_URL, params=parameters)
        coin_name = json.loads(responce.text)['data'][symbol]['name']
        coin_full = 'Coin name is: ' + coin_name
        return coin_full
    except:
        return 'Неправильный символ ! \nВведите корретный символ,\nбудьте так любезны(BTC, ETH, SOL например): '


def change_24(symbol):
    symbol = get_symbol()
    parameters = {"symbol": symbol, 'convert': 'USD'}
    session.headers.update(headers)
    try:
        responce = session.get(COINMARKETCAP_API_URL, params=parameters)
        percent_change_24h = round((json.loads(responce.text)['data'][symbol]['quote']['USD']['percent_change_24h']), 2)
        if percent_change_24h > 0:
            change_24 = f'24 hours change is: +{percent_change_24h}'
        else:
            change_24 = f'24 hours change is: {percent_change_24h}'
        return change_24
    except:
        return '---'


def change_7(symbol):
    symbol = get_symbol()
    parameters = {"symbol": symbol, 'convert': 'USD'}
    session.headers.update(headers)
    try:
        responce = session.get(COINMARKETCAP_API_URL, params=parameters)
        percent_change_7d = round((json.loads(responce.text)['data'][symbol]['quote']['USD']['percent_change_7d']), 2)
        if percent_change_7d > 0:
            change_7 = f'7 days change is: +{percent_change_7d}'
        else:
            change_7 = f'7 days change is: {percent_change_7d}'
        return change_7
    except:
        return '---'


def send_message(chat_id, text):
    method = 'sendMessage'
    url = f'{TELEGRAM_URL}{token}/{method}'
    data = {'chat_id': chat_id, 'text': text}
    post(url, data=data)



@server.route(f'/{token}', methods=['POST'])
def redirect_message():
    symbol = get_symbol()
    return_price(symbol)
    full_coin_name(symbol)
    change_24(symbol)
    change_7(symbol)
    chat_id = request.json['message']['chat']['id']
    send_message(chat_id=chat_id, text=f'{full_coin_name(symbol)}\n'
                                       f'{return_price(symbol)}\n{change_24(symbol)}\n{change_7(symbol)}')
    return '!', 200
   


if __name__ == '__main__':
    bot.remove_webhook()
    bot.set_webhook(url=app_url)
    server.run()



