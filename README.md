# iphonexPickupNotification
Checks if the iphone x is available for pickup in  a store near you!

Sends an email and text if your desired iphone is available in a location near you or a friend!

How to use:
1. Start with configuring the config.ini file

  a. If you want to receive text messages, fill out the Twilio details. Otherwise delete the TWILIO section from the ini file
  
  b. Fill out the Notifications sections with a list of emails you want to notify, phone numbers you want to text and zip codes you want to search in
  
  c. You can configure Urgent Notifications if you want: Urgent notifications gives you the flexibiity of receiving notifications via text/email only if specific zip codes or models (64gb/256gb) are available for pick up. This is handy if you want to monitor multiple zip codes through the log files but only want to receive notifications for the zip codes near you!
  
  
2. Setup a cron job to run this script as often as you like!

3. Profit (Or loss.. depends on where you stand)
