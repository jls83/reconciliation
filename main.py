from reconciliation.reconciliation import *

if __name__ == '__main__':
    d0_pos, d1_trn, d1_pos = read_recon_in('recon.in')
    d0_pos_dict = position_dict_create(d0_pos)
    d1_trn_list = transaction_data_list_create(d1_trn)
    bulk_position_update(d1_trn_list, d0_pos_dict)
    d1_pos_dict = position_dict_create(d1_pos)
    reconcile_dict = reconcile_positions(d0_pos_dict, d1_pos_dict)
    write_recon_out(reconcile_dict, 'recon.out')
