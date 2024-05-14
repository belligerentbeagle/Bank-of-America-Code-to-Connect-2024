# matcher test file
import unittest
from matchingEngine import segment_orders_by_time
from CSVParser import parse_orders
from CSVParser import Order
from datetime import datetime


# test for segmenting orders
class TestSegmentOrders(unittest.TestCase):
    def test_segment_orders(self):
        orders = parse_orders("./DataSets/example-set/input_orders_test.csv")
        oa, ct, ca = segment_orders_by_time(orders)
        for order in oa:
            self.assertIsInstance(order, Order)
            self.assertTrue(datetime.strptime(order.time , "%H:%M:%S").time() < datetime(2022, 2, 2, 9, 30, 0).time())
        print("Orders before 9:30:00 passed")

        for order in ct:
            self.assertIsInstance(order, Order)
            self.assertTrue(datetime.strptime(order.time , "%H:%M:%S").time() >= datetime(2022, 2, 2, 9, 30, 0).time() and datetime.strptime(order.time , "%H:%M:%S").time() < datetime(2022, 2, 2, 16, 0, 0).time())

        print("Orders in CT passed")

        for order in ca:
            self.assertIsInstance(order, Order)
            self.assertTrue(datetime.strptime(order.time , "%H:%M:%S").time() >= datetime(2022, 2, 2, 16, 0, 0).time())
        
        print("Orders after 16:00:00 passed")

if __name__ == '__main__':
    unittest.main()


