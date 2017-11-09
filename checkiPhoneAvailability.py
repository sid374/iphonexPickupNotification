import requests

APPLE_BASE_URL_STORE_AVAILABILITY = 'https://www.apple.com/shop/retail/pickup-message?pl=true&cppart=TMOBILE/US&parts.0=' 
APPLE_URL_LOCATION_EXTENSION = '&location=' 


def checkAvailibilityForModel(modelCode='MQAQ2LL/A', zipCode = '33308'):
	''' Checks the in store pick up availability for the modelcode and zipcode provided'''
	availability_url = APPLE_BASE_URL_STORE_AVAILABILITY + modelCode + APPLE_URL_LOCATION_EXTENSION + zipCode
	r = requests.get(availability_url)
	if r.status_code != requests.codes.ok:
		print('Get Request Failed')
		return
		
	jsonData = r.json()
	for store in jsonData['body']['stores']:
		print store['storeName']
		if store['partsAvailability'][modelCode]['pickupDisplay'] == 'unavailable':
			print 'unavailable'
		else:
			print 'available!'

def main():
	checkAvailibilityForModel()
	
if __name__ == "__main__":
    main()