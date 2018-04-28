import unittest

from decimal import Decimal

from reconciliation.reconciliation import *

d0_pos_test = [
    'AAPL 100',
    'GOOG 200',
    'SP500 175.75',
    'Cash 1000'
]

d1_trn_test = [
    'AAPL SELL 100 30000',
    'GOOG BUY 10 10000',
    'Cash DEPOSIT 0 1000',
    'Cash FEE 0 50',
    'GOOG DIVIDEND 0 50',
    'TD BUY 100 10000'
]

d1_pos_test = [
    'GOOG 220',
    'SP500 175.75',
    'Cash 20000',
    'MSFT 10'
]


class TestPositionCreate(unittest.TestCase):
    position_input = [
        'AAPL 100',
        'GOOG 200',
        'SP500 175.75',
        'Cash 1000'
    ]

    expected_output = {
        'AAPL': Decimal(100),
        'GOOG': Decimal(200),
        'SP500': Decimal(175.75),
        'Cash': Decimal(1000)
    }

    def test_position_create_happy_path_return_type(self):
        result_dict = position_dict_create(self.position_input)
        self.assertIsInstance(result_dict, dict)

    def test_position_create_happy_path_return_values(self):
        result_dict = position_dict_create(self.position_input)
        self.assertEqual(result_dict, self.expected_output)


class TestTransactionDataListCreate(unittest.TestCase):
    transaction_input = [
        'AAPL SELL 100 30000',
        'GOOG BUY 10 10000',
        'Cash DEPOSIT 0 1000',
        'Cash FEE 0 50',
        'GOOG DIVIDEND 0 50',
        'TD BUY 100 10000'
    ]

    expected_output = [
        ('AAPL', 'SELL', '100', '30000'),
        ('GOOG', 'BUY', '10', '10000'),
        ('Cash', 'DEPOSIT', '0', '1000'),
        ('Cash', 'FEE', '0', '50'),
        ('GOOG', 'DIVIDEND', '0', '50'),
        ('TD', 'BUY', '100', '10000')
    ]

    def test_transaction_data_list_create_return_type(self):
        transaction_list = transaction_data_list_create(self.transaction_input)
        self.assertIsInstance(transaction_list, list)

    def test_transaction_data_list_create_return_values(self):
        transaction_list = transaction_data_list_create(self.transaction_input)
        self.assertEqual(transaction_list, self.expected_output)






