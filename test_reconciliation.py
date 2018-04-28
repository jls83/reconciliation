import unittest

from reconciliation import *

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
    happy_path_input = [
        'AAPL 100',
        'GOOG 200',
        'SP500 175.75',
        'Cash 1000'
    ]

    def test_position_create_happy_path_return_type(self):
        result_dict = position_dict_create(self.happy_path_input)
        self.assertIsInstance(result_dict, dict)

