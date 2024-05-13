import CSVParser
import orderHistory
# Description: This file contains the functions to group and categoise the valid orders

def checkOrderValidity(order):
    
    #get the instruments
    instruments = CSVParser.parse_instruments("./DataSets/example-set/input_instruments.csv")
    instruments_dict = {}
    for instrument in instruments:
        instruments_dict[instrument.instrument_id] = instrument

    #get clients
    clients = CSVParser.parse_clients("./DataSets/example-set/input_clients_test.csv")
    clients_dict = {}
    for client in clients:
        clients_dict[client.client_id] = client

    order_instrument = order.instrument_id

    # Instrument Check
    if order_instrument not in instruments_dict:
        # inValidOrders[order.order_id] = (order, "REJECTED - INSTRUMENT NOT FOUND")
        return False, "REJECTED - INSTRUMENT NOT FOUND"

    # Client Check
    client_id = order.client_id
    order_currency = instruments_dict[order_instrument].currency
    if order_currency not in clients_dict[client_id].currencies: #if the required currency for the order is not in the client's list of currencies
        # inValidOrders[order.order_id] = (order, "REJECTED - MISMATCH CURRENCY")
        return False, "REJECTED - MISMATCH CURRENCY"

    #check if lot size is valid against the instrument ID
    order_lot_size = order.quantity
    if float(order_lot_size) % float(instruments_dict[order_instrument].lot_size) != 0:
        # inValidOrders[order.order_id] = (order, "REJECTED - INVALID LOT SIZE")
        return False, "REJECTED - INVALID LOT SIZE"
    
    # check if the order can be processessed checking against the order history, if the client has bought the instrument before
    if order.side == "SELL":
        # find that client's order history
        client_holdings = orderHistory.get_holdings(client_id) #TODO 
        lots_available = client_holdings[order_instrument]
        if lots_available < order_lot_size:
            return False, "REJECTED - POSITION CHECK FAILED"

    # temp_passed_orders_dict[order.order_id] = order

    return True, "PASSED"


# validOrders = {}
# inValidOrders = {}

# # get the orders for testing
# orders = CSVParser.parse_orders("./DataSets/example-set/input_orders_test.csv")
# orders_dict = {}
# temp_passed_orders_dict = {}

# for order in orders:
#     print(checkOrderValidity(order))