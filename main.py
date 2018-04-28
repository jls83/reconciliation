import sys

from reconciliation.reconciliation import *

if __name__ == '__main__':
    if len(sys.argv) == 3:
        in_path = sys.argv[1]
        out_path = sys.argv[2]
    elif len(sys.argv) == 1:
        in_path = 'recon.in'
        out_path = 'recon.out'
    else:
        raise ValueError('Incorrect number of arguments. Expected 0 or 2; got {}'.format(len(sys.argv) - 1))

    d0_pos, d1_trn, d1_pos = read_recon_in(in_path)

    d0_pos_dict = position_dict_create(d0_pos)
    d1_trn_list = transaction_data_list_create(d1_trn)

    bulk_position_update(d1_trn_list, d0_pos_dict)

    d1_pos_dict = position_dict_create(d1_pos)

    reconcile_dict = reconcile_positions(d0_pos_dict, d1_pos_dict)

    write_recon_out(reconcile_dict, out_path)
