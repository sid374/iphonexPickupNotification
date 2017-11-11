import argparse
import yagmail

parser = argparse.ArgumentParser(description='Set up iphone x pick up notifier')
parser.add_argument('--u', required = False, help='gmail username')
parser.add_argument('--p', required = False, help='gmail password')

args = parser.parse_args()

if args.u is not None and args.p is not None:
	yagmail.register(vars(args)['u'], vars(args)['p'])
