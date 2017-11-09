import requests
import logging
import yagmail

APPLE_BASE_URL_STORE_AVAILABILITY = 'https://www.apple.com/shop/retail/pickup-message?pl=true&cppart=TMOBILE/US&parts.0=' 
APPLE_URL_LOCATION_EXTENSION = '&location=' 

logging.basicConfig(filename='availabilityLog.log',level=logging.DEBUG)
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)

def checkAvailibilityForModel(modelCode='MQAQ2LL/A', zipCode = '33308'):
	''' Checks the in store pick up availability for the modelcode and zipcode provided'''
	availability_url = APPLE_BASE_URL_STORE_AVAILABILITY + modelCode + APPLE_URL_LOCATION_EXTENSION + zipCode
	r = requests.get(availability_url)
	if r.status_code != requests.codes.ok:
		logger.error('Get request failed: URL = ' + availability_url)
		return
		
	jsonData = r.json()
	for store in jsonData['body']['stores']:
		#print store['storeName']
		if store['partsAvailability'][modelCode]['pickupDisplay'] == 'unavailable':
			logger.log(logging.INFO, store['storeName'] + ': unavailable')
		else:
			logger.log(logging.INFO, store['storeName'] + ': Available!')

			
def sendEmail():
	yag = yagmail.SMTP('sidautoemail')
	yag.send(to = 'sid.bidasaria@gmail.com', contents = 'Test')
			
def main():
	#checkAvailibilityForModel()
	sendEmail()
if __name__ == "__main__":
    main()