#CSV Parser test
import CSVParser

def test_parse_instruments():
    instruments = CSVParser.parse_instruments("./DataSets/example-set/input_instruments.csv")
    assert len(instruments) == 4
    assert instruments[0].instrument_id == "SIA"
    assert instruments[0].currency == "SGD"
    assert instruments[0].lot_size == 100
    
def test_parse_clients():
    clients = CSVParser.parse_clients("./DataSets/example-set/input_clients.csv")
    assert len(clients) == 5
    assert clients[0].client_id == "C1"
    assert clients[0].currencies == ['SGD', 'USD']
    assert clients[0].position_check == True
    assert clients[0].rating == 1

def test_parse_orders():
    orders = CSVParser.parse_orders("./DataSets/example-set/input_orders.csv")
    assert len(orders) == 5
    assert orders[0].order_id == "O1"
    assert orders[0].client_id == "C1"
    assert orders[0].instrument_id == "SIA"
    assert orders[0].side == "BUY"
    assert orders[0].quantity == 100
    assert orders[0].price == 100
    assert orders[0].time == "2021-01-01 10:00:00"

test_parse_instruments()
test_parse_clients()
test_parse_orders()