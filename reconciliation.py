"""
    1. Will there always be an entry for "Cash" in D0-POS?
    2. Should we account for dividends from stocks not in D0-POS?
    3. Does the output order matter?

"""
from decimal import *


def read_recon_in(in_file):
    """ Reads the input file, then returns lists of lines for each group of
        input data.

        Finds the appropriate headers as described in the file specification,
        then splits out the position data and transaction data.

        Parameters:
            in_file (str): Path to the input file
        Returns:
            d0_pos, d1_trn, d1_pos: Lists of strings containing position data
                (d0_pos, d1_pos) and transaction data (d1_trn)
    """

    with open(in_file, 'r') as f:
        lines = [line.rstrip() for line in f]

    d0_pos_header = lines.index('D0-POS')
    d1_trn_header = lines.index('D1-TRN')
    d1_pos_header = lines.index('D1-POS')

    d0_pos = lines[d0_pos_header + 1:d1_trn_header - 1]
    d1_trn = lines[d1_trn_header + 1:d1_pos_header - 1]
    d1_pos = lines[d1_pos_header + 1:]

    return d0_pos, d1_trn, d1_pos


def write_recon_out(in_dict, out_file):
    """ Writes data from a position dictionary to the specified output file.

        NOTE: Will overwrite output file; use caution

        Parameters:
            in_dict (dict): Dictionary containing position data
            out_file (str): Path to file to write to
        Returns:
            None
    """

    position_list = ['{} {}'.format(k, in_dict[k]) for k in in_dict]
    with open(out_file, 'w') as f:
        for p in position_list:
            f.write(p + '\n')


def position_dict_create(in_list):
    """ Creates a dictionary containing position data from a list of strings.

        Parameters:
            in_list (List<str>): List of strings describing daily position data
        Returns:
            (dict): Position data; keys are symbols (incl. 'Cash'), values are
                share amounts or cash-on-hand
    """

    positions_split = [p.split(' ') for p in in_list]
    return {i[0]: Decimal(i[1]) for i in positions_split}


def transaction_data_list_create(in_trans_list):
    """ Returns tuple of transaction data

        Parameters:
            in_trans_list (List<str>): List of strings describing transactions
        Returns:
            (List<tuple>): List of tuples containing transaction data in the
                following format:
                    symbol = tuple[0] (e.g. 'AAPL', 'Cash')
                    type = tuple[1] (e.g. 'SELL', 'DIVIDEND')
                    shares = tuple[2] (Decimal value of shares to sell/buy; 0
                        for cash transactions)
                    amount = tuple[3] (Decimal value of cash exchanged)
    """

    return tuple(t.split(' ') for t in in_trans_list)


def position_update(in_transaction, position_dict):
    """ Updates the positions in `position_dict` using the data in
        `in_transaction`

        Parameters:
            in_transaction (tuple): Transaction data; see `transaction_data_list_create`
            position_dict (dict): Position data; see `position_dict_create`
        Returns:
            None
    """

    trans_symbol = in_transaction[0]
    trans_type = in_transaction[1]
    trans_shares = Decimal(in_transaction[2])
    trans_amount = Decimal(in_transaction[3])

    if trans_type in ['DEPOSIT', 'DIVIDEND', 'SELL']:  # share loss and/or cash gain
        trans_shares *= -1
    elif trans_type in ['FEE', 'BUY']:  # share gain and/or cash loss
        trans_amount *= -1
    else:  # We should not end up here, but just in case...
        raise ValueError('{} is an incompatible transaction type'.format(trans_type))

    position_dict['Cash'] += trans_amount
    try:
        position_dict[trans_symbol] += trans_shares
    except KeyError:
        position_dict[trans_symbol] = trans_shares


def bulk_position_update(in_trans_list, position_dict):
    """ Runs `position_update` in bulk

        Parameters:
            in_trans_list (List<tuple>): List of transaction data; see
                `transaction_data_list_create` and `position_update`
            position_dict (dict): Position data; see `position_dict_create`
        Returns:
            None
    """

    for trans in in_trans_list:
        position_update(trans, position_dict)


def reconcile_positions(pos_dict_1, pos_dict_2):
    """ Reconciles two position dictionaries into a new dictionary.

        Parameters:
            pos_dict_1 (dict): Position data post-transactions
            pos_dict_2 (dict): Position data reported by "bank"

        Returns:
            res (dict): Differences in reported values for each symbol (incl. cash)
                from each passed-in position data.
    """

    res = {}

    all_keys = list(pos_dict_1.keys()) + list(pos_dict_2.keys())

    for symbol in all_keys:
        if symbol not in pos_dict_2: # "left" keys
            symbol_diff = pos_dict_1[symbol] * -1
        elif symbol not in pos_dict_1: # "right" keys
            symbol_diff = pos_dict_2[symbol]
        else: # "middle" keys
            symbol_diff = pos_dict_2[symbol] - pos_dict_1[symbol]

        if symbol_diff != 0:
            res[symbol] = symbol_diff

    return res


def reconcile_positions_2(pos_dict_1, pos_dict_2):
    res = {}

    dict_1_keys = set(pos_dict_1.keys())
    dict_2_keys = set(pos_dict_2.keys())

    left_keys = dict_1_keys.difference(dict_2_keys) # stuff i have that wasn't reported
    middle_keys = dict_1_keys.intersection(dict_2_keys) # stuff i have that was reported
    right_keys = dict_2_keys.difference(dict_1_keys) # stuff i don't have that was reported

    for symbol in left_keys:
        symbol_diff = pos_dict_1[symbol] * -1
        if symbol_diff != 0:
            res[symbol] = symbol_diff

    for symbol in middle_keys:
        symbol_diff = pos_dict_2[symbol] - pos_dict_1[symbol]
        if symbol_diff != 0:
            res[symbol] = symbol_diff

    for symbol in right_keys:
        symbol_diff = pos_dict_2[symbol]
        if symbol_diff != 0:
            res[symbol] = symbol_diff

    return res


def get_symbol_value_reconcile(symbol, position_dict):
    try:
        val = position_dict[symbol]
    except KeyError:
        val = 0
    return val


def reconcile_positions_3(pos_dict_1, pos_dict_2):
    res = {}

    all_keys = list(pos_dict_1.keys()) + list(pos_dict_2.keys())

    for symbol in all_keys:
        d0_val = get_symbol_value_reconcile(symbol, pos_dict_1)
        d1_val = get_symbol_value_reconcile(symbol, pos_dict_2)
        diff = d1_val - d0_val
        if diff != 0:
            res[symbol] = diff

    return res


if __name__ == '__main__':
    d0_pos, d1_trn, d1_pos = read_recon_in('recon.in')
    d0_pos_dict = position_dict_create(d0_pos)
    d1_trn_list = transaction_data_list_create(d1_trn)
    bulk_position_update(d1_trn_list, d0_pos_dict)
    d1_pos_dict = position_dict_create(d1_pos)
    reconcile_dict = reconcile_positions(d0_pos_dict, d1_pos_dict)
    write_recon_out(reconcile_dict, 'recon.out')

