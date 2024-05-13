#CSV Parser test
import CSVParser

def test_parse_instruments():
    instruments = CSVParser.parse_instruments("./DataSets/example-set/input_instruments.csv")
    assert len(instruments) == 4
    assert instruments[0].instrument_id == "SIA"
    assert instruments[0].currency == "SGD"
    assert instruments[0].lot_size == "100"

def test_parse_clients():
    clients = CSVParser.parse_clients("./DataSets/example-set/input_clients.csv")
    assert len(clients) == 5
    assert clients[0].client_id == "C1"
    assert clients[0].currencies == ['SGD', 'USD']
    assert clients[0].position_check == True
    assert clients[0].rating == 1