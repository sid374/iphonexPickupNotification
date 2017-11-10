import requests
import logging
import yagmail
import sys

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

def checkAvailibilityForModel(modelCode='MQAQ2LL/A', zipCode = '33308', description= 'iphone' ):
	''' Checks the in store pick up availability for the modelcode and zipcode provided'''
	availability_url = APPLE_BASE_URL_STORE_AVAILABILITY + modelCode + APPLE_URL_LOCATION_EXTENSION + zipCode
	r = requests.get(availability_url)
	if r.status_code != requests.codes.ok:
		logger.error('Get request failed: URL = ' + availability_url)
		return
		
	jsonData = r.json()
	for store in jsonData['body']['stores']:
		#print store['storeName']
		if store['partsAvailability'][modelCode]['pickupDisplay'] == 'unavailable' or store['partsAvailability'][modelCode]['pickupSearchQuote'] == 'Currently unavailable':
			logger.log(logging.INFO, store['storeName'] + ': ' + description + ' unavailable' + ' Zip: ' + zipCode)
		else:
			logger.log(logging.INFO, store['storeName'] + ': ' + description + ' AVAILABLE!' + ' Zip: ' + zipCode)
			logger.log(logging.DEBUG, store)
			sendEmail("Phone {0} available at {1} {2}".format(description, store['storeName'], zipCode))



def sendEmail(content='Test'):
	try:
		yag = yagmail.SMTP('sidautoemail')
		yag.send(to = 'sid.bidasaria@gmail.com', contents = content)
	except:
		e = sys.exc_info()[0]
		logger.error('Sending email failed')



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
	sendEmail("Job Finished.")

			
def main():
	checkAvailability()

if __name__ == "__main__":
    main()
