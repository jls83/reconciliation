import unittest
import copy

from decimal import Decimal

from reconciliation.reconciliation import *


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


class TestPositionUpdate(unittest.TestCase):
    initial_positions = {
        'AAPL': Decimal(100),
        'GOOG': Decimal(200),
        'SP500': Decimal(175.75),
        'Cash': Decimal(1000)
    }

    transaction_list = [
        ('AAPL', 'SELL', '100', '30000'),
        ('GOOG', 'BUY', '10', '10000'),
        ('Cash', 'DEPOSIT', '0', '1000'),
        ('Cash', 'FEE', '0', '50'),
        ('GOOG', 'DIVIDEND', '0', '50'),
        ('TD', 'BUY', '100', '10000')
    ]

    def test_position_update_sell(self):
        single_transaction = ('AAPL', 'SELL', '100', '30000')
        new_positions = copy.deepcopy(self.initial_positions)

        symbol = single_transaction[0]
        shares = Decimal(single_transaction[2])
        amount = Decimal(single_transaction[3])

        position_update(single_transaction, new_positions)

        share_change = self.initial_positions[symbol] - shares == new_positions[symbol]
        cash_change = self.initial_positions['Cash'] + amount == new_positions['Cash']

        self.assertTrue(share_change and cash_change)

    def test_position_update_buy(self):
        single_transaction = ('GOOG', 'BUY', '10', '10000')
        new_positions = copy.deepcopy(self.initial_positions)

        symbol = single_transaction[0]
        shares = Decimal(single_transaction[2])
        amount = Decimal(single_transaction[3])

        position_update(single_transaction, new_positions)

        share_change = self.initial_positions[symbol] + shares == new_positions[symbol]
        cash_change = self.initial_positions['Cash'] - amount == new_positions['Cash']

        self.assertTrue(share_change and cash_change)

    def test_position_update_deposit(self):
        single_transaction = ('Cash', 'DEPOSIT', '0', '1000')
        new_positions = copy.deepcopy(self.initial_positions)

        amount = Decimal(single_transaction[3])

        position_update(single_transaction, new_positions)

        cash_change = self.initial_positions['Cash'] + amount == new_positions['Cash']

        self.assertTrue(cash_change)

    def test_position_update_fee(self):
        single_transaction = ('Cash', 'FEE', '0', '50')
        new_positions = copy.deepcopy(self.initial_positions)

        amount = Decimal(single_transaction[3])

        position_update(single_transaction, new_positions)

        cash_change = self.initial_positions['Cash'] - amount == new_positions['Cash']

        self.assertTrue(cash_change)

    def test_position_update_dividend(self):
        single_transaction = ('GOOG', 'DIVIDEND', '0', '50')
        new_positions = copy.deepcopy(self.initial_positions)

        symbol = single_transaction[0]
        shares = Decimal(single_transaction[2])
        amount = Decimal(single_transaction[3])

        position_update(single_transaction, new_positions)

        share_change = self.initial_positions[symbol] - shares == new_positions[symbol]
        cash_change = self.initial_positions['Cash'] + amount == new_positions['Cash']

        self.assertTrue(share_change and cash_change)


class TestReconcilePositions(unittest.TestCase):
    initial_positions = {
        'AAPL': Decimal(100),
        'GOOG': Decimal(200),
        'SP500': Decimal(175.75),
        'Cash': Decimal(1000)
    }

    def test_reconcile_positions_duplicate_inputs(self):
        """ Should return an empty dict """
        new_positions = copy.deepcopy(self.initial_positions)
        result_dict = reconcile_positions(self.initial_positions, new_positions)
        self.assertEqual(result_dict, {})

    def test_reconcile_positions_empty_second_input(self):
        """ Should return a dict with 'negated' values """
        new_positions = {}
        expected_result = {k: (self.initial_positions[k] * -1) for k in self.initial_positions}
        result_dict = reconcile_positions(self.initial_positions, new_positions)
        self.assertEqual(result_dict, expected_result)

    def test_reconcile_positions_single_element_difference(self):
        """ Should return a dict with a single key/value pair """
        new_positions = {
            'AAPL': Decimal(100),
            'GOOG': Decimal(250),
            'SP500': Decimal(175.75),
            'Cash': Decimal(1000)
        }

        expected_result = {
            'GOOG': Decimal(50)
        }

        result_dict = reconcile_positions(self.initial_positions, new_positions)
        self.assertEqual(result_dict, expected_result)

    def test_reconcile_positions_multi_element_difference(self):
        """ Should return a dict with multiple key/value pairs """
        new_positions = {
            'AAPL': Decimal(10),
            'GOOG': Decimal(250),
            'SP500': Decimal(175.75),
            'Cash': Decimal(12000)
        }

        expected_result = {
            'AAPL': Decimal(-90),
            'GOOG': Decimal(50),
            'Cash': Decimal(11000)
        }

        result_dict = reconcile_positions(self.initial_positions, new_positions)
        self.assertEqual(result_dict, expected_result)
