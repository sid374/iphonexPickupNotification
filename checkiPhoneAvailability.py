import requests
import logging
import yagmail
import sys
import configparser
from twilio.rest import Client


APPLE_BASE_URL_STORE_AVAILABILITY = 'https://www.apple.com/shop/retail/pickup-message?pl=true&cppart=TMOBILE/US&parts.0=' 
APPLE_URL_LOCATION_EXTENSION = '&location=' 

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

fileHandler = logging.FileHandler("availabilityLog.log")
fileHandler.setLevel(logging.DEBUG)
fileHandler.setFormatter(formatter)
logger.addHandler(fileHandler)

ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
ch.setFormatter(formatter)
logger.addHandler(ch)

config = configparser.ConfigParser()
config.read('config.ini')

def checkAvailibilityForModel(modelCode='MQAQ2LL/A', zipCode = '33308', description= 'iphone' ):
	''' Checks the in store pick up availability for the modelcode and zipcode provided'''
	availability_url = APPLE_BASE_URL_STORE_AVAILABILITY + modelCode + APPLE_URL_LOCATION_EXTENSION + zipCode
	r = requests.get(availability_url)
	if r.status_code != requests.codes.ok:
		logger.error('Get request failed: URL = ' + availability_url)
		return
		
	jsonData = r.json()
	for store in jsonData['body']['stores']:
		if store['partsAvailability'][modelCode]['pickupDisplay'] == 'unavailable' or store['partsAvailability'][modelCode]['pickupSearchQuote'] == 'Currently unavailable':
			logger.log(logging.INFO, store['storeName'] + ': ' + description + ' unavailable' + ' Zip: ' + zipCode)
		else:
			logger.log(logging.INFO, store['storeName'] + ': ' + description + ' AVAILABLE!' + ' Zip: ' + zipCode)
			logger.log(logging.DEBUG, store)
			if zipCode == '33308' and '64' in description:
				sendText(content = "Phone {0} available at {1} {2}".format(description, store['storeName'], zipCode))
				sendEmail(content = "Phone {0} available at {1} {2}".format(description, store['storeName'], zipCode), sub = "Woohoo! in {0}".format(zipCode))
			if zipCode == '33308' or '64' in description:
				sendEmail(content = "Phone {0} available at {1} {2}".format(description, store['storeName'], zipCode), sub = "Urgent in {0}".format(zipCode))
			else:
				#too much spam.. commenting
				#sendEmail("Phone {0} available at {1} {2}".format(description, store['storeName'], zipCode), sub = "Found in {0}".format(zipCode))
				pass



def sendEmail(content='Test', sub = ''):
	try:
		yag = yagmail.SMTP('sidautoemail')
		yag.send(to = 'sid.bidasaria@gmail.com', contents = content, subject = sub)
		yag.send(to = 'anupriya.bidasaria1996@gmail.com', contents = content, subject = sub)
	except:
		e = sys.exc_info()[0]
		logger.error('Sending email failed')


def sendText(to="4017495246", content = 'iphonex notification'):
	if 'Twilio' not in config.sections():
		return

	if config.has_option('Twilio', 'sid') and config.has_option('Twilio', 'auth') and config.has_option('Twilio', 'outgoingPhone'):
		account_sid = config.get('Twilio', 'sid')
		auth_token = config.get('Twilio', 'auth')
		phone = config.get('Twilio', 'outgoingPhone')

		client = Client(account_sid, auth_token)
		message = client.messages.create(
		    to="+14017495246", 
		    from_=  phone,
		    body=content)


def checkAvailability():
	SPACEGRAY_64 = {'modelCode':'MQAQ2LL/A', 'description':'SPACE GRAY 64'}
	SILVER_64 = {'modelCode':'MQAR2LL/A', 'description':'SILVER 64'}
	SPACEGRAY_256 = {'modelCode':'MQAU2LL/A', 'description':'SPACE GRAY 256'}
	SILVER_256 = {'modelCode' : 'MQAV2LL/A', 'description':'SILVER 256'}

	modelList = [SPACEGRAY_64, SILVER_64, SPACEGRAY_256, SILVER_256]
	zipcodeList = ['33308', '94116', '98112']

	for model in modelList:
		for zipcode in zipcodeList:
			checkAvailibilityForModel(zipCode = zipcode, **model)

			
def main():
	checkAvailability()

if __name__ == "__main__":
    main()
