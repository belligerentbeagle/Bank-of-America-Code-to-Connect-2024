import csv

# Instrument object
class Instrument:
    def __init__(self, instrument_id, currency, lot_size):
        self.instrument_id = instrument_id
        self.currency = currency
        self.lot_size = lot_size 

    def __str__(self):
        return f"Instrument ID: {self.instrument_id}, Currency: {self.currency}, Lot Size: {self.lot_size}"

# Order Object
class Order:
    def __init__(self, time, client_id, instrument_id, side, price, quantity, order_id, market_bool):
        self.time = time
        self.order_id = order_id
        self.client_id = client_id
        self.instrument_id = instrument_id
        self.quantity = quantity
        if price is not None:
            self.price = float(price)
        else:
            self.price = None
        self.side = side
        self.market = market_bool

    def __str__(self):
        return f"Time: {self.time}, Client ID: {self.client_id}, Instrument ID: {self.instrument_id}, Side: {self.side}, Price: {self.price}, Quantity: {self.quantity}, Order ID: {self.order_id}, Market: {self.market}"


# Client Object
class Client:
    def __init__(self, client_id, currencies, position_check, rating):
        self.client_id = client_id
        self.currencies = currencies
        self.position_check = position_check
        self.rating = rating

    def __str__(self):
        return f"Client ID: {self.client_id}, Currencies: {self.currencies}, Position Check: {self.position_check}, Rating: {self.rating}"



## Takes in a file path and returns a list of instrument objects
## Each instrument object contains the instrument_id, currency, and lot_size

# Example:
# instruments = parse_instruments("./DataSets/example-set/input_instruments.csv")
# print(instruments[0]) # Instrument ID: SIA, Currency: SGD, Lot Size: 100

def parse_instruments(instruments_file):
    instruments = open(instruments_file, "r")
    instruments_array = []
    count = 0
    for i in instruments:
        #we skip the first line because it contains the header
        if count == 0:
            count += 1
            continue
        instrument_id = i.split(",")[0]
        currency = i.split(",")[1]
        lot_size = int(i.split(",")[2])
        instruments_array.append(Instrument(instrument_id, currency, lot_size))

    #remove header
    # instruments_dict = instruments_dict.pop("InstrumentID")

    return instruments_array


###parse clients.csv


## Takes in a file path and returns a list of client objects
## Each client object contains the client_id, currencies, position_check, and rating
## Example:
# clients = parse_clients("./DataSets/example-set/input_clients.csv")
# print(clients[0]) # Client ID: C1, Currencies: list of currencies, Position Check: True/False, Rating: 1
def parse_clients(clients_file):
    clients_array = []
    with open(clients_file, "r") as clients:
        reader = csv.reader(clients)
        next(reader)  # Skip the header
        for row in reader:
            client_id = row[0]
            currencies = row[1].split(",")
            position_check = row[2] == "Y"
            rating = int(row[3])
            clients_array.append(Client(client_id, currencies, position_check, rating))

    return clients_array #we skip the first line because it contains the header

# clients = parse_clients("./DataSets/example-set/input_clients.csv")

# for client in clients:
#     print(client)

## Takes in a file path and returns a list of order objects
## Each order object contains the time, client_id, instrument_id, side, price, quantity, and order_id
## Example:
# orders = parse_orders("./DataSets/example-set/input_orders.csv")
# print(orders[0]) # Time: 16:09:59, Client ID: E, Instrument ID: SIA, Side: Buy, Price: 31.8, Quantity: 2000, Order ID: E3, Market: False
def parse_orders(orders_file):
    orders_array = []
    with open(orders_file, "r") as orders:
        reader = csv.reader(orders)
        next(reader)  # Skip the header
        for row in reader:
            time = row[0]
            order_id = row[1]
            instrument_id = row[2]
            quantity = float(row[3])
            price = row[5]
            market = False
            if price == "Market":
                price = None
                market = True
            else:
                price = float(price)

            client_id = row[4]
            side = row[6]
            orders_array.append(Order(time, client_id, instrument_id, side, price, quantity, order_id, market))

    return orders_array #we skip the first line because it contains the header

# orders = parse_orders("./DataSets/example-set/input_orders.csv")
# for order in orders:
#     print(order)

