#CSV Parser test
import CSVParser

def test_parse_instruments():
    instruments = CSVParser.parse_instruments("./DataSets/example-set/input_instruments.csv")
    assert len(instruments) == 1
    assert instruments[0].instrument_id == "SIA"
    assert instruments[0].currency == "SGD"
    assert instruments[0].lot_size == 100

def test_parse_clients():
    clients = CSVParser.parse_clients("./DataSets/example-set/input_clients.csv")
    assert len(clients) == 5
    assert clients[0].client_id == "A"
    assert clients[0].currencies == ['USD', 'SGD']
    assert clients[0].position_check == True
    assert clients[0].rating == 1

def test_parse_orders():
    orders = CSVParser.parse_orders("./DataSets/example-set/input_orders.csv")
    assert len(orders) == 17
    assert orders[0].order_id == "A1"
    assert orders[0].client_id == "A"
    assert orders[0].instrument_id == "SIA"
    assert orders[0].side == "Buy"
    assert orders[0].quantity == 1500
    assert orders[0].price == None
    assert orders[0].time == "9:00:01"
    assert orders[0].market == True

test_parse_instruments()
test_parse_clients()
test_parse_orders()