# Generic modules
import requests
import time
import json
import meraki as m

# Global variables
apikey = 'PLACE-API-KEY-HERE'
orgId = 'PLACE-ORG-ID-HERE'
alert_template = {'defaultDestinations':{'emails':['foo@bar.com'],'allAdmins':True},'alerts':[{'type':'settingsChanged','enabled':True,'alertDestinations':{'emails':[],'allAdmins':True,'snmp':False},'filters"''':{}}]}

# First grab a list of the device in the inventory
networks = m.getnetworklist(apikey, orgId, suppressprint=True)

def update_alert_settings(networkId, alert_settings):
    headers = {
        'x-cisco-meraki-api-key': format(str(apikey)),
        'Content-Type': 'application/json'
    }
    putdata = json.dumps(alert_settings)
    puturl = '{0}/networks/{1}/alertSettings'.format(str(m.base_url), str(networkId))
    dashboard = requests.put(puturl, data=putdata, headers=headers)
    if dashboard.status_code == 200:
        return True
    else:
        return False


for network in networks:                                            # Going to loop through the inventory
    settings = m.getalertsettings(apikey, 
        network['id'],  
        suppressprint=True)                                         # Grab device settings for each Network
    for i in settings['alerts']:
        if i['type'] == 'settingsChanged':
            print('INFO: Settings changed is set to: {} for network {}'.format(str(i['enabled']), str(network['name'])))
            if i['enabled'] is False:
                push = update_alert_settings(network['id'], alert_template)
                if push == True:
                    print('INFO: Settings were pushed successfully')
                else:
                    print('WARN: Settings did not push successfully')
    time.sleep(0.3)                                                 # Sleep for ~300ms to avoid rate-limit

