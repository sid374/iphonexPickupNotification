import argparse
import yagmail
import os

parser = argparse.ArgumentParser(description='Set up iphone x pick up notifier')
parser.add_argument('--u', required = False, help='gmail username')
parser.add_argument('--p', required = False, help='gmail password')
parser.add_argument('--twilioSid', required = False, help='twilio sid')
parser.add_argument('--twilioAuth', required = False, help='twilio auth')
parser.add_argument('--twilioPhone', required = False, help='twilio phone')


args = parser.parse_args()

if args.u is not None and args.p is not None:
	yagmail.register(vars(args)['u'], vars(args)['p'])

if args.twilioSid is not None:
	os.environ['twilioSid'] = args.twilioSid

if args.twilioAuth is not None:
	os.environ['twilioAuth'] = args.twilioAuth

if args.twilioPhone is not None:
	os.environ['twilioPhone'] = args.twilioPhone