from datetime import datetime
from functools import cmp_to_key
import sys
import CSVParser
import sys
import CSVParser
from CSVParser import Order
from CSVParser import Client
from CSVParser import Instrument
import orderValidator
import reportGenerator
import math

#file paths
ORDER_FILE_PATH = ""
CLIENT_FILE_PATH = ""
INSTRUMENT_FILE_PATH = ""

buy_orders_by_priority = [] 
sell_orders_by_priority = []
ORDER_HISTORY = []
CLIENT_POSITIONS = {}
filtered_orders = []
INSTRUMENT_DATA = []
REJECTED_ORDERS = []
filled_orders= []

# returns the number of fullfilled orders if this price is taken as open price
def num_fullfilled_orders(price: int):
    curr_orders = filtered_orders.copy()
    for row, i in enumerate(curr_orders):
        if row['market_order']:
            curr_orders[i] = Order(row['time'], row['orderID'], row['client'], row['instrument'],
                                   row['quantity'], price, row['side'], row['market_order'])

def get_unique_prices():
    price_list = set()
    for row in filtered_orders:
        if row['price'] not in price_list and not row['market_order']:
            price_list.add(row['price'])
    return list(price_list)

# clients = {}
# instruments = {}

def sortBuysComparatorByPriceRatingTime(obj1, obj2):
    if obj1.price < obj2.price:
        return 1
    elif obj1.price == obj2.price:
        if clients[obj1.client_id]['rating'] > clients[obj2.client_id]['rating']:
            return 1
        elif clients[obj1.client_id]['rating'] == clients[obj2.client_id]['rating']:
            if datetime.strptime(obj1.time, "%H:%M:%S") > datetime.strptime(obj2.time, "%H:%M:%S"):
                return 1
            else:
                return -1
        else:
            return -1
    else:
        return -1

def sortSellsComparatorByPriceRatingTime(obj1, obj2):
    if obj1.price > obj2.price:
        return 1
    elif obj1.price == obj2.price:
        if clients[obj1.client_id]['rating'] > clients[obj2.client_id]['rating']:
            return 1
        elif clients[obj1.client_id]['rating'] == clients[obj2.client_id]['rating']:
            if datetime.strptime(obj1.time, "%H:%M:%S") > datetime.strptime(obj2.time, "%H:%M:%S"):
                return 1
            else:
                return -1
        else:
            return -1
    else:
        return -1
        
def sortBuyOrders(l: list):
    buyOrdersList = filter(lambda x: x.side == 'Buy', l)
    return list(buyOrdersList)

def sortSellOrders(l: list):
    sellOrdersList = filter(lambda x: x.side == 'Sell', l)
    return list(sellOrdersList)

def matchOrders(sortedBuyList: list, sortedSellList: list):
    matchedBuy = {}
    matchedSell = {}
    currBuyOrder = sortedBuyList[0] # order book buy side
    currSellOrder = sortedSellList[0] # order book sell side

    # Match Attempt
    if currBuyOrder.price >= currSellOrder.price: # if match is found in the orderbook
        return (matchedBuy, matchedSell)
    else: #if no match found, we add orders to orderbook
        return False

def generate_all_reports(REJECTED_ORDERS, CLIENT_POSITIONS, ORDER_HISTORY):
    try:
        reportGenerator.generate_exchange_report(REJECTED_ORDERS)
    #     reportGenerator.generate_client_report(CLIENT_POSITIONS)
    #     reportGenerator.generate_instrument_report(INSTRUMENT_DATA)
    except Exception as e:
        print(e)
        return 0 
    return -1

def segment_orders_by_time(orders):
    oa_orders = list(filter(lambda x: datetime.strptime(x.time, "%H:%M:%S").time() < datetime(2022, 2, 2, 9, 30, 0).time(), orders))
    ct_orders = list(filter(lambda x: datetime.strptime(x.time, "%H:%M:%S").time() >= datetime(2022, 2, 2, 9, 30, 0).time() and datetime.strptime(x.time, "%H:%M:%S").time() < datetime(2022, 2, 2, 16, 0, 0).time(), orders))
    ca_orders = list(filter(lambda x: datetime.strptime(x.time, "%H:%M:%S").time() >= datetime(2022, 2, 2, 16, 0, 0).time(), orders))

    return oa_orders, ct_orders, ca_orders #TODO handle may be empty list or None

def open_auction(oa_orders):
    open_price = 0 
    max_vol = 0 
    for order in oa_orders:
        price, vol = try_execute_trade(order)
        if vol > max_vol:
            max_vol = vol
            open_price = price
        elif vol == max_vol:
            max_vol = vol
            open_price = max(open_price, price)

    return open_price
    
def try_execute_trade(order):
    valid, reason = orderValidator.checkOrderValidity(order, CLIENT_FILE_PATH, INSTRUMENT_FILE_PATH)
    if not valid:
        REJECTED_ORDERS.append((order.order_id, reason))
        return 0, 0
    return try_match_order(order)

def try_match_order(order):
    #add to order book of buy or sell
    add_to_order_book(order)
    if len(buy_orders_by_priority) > 0 and len(sell_orders_by_priority) > 0 and buy_orders_by_priority[0].price >= sell_orders_by_priority[0].price:
        #potential match
        buy_order = buy_orders_by_priority.pop()
        sell_order = sell_orders_by_priority.pop()
        return process_trade(buy_order, sell_order)
    return 0, 0

def process_trade(buy_order, sell_order):
    trad_vol = min(buy_order.quantity, sell_order.quantity)
    if buy_order.quantity - trad_vol > 0: #still have buy orders left over
        fulfilled_buy_order = Order(buy_order.time, buy_order.order_id, buy_order.client_id, buy_order.instrument_id, trad_vol, buy_order.price, buy_order.side, buy_order.market)
        ORDER_HISTORY.append(sell_order)
        ORDER_HISTORY.append(fulfilled_buy_order)
        left_over_buy_qty = buy_order.quantity - trad_vol
        leftover_buy_order = Order(buy_order.time, buy_order.order_id, buy_order.client_id, buy_order.instrument_id, left_over_buy_qty, buy_order.price, buy_order.side, buy_order.market)
        add_to_order_book(leftover_buy_order)
        print("buy order partially fulfilled")
        return buy_order.price, trad_vol
    elif sell_order.quantity - trad_vol > 0: #still have sell orders left over
        fulfilled_sell_order = Order(sell_order.time, sell_order.order_id, sell_order.client_id, sell_order.instrument_id, trad_vol, sell_order.price, sell_order.side, sell_order.market)
        ORDER_HISTORY.append(buy_order)
        ORDER_HISTORY.append(fulfilled_sell_order)
        left_over_sell_qty = sell_order.quantity - trad_vol
        leftover_sell_order = Order(sell_order.time, sell_order.order_id, sell_order.client_id, sell_order.instrument_id, left_over_sell_qty, sell_order.price, sell_order.side, sell_order.market)
        add_to_order_book(leftover_sell_order)
        print("sell order partially fulfilled")
        return sell_order.price, trad_vol
    elif buy_order.quantity == sell_order.quantity:
        ORDER_HISTORY.append(buy_order)
        ORDER_HISTORY.append(sell_order)
        print("both orders completely fulfilled")
        return buy_order.price, sell_order.quantity 
    return 0, 0


def add_to_order_book(order):
    global buy_orders_by_priority
    global sell_orders_by_priority

    if order.side == 'Buy':
        if order.market:
            order.price = math.inf
        buy_orders_by_priority.append(order)
        buy_orders_by_priority = sorted(buy_orders_by_priority, key=cmp_to_key(sortBuysComparatorByPriceRatingTime))
    else:
        if order.market:
            order.price = 0
        sell_orders_by_priority.append(order)
        sell_orders_by_priority = sorted(sell_orders_by_priority, key=cmp_to_key(sortSellsComparatorByPriceRatingTime))

# take in order, clients, and instruments csv as CLI arguments 
if __name__ == "__main__":
    inputs = sys.argv
    _, order_file, client_file, instru_file = inputs
    ORDER_FILE_PATH = order_file
    CLIENT_FILE_PATH = client_file
    INSTRUMENT_FILE_PATH = instru_file

    #load all csv
    orders = CSVParser.parse_orders(order_file)
    clients_retrieved = CSVParser.parse_clients(client_file)
    instruments_retrieved = CSVParser.parse_instruments(instru_file)

    #open auction orders
    open_auction_orders, continuous_trading_orders, close_auction_orders = segment_orders_by_time(orders)
    open_price = open_auction(open_auction_orders) # left over orders are left in order book

    # #continous trading
    # left_over_from_CT = continous_trading(left_over_from_OA + continuous_trading_orders)

    # #close auction
    # left_over_from_CA = close_auction(left_over_from_CT + close_auction_orders)

    # Generate reports
    generate_all_reports(REJECTED_ORDERS, CLIENT_POSITIONS, ORDER_HISTORY)

    print(open_price)
    print(buy_orders_by_priority)
    print(sell_orders_by_priority)
    
    exit(0)

    
    # for instrument in list(instruments.values()):
    #     filtered_buys_instr = list(filter(lambda x: x.instrument_id == instrument['id'], open_auction_buys))
    #     filtered_sells_instr = list(filter(lambda x: x.instrument_id == instrument['id'], open_auction_sells))
        
    #     while True:
    #         curr_buy = filtered_buys_instr[0]
    #         curr_sell = filtered_sells_instr[0]

    #         print(curr_buy)
    #         print(curr_sell)
    #         if curr_buy.price >= curr_sell.price:
                
    #             orderFilled = True
    #             volume_fullfilled = min(int(curr_buy.quantity), int(curr_sell.quantity))
    #             print(volume_fullfilled)
    #             if volume_fullfilled > 0:
    #                 #remove first elements from buy and sell queue
    #                 filtered_buys_instr.pop(0)
    #                 filtered_sells_instr.pop(0)
    #                 # check if have left over.
    #                 if int(curr_buy.quantity) - int(volume_fullfilled) > 0:
    #                     curr_buy.quantity = str(int(curr_buy.quantity) - int(volume_fullfilled))
    #                     updated_buy_order = Order(curr_buy.time, curr_buy.order_id, curr_buy.client_id, curr_buy.instrument_id,
    #                                               curr_buy.quantity, curr_buy.price, curr_buy.side, curr_buy.market_order)
    #                     fully_fulfilled_sell_order = Order(curr_sell.time, curr_sell.order_id, curr_sell.client_id, curr_sell.instrument_id,
    #                                                        curr_sell.quantity, curr_sell.price, curr_sell.side, curr_sell.market_order)
    #                     partially_fulfilled_buy_order = Order(curr_buy.time, curr_buy.order_id, curr_buy.client_id, curr_buy.instrument_id,
    #                                                            curr_sell.quantity, curr_buy.price, curr_buy.side, curr_buy.market_order)
    #                     ORDER_HISTORY.append(fully_fulfilled_sell_order)
    #                     ORDER_HISTORY.append(partially_fulfilled_buy_order)
    #                     #add updated buy order back to buy queue
    #                     filtered_buys_instr.append(updated_buy_order)
    #                     filtered_buys_instr = sorted(filtered_buys_instr, key=cmp_to_key(sortBuysComparatorByPriceRatingTime))

    #                 elif int(curr_sell.quantity) - int(volume_fullfilled) > 0:
    #                     curr_sell.quantity = str(int(curr_sell.quantity) - int(volume_fullfilled))
    #                     updated_sell_order = Order(curr_sell.time, curr_sell.order_id, curr_sell.client_id, curr_sell.instrument_id,
    #                                                curr_sell.quantity, curr_sell.price, curr_sell.side, curr_sell.market_order)
    #                     fully_fulfilled_buy_order = Order(curr_buy.time, curr_buy.order_id, curr_buy.client_id, curr_buy.instrument_id,
    #                                                       curr_buy.quantity, curr_buy.price, curr_buy.side, curr_buy.market_order)
    #                     partially_fulfilled_sell_order = Order(curr_sell.time, curr_sell.order_id, curr_sell.client_id, curr_sell.instrument_id,
    #                                                            curr_buy.quantity, curr_sell.price, curr_sell.side, curr_sell.market_order)
    #                     ORDER_HISTORY.append(fully_fulfilled_buy_order)
    #                     ORDER_HISTORY.append(partially_fulfilled_sell_order)
    #                     #add updated sell order back to sell queue
    #                     filtered_sells_instr.append(updated_sell_order)
    #                     filtered_sells_instr = sorted(filtered_sells_instr, key=cmp_to_key(sortSellsComparatorByPriceRatingTime))
    #                 else: #both buy and sell completely fulfills each other                    
    #                     ORDER_HISTORY.append(curr_buy, curr_sell)
    #                 curr_buy.quantity = str(int(curr_buy.quantity) - int(volume_fullfilled))
    #                 curr_sell.quantity = str(int(curr_sell.quantity) - int(volume_fullfilled))
    #             else:
    #                 break
    #         else:
    #             break
        
    # print(f'Order history {ORDER_HISTORY}')
    # print(f'Instruments {instruments}')
    # client_report = []
    # for client in list(clients.keys()):
    #     filtered_orders_client = list(filter(lambda x: x.client_id == client, ORDER_HISTORY))   
    #     ### show total holdings of each client
    #     # get unique instruments
    #     instruments = set()
    #     for row in filtered_orders_client:
    #         instruments.add(row.instrument_id)
            
    #     # Ensure the client key exists in CLIENT_POSITIONS and its value is a dictionary
    #     if client not in CLIENT_POSITIONS:
    #         CLIENT_POSITIONS[client] = {}

    #     for instrument in instruments:
    #         this_instrument_orders = list(filter(lambda x: x.instrument_id == instrument, filtered_orders_client))
    #         total_holdings = 0
    #         for row in this_instrument_orders:
    #             if row.side == 'Buy':
    #                 total_holdings += row.quantity
    #             else:
    #                 total_holdings -= row.quantity
    #         CLIENT_POSITIONS[client][instrument] = total_holdings

        
    
