import argparse
import yagmail

parser = argparse.ArgumentParser(description='Set up iphone x pick up notifier')
parser.add_argument('-u', required = True, help='gmail username')
parser.add_argument('-p', required = True, help='gmail password')
args = parser.parse_args()

yagmail.register(vars(args)['u'], vars(args)['p'])