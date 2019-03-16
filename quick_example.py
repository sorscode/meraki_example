# Generic modules
import requests
import time
import meraki as m

# Global variables
apikey = 'API-KEY-HERE'
orgId = 'Organization_ID_Here'

# First grab a list of the device in the inventory
inventory = m.getorginventory(apikey, orgId, suppressprint=True)

for network in inventory:                                           # Going to loop through the inventory
    if network['networkId'] is not None:                            # Make sure that the device is associated with a network
        single_device = m.getdevicedetail(apikey, 
            network['networkId'], 
            network['serial'], 
            suppressprint=True)                                     # Grab a each devices details one at a time
        print('Device Name is {} with a serial number of {} and is a Meraki {}'.format(single_device['name'], 
            single_device['serial'], single_device['model']))       # Print each devices details
        time.sleep(0.3)                                             # Sleep for ~300ms to avoid rate-limit

for uplink in inventory:                                            # Going to loop through the inventory
    if uplink['networkId'] is not None:                             # Make sure that the device is associated with a network
        device_uplink = m.getdeviceuplink(apikey, 
            uplink['networkId'], 
            uplink['serial'], 
            suppressprint=True)                                     # Grab a each devices uplink details one at a time
        for i in device_uplink:                                     # Some device might have multiple uplinks so lets loop through each
            if 'ip' in i:                                           # Make sure there is an IP assigned
                print('Device Name is {} and its uplink status is {}, and its uplink IP is {}'.format(uplink['name'], 
                    i['status'], i['ip']))                          # Print the results for each device
        time.sleep(0.3)                                             # Sleep for ~300ms to avoid rate-limit
    