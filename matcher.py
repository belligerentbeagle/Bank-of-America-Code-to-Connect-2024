from datetime import datetime
from functools import cmp_to_key
import sys
import CSVParser

buy_orders_by_priority = [] 
sell_orders_by_priority = []
ORDER_HISTORY = []
CLIENT_POSITIONS = {} # {client_id: {instrument_id: net_position}} dummy_client_positions = {'A': {'SIA': 100, 'CAG': 20}, 'B': {'SIA': 0, 'CAG': 0}}
filtered_orders = []
INSTRUMENT_DATA = []
REJECTED_ORDERS = []

filled_orders= []

# returns the number of fullfilled orders if this price is taken as open price
def num_fullfilled_orders(price: int):
    curr_orders = filtered_orders.copy()
    for row, i in enumerate(curr_orders):
        if row['market_order']:
            curr_orders[i] = {'time': row['time'], 'orderID': row['orderID'], 'instrument': row['instrument'],
                         'quantity': row['quantity'], 'price': price, 'side': row['side'], 'market_order': row['market_order']}
    
    
# def find_lowest_price():
#     lowest_price = 1000000000000
#     for row in filtered_orders:
#         if row['price'] < lowest_price:
#             lowest_price = row['price']
#     return lowest_price

# def find_highest_price():
#     highest_price = 0
#     for row in filtered_orders:
#         if row['price'] > highest_price:
#             highest_price = row['price']
#     return highest_price


def get_unique_prices():
    price_list = set()
    for row in filtered_orders:
        if row['price'] not in price_list and not row['market_order']:
            price_list.add(row['price'])
    return list(price_list)

# unique_price_list = get_unique_prices()

# price_highest_fullfilled = None
# num_highest_fullfilled = 0
# for price in unique_price_list:
#     curr = num_fullfilled_orders(price)
#     if curr > num_highest_fullfilled:
#         num_highest_fullfilled = curr
#         price_highest_fullfilled = price

# open_price = price_highest_fullfilled

clients = {'A': {'id': 'A', 'rating': 1}, 'B': {'id': 'B', 'rating': 2}}

filtered_orders1 = [
                    {'time': '9:00:02', 'orderID': 1, 'client': 'B',
                         'quantity': 100, 'price': 32.3, 'side': 'Buy', 'market_order': False},
                    {'time': '9:00:01', 'orderID': 1, 'client': 'A',
                         'quantity': 100, 'price': 32.1, 'side': 'Buy', 'market_order': False},
                    {'time': '9:00:02', 'orderID': 1, 'client': 'B',
                         'quantity': 100, 'price': 32.1, 'side': 'Buy', 'market_order': False},
                    {'time': '9:00:01', 'orderID': 1, 'client': 'B',
                         'quantity': 100, 'price': 32.1, 'side': 'Buy', 'market_order': False},
                    {'time': '9:00:01', 'orderID': 1, 'client': 'B',
                         'quantity': 100, 'price': 32.1, 'side': 'Sell', 'market_order': False},
                    {'time': '9:00:01', 'orderID': 1, 'client': 'B',
                         'quantity': 100, 'price': 32.0, 'side': 'Sell', 'market_order': False}
                    ]


def sortBuysComparator(obj1, obj2):
    if obj1['price'] < obj2['price']:
        return 1
    elif obj1['price'] == obj2['price']:
        if clients[obj1['client']]['rating'] > clients[obj2['client']]['rating']:
            return 1
        elif clients[obj1['client']]['rating'] == clients[obj2['client']]['rating']:
            if datetime.strptime(obj1['time'], "%H:%M:%S") > datetime.strptime(obj2['time'], "%H:%M:%S"):
                return 1
            else:
                return -1
        else:
            return -1
    else:
        return -1

def sortSellsComparator(obj1, obj2):
    if obj1['price'] > obj2['price']:
        return 1
    elif obj1['price'] == obj2['price']:
        if clients[obj1['client']]['rating'] > clients[obj2['client']]['rating']:
            return 1
        elif clients[obj1['client']]['rating'] == clients[obj2['client']]['rating']:
            if datetime.strptime(obj1['time'], "%H:%M:%S") > datetime.strptime(obj2['time'], "%H:%M:%S"):
                return 1
            else:
                return -1
        else:
            return -1
    else:
        return -1
        
def sortBuyOrders(l: list):
    print(l[0])
    buyOrdersList = filter(lambda x: x['side'] == 'Buy', l)
    return list(buyOrdersList)

def sortSellOrders(l: list):
    sellOrdersList = filter(lambda x: x.side == 'Sell', l)
    return list(sellOrdersList)

# test = sorted(filtered_orders1, key=cmp_to_key(sortBuysComparator))
# print(test)

def matchOrders(sortedBuyList: list, sortedSellList: list):
    matchedBuy = {}
    matchedSell = {}
    currBuyOrder = sortedBuyList[0] # order book buy side
    currSellOrder = sortedSellList[0] # order book sell side

    # Match Attempt
    if currBuyOrder['price'] >= currSellOrder['price']: # if match is found in the orderbook
        return (matchedBuy, matchedSell)
    else: #if no match found, we add orders to orderbook
        return False


import sys
import CSVParser
import orderValidator
import reportGenerator
# take in order, clients, and instruments csv as CLI arguments 
if __name__ == "__main__":
    inputs = sys.argv
    _, order_file, client_file, instru_file = inputs

    #load all csv
    orders = CSVParser.parse_orders(order_file)
    clients = CSVParser.parse_clients(client_file)
    instruments = CSVParser.parse_instruments(instru_file)

    # sort order by time, check validity of each order and execute. While saving the order's history
    for order in orders:
        valid, reason = orderValidator.checkOrderValidity(order)
        if valid:
            ORDER_HISTORY.append(order)
        else:
            REJECTED_ORDERS.append((order.order_id, reason))
    
    arr_copy = ORDER_HISTORY.copy()
    for obj in ORDER_HISTORY:
        filled_orders.append({'time': obj.time, 'orderID': obj.order_id, 'client': obj.client_id,
             'quantity': obj.quantity, 'price': obj.price, 'side': obj.side, 'market_order': obj.market})
    
    buy_orders = sortBuyOrders(filled_orders)
    buy_orders_by_priority = sorted(buy_orders, key=cmp_to_key(sortBuysComparator))
    sell_orders = sortSellOrders(filled_orders)
    sell_orders_by_priority = sorted(sell_orders, key=cmp_to_key(sortSellsComparator))
    print(buy_orders_by_priority)
    print(sell_orders_by_priority)

    reportGenerator.generate_exchange_report(REJECTED_ORDERS)
    # reportGenerator.client_report(dummy_client_positions)

    reportGenerator.client_report(CLIENT_POSITIONS)
    # reportGenerator.instrumental_report(INSTRUMENT_DATA)
