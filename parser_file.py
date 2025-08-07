import argparse

def create_parser():
    parser = argparse.ArgumentParser(description='parser')
    parser.add_argument('-f','--file', nargs='+', help='Files for processing', required=True)
    parser.add_argument('-r', '--report', help='Enter report', required=False)
    parser.add_argument('-d', '--date',nargs='+', help='Enter day', required=False)
    return parser
