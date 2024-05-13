import CSVParser
import orderHistory
# Description: This file contains the functions to group and categoise the valid orders


# TODO Rejection Reasons to be added

def getValidOrders():
    # return ["order1", "order2", "order3"]
    validOrders = {}
    inValidOrders = {}

    # get the orders
    orders = CSVParser.parse_orders("./DataSets/example-set/input_orders_test.csv")
    orders_dict = {}
    temp_orders_dict = {}
    for order in orders:
        orders_dict[order.order_id] = order
    
    #check if the instrument exists
    instruments = CSVParser.parse_instruments("./DataSets/example-set/input_instruments.csv")
    instruments_dict = {}
    for instrument in instruments:
        instruments_dict[instrument.instrument_id] = instrument
    
    for order_id in orders_dict:
        order = orders_dict[order_id]
        if order.instrument_id not in instruments_dict:
            inValidOrders[order.order_id] = (order, "REJECTED - INSTRUMENT NOT FOUND")
        else:
            temp_orders_dict[order.order_id] = order
    
    orders_dict_instr_Checked = temp_orders_dict
    temp_orders_dict = {}

    #check if the client has the currency eligibility
    clients = CSVParser.parse_clients("./DataSets/example-set/input_clients_test.csv")
    clients_dict = {}
    for client in clients:
        clients_dict[client.client_id] = client
    
    for order_id in orders_dict_instr_Checked:
        order = orders_dict_instr_Checked[order_id]
        # assume client's id already exists.
        client_id = order.client_id
        order_instrument = order.instrument_id
        order_currency = instruments_dict[order_instrument].currency
        if order_currency not in clients_dict[client_id].currencies: #if the required currency for the order is not in the client's list of currencies
            inValidOrders[order.order_id] = (order, "REJECTED - MISMATCH CURRENCY")
        else:
            temp_orders_dict[order.order_id] = order
    
    orders_dict_currency_Checked = temp_orders_dict
    temp_orders_dict = {}

    # print(orders_dict_currency_Checked)
    
    #check if lot size is valid against the instrument ID
    for order_id in orders_dict_currency_Checked:
        order = orders_dict_currency_Checked[order_id]
        order_instrument = order.instrument_id
        order_lot_size = order.quantity
        if float(order_lot_size) % float(instruments_dict[order_instrument].lot_size) != 0:
            inValidOrders[order.order_id] = (order, "REJECTED - INVALID LOT SIZE")
        else:
            temp_orders_dict[order.order_id] = order

    orders_dict_lot_Checked = temp_orders_dict
    temp_orders_dict = {}

    print(orders_dict_lot_Checked)

    # #check if the client has the position check that exceed's client's current position of this instrument.
    # for order_id in orders_dict_lot_Checked:
    #     order = orders_dict_lot_Checked[order_id]
    #     if order.side == "BUY":
    #         temp_orders_dict[order.order_id] = order
    #         continue

    #     # if order sell
    #     client_id = order.client_id
    #     if clients_dict[client_id].position_check == False:
    #         temp_orders_dict[order.order_id] = order
    #         continue
        
    #     # if it is a sell and orders requires position checking on client
    #     order_instrument = order.instrument_id
    #     order_quantity = order.quantity
    #     order_history = orderHistory.ORDER_HISTORY()


        

def getInvalidOrders():
    return ["order4", "order5", "order6"]

# getValidOrders()
print(orderHistory.ARRAY_TEST)