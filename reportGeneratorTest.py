import unittest


from reportGenerator import generate_client_report
# test for client report generator
# input client_report = {'A': {'SIA': 2600.0}, 'B': {'SIA': -6200.0}, 'C': {'SIA': 3600.0}, 'D': {}, 'E': {'SIA': 1600.0}}
class TestClientReport(unittest.TestCase):
    def test_client_report(self):
        client_report = {
            'client1': {
                'instrument1': 100,
                'instrument2': -50
            },
            'client2': {
                'instrument1': 200,
                'instrument3': 150
            }
        }

        expected_output = [
            ['client1', 'instrument1', 100],
            ['client1', 'instrument2', -50],
            ['client2', 'instrument1', 200],
            ['client2', 'instrument3', 150]
        ]

        # Call the function
        result = generate_client_report(client_report)

        # Assert the output
        self.assertEqual(result, expected_output)

if __name__ == '__main__':
    unittest.main()



