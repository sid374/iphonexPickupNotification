import requests
import logging
import yagmail
import sys
import configparser
import json
from twilio.rest import Client

APPLE_BASE_URL_STORE_AVAILABILITY_ATT = 'https://www.apple.com/shop/retail/pickup-message?pl=true&cppart=ATT/US&parts.0=' 
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

			#If the urgentonly flag is on in the config file then do this
			if config.getboolean('Notifications', 'urgentOnly') and isUrgent(zipC = zipCode, modelDescription = description):
				sendText(content = "Phone {0} available at {1} {2}".format(description, store['storeName'], zipCode))
				sendEmail(content = "Phone {0} available at {1} {2}".format(description, store['storeName'], zipCode), sub = "Woohoo! in {0}".format(zipCode))
			elif config.getboolean('Notifications', 'urgentOnly') == False:
				sendText(content = "Phone {0} available at {1} {2}".format(description, store['storeName'], zipCode))
				sendEmail(content = "Phone {0} available at {1} {2}".format(description, store['storeName'], zipCode), sub = "Woohoo! in {0}".format(zipCode))
			else:
				#too much spam.. commenting
				#sendEmail("Phone {0} available at {1} {2}".format(description, store['storeName'], zipCode), sub = "Found in {0}".format(zipCode))
				pass


def isUrgent(zipC, modelDescription):
	'''checks if the given zipcode and model are specified in the urgent section of the config file'''
	urgentZips = []
	urgentModels = []
	#if urgentZipCodes or urgentModels is not defined in the config file, we treat ALL as urgent!
	if not config.has_option('UrgentNotification','urgentZipCodes'):
		urgentZips = json.loads(config.get("Notifications","zipCodeList"))
	else:
		urgentZips = json.loads(config.get("UrgentNotification","urgentZipCodes"))

	if not config.has_option('UrgentNotification','urgentModels'):
		urgentModels = ["64", "256"]
	else:
		urgentModels = json.loads(config.get("UrgentNotification","urgentModels"))

	if zipC in urgentZips:
		return True

	for model in urgentModels:
		if model in modelDescription:
			return True 

	return False

def sendEmail(content='Test', sub = ''):
	if not config.has_option('Notifications','phoneList'):
		return

	emailList = json.loads(config.get("Notifications","emailList"))
	try:
		yag = yagmail.SMTP('sidautoemail')
		for email in emailList:
			yag.send(to = email, contents = content, subject = sub)
	except:
		e = sys.exc_info()[0]
		logger.error('Sending email failed')


def sendText(content = 'iphonex notification'):
	if 'Twilio' not in config.sections() or not config.has_option('Notifications','phoneList'):
		return

	if config.has_option('Twilio', 'sid') and config.has_option('Twilio', 'auth') and config.has_option('Twilio', 'outgoingPhone'):
		account_sid = config.get('Twilio', 'sid')
		auth_token = config.get('Twilio', 'auth')
		twilPhone = config.get('Twilio', 'outgoingPhone')

		client = Client(account_sid, auth_token)

		phoneList = json.loads(config.get("Notifications","phoneList"))

		for phone in phoneList:
			message = client.messages.create(
			    to=phone, 
			    from_=  twilPhone,
			    body=content)


def checkAvailability():
	SPACEGRAY_64 = {'modelCode':'MQAQ2LL/A', 'description':'SPACE GRAY 64'}
	SILVER_64 = {'modelCode':'MQAR2LL/A', 'description':'SILVER 64'}
	SPACEGRAY_256 = {'modelCode':'MQAU2LL/A', 'description':'SPACE GRAY 256'}
	SILVER_256 = {'modelCode' : 'MQAV2LL/A', 'description':'SILVER 256'}

	SPACEGRAY_64_ATT = {'modelCode':'MQAJ2LL/A', 'description':'SPACE GRAY 64 ATT'}
	SILVER_64_ATT = {'modelCode':'MQAK2LL/A', 'description':'SILVER 64 ATT'}
	SPACEGRAY_256_ATT = {'modelCode':'MQAM2LL/A', 'description':'SPACE GRAY 256 ATT'}
	SILVER_256_ATT = {'modelCode':'MQAN2LL/A', 'description':'SILVER 256 ATT'}

	modelList = [SPACEGRAY_64, SILVER_64, SPACEGRAY_256, SILVER_256]

	zipcodeList = json.loads(config.get("Notifications","zipCodeList"))

	for model in modelList:
		for zipcode in zipcodeList:
			checkAvailibilityForModel(zipCode = zipcode, **model)
			
def main():
	checkAvailability()

if __name__ == "__main__":
    main()
