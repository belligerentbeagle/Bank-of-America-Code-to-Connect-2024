from datetime import datetime
from functools import cmp_to_key
import sys
import CSVParser

filtered_orders = []
buy_orders_by_priority = []
sell_orders_by_priority = []
ORDER_HISTORY = []
REJECTED_ORDERS = []
CLIENT_POSITIONS = []
INSTRUMENT_DATA = []

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

clients = {}
instruments = {}
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
    buyOrdersList = filter(lambda x: x['side'] == 'Buy', l)
    return list(buyOrdersList)

def sortSellOrders(l: list):
    sellOrdersList = filter(lambda x: x['side'] == 'Sell', l)
    return list(sellOrdersList)

# test = sorted(filtered_orders1, key=cmp_to_key(sortBuysComparator))
# print(test)

def matchOrders(sortedBuyList: list, sortedSellList: list):
    matchedBuy = {}
    matchedSell = {}
    currBuyOrder = sortedBuyList[0]
    currSellOrder = sortedSellList[0]
    if currBuyOrder['price'] >= currSellOrder['price']:
        return (matchedBuy, matchedSell)
    else:
        return False




import sys
import CSVParser
import orderValidator
# take in order, clients, and instruments csv as CLI arguments 
if __name__ == "__main__":
    inputs = sys.argv
    _, order_file, client_file, instru_file = inputs

    #load all csv
    orders = CSVParser.parse_orders(order_file)
    clients_retrieved = CSVParser.parse_clients(client_file)
    instruments_retrieved = CSVParser.parse_instruments(instru_file)
    print(instruments_retrieved)
    arr_copy = orders.copy()
    for obj in arr_copy:
        filled_orders.append({'time': obj.time, 'orderID': obj.order_id, 'client': obj.client_id,
             'quantity': obj.quantity, 'price': obj.price, 'side': obj.side, 'market_order': obj.market,
             'instrument': obj.instrument_id})
    for obj in clients_retrieved:
        clients[obj.client_id] = {'id': obj.client_id, 'currencies': obj.currencies, 'rating': obj.rating,
             'position_check': obj.position_check}
    for obj in instruments_retrieved:
        instruments[obj.instrument_id] = {'id': obj.instrument_id, 'currency': obj.currency, 'lot_size': obj.lot_size}
    
    buy_orders = sortBuyOrders(filter(lambda x: x['price'] != None, filled_orders))
    buy_orders_by_priority = sorted(buy_orders, key=cmp_to_key(sortBuysComparator))
    sell_orders = sortSellOrders(filter(lambda x: x['price'] != None, filled_orders))
    sell_orders_by_priority = sorted(sell_orders, key=cmp_to_key(sortSellsComparator))
    
    # # sort order by time, check validity of each order and execute. While saving the order's history
    # for order in orders:
    #     valid, reason = orderValidator.checkOrderValidity(order)
    #     if valid:
    #         ORDER_HISTORY.append(order)
    #     else:
    #         REJECTED_ORDERS.append(order)
    
    
    #Open Auction
    open_auction_buys = list(filter(lambda x: datetime.strptime(x['time'], "%H:%M:%S").time() < datetime(2022, 2, 2, 9, 30, 0).time(), buy_orders_by_priority))
    open_auction_sells = list(filter(lambda x: datetime.strptime(x['time'], "%H:%M:%S").time() < datetime(2022, 2, 2, 9, 30, 0).time(), sell_orders_by_priority))
    
    for instrument in list(instruments.values()):
        filtered_buys_instr = list(filter(lambda x: x['instrument'] == instrument['id'], open_auction_buys))
        filtered_sells_instr = list(filter(lambda x: x['instrument'] == instrument['id'], open_auction_sells))
        
        while True:
            curr_buy = filtered_buys_instr[0]
            curr_sell = filtered_sells_instr[0]
            print(curr_buy)
            print(curr_sell)
            if curr_buy['price'] >= curr_sell['price']:
                
                orderFilled = True
                volume_fullfilled = min(int(curr_buy['quantity']), int(curr_sell['quantity']))
                print(volume_fullfilled)
                if volume_fullfilled > 0:
                    ORDER_HISTORY.append({'client_buy': curr_buy['client'], 'client_sell': curr_sell['client'],
                                        'order_buy': curr_buy['orderID'], 'order_sell': curr_sell['orderID'],
                                        'vol': volume_fullfilled, 'instument': instrument['id']})
                    curr_buy['quantity'] = str(int(curr_buy['quantity']) - int(volume_fullfilled))
                    curr_sell['quantity'] = str(int(curr_sell['quantity']) - int(volume_fullfilled))
                else:
                    break
            else:
                break
        
    print(ORDER_HISTORY)
    print(instruments)
    client_report = []
    for client in list(clients.values()):
        filtered_orders_client = list(filter(lambda x: x['client_buy'] == client or x['client_buy'] == client, 
                                            ORDER_HISTORY))   
        
        for instr in list(instruments.values()):
            # client_report.append([client['id'], instr['id']])
        # print(client)
        # for instrument in instruments
        # client_report.append(client['id'], )

    #Continous Trading
    
    #Close Auction
    