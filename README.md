# Reconciliation

Reconciles position data and transactions. See included `recon.in` file for example input file.

## Requirements

* Python 3.6

## Usage

Clone this repository, then invoke the program using one of the following:

* `$ python main.py`
    - Will look for `recon.in` in the parent folder and write to `recon.out` in the parent folder

* `$ python main.py /path/to/recon.in`
    - Will look for the input file at the specified path and write to `recon.out` in the parent folder

* `$ python main.py /path/to/recon.in /path/to/recon.out`
    - Will look for the input file at the first specified path and write to the second specified path

## Other Notes

* Run `$ python -m unittest discover` to run test suite


