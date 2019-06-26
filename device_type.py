# Generic modules
import csv
import requests
import time
# Meraki specific module
import meraki as m

# Global variables
apikey = 'API-KEY-HERE'
orgId = 'Organization_ID_Here'
device_type = 'Z'  # This can be MX, or Z as this is meant for Appliances
# Going to create a file, and timestamp it
timestr = time.strftime("%Y-%m-%d-%H%M%S")
# Filename with timestamp
file_name = 'device_status_'+timestr+'.csv'

def get_inventory():
    # First grab a list of the device in the inventory
    inventory = m.getorginventory(apikey, orgId, suppressprint=True)
    # Lets return our results back to the main function
    return inventory        

def filter_devices(dataset, filter=None):
    if filter is None:
        print('Must specify a device_type to filter against')
        sys.exit(1)
    # Create a new list to hold the filtered results
    filtered_data = []
    # Lets loop through the full inventory and find the specific device type we want
    # and add it to 'filtered_data' list.
    for device in dataset:
        if device_type in device['model']:
            filtered_data.append(device)
    # Once we have looped through the dataset and filtered the data
    # lets send it back to the main function
    return filtered_data

def get_uplinks():
    # This will get ever devices uplink status and limit our API calls
    uplink_data = m.get_device_statuses(apikey, orgId, suppress_print=True)
    # Lets now return this data back to main
    return uplink_data

def find_matches(filtered_data, uplink_data):
    # Lets find matches and put the data into a single list
    results = []
    for filtered in filtered_data:
        for uplinks in uplink_data:
            # Lets find a match between filtered and uplinks
            if filtered['networkId'] == uplinks['networkId'] and 'wan1Ip' in uplinks:
                # If a match is found, lets add it to our new list
                results.append({'name': filtered['name'], \
                    'serial': filtered['serial'], \
                    'networkId': filtered['networkId'], \
                    'model': filtered['model'], \
                    'publicIp': filtered['publicIp'] ,\
                    'wan1Ip': uplinks['wan1Ip'], \
                    'usingCellularFailover' : uplinks['usingCellularFailover'], \
                    'status': uplinks['status']})
    # Lets return our new list
    return results

def output_to_csv(dataset):
    with open(file_name, 'a') as outcsv:
        writer = csv.writer(outcsv, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL, lineterminator='\n')
        writer.writerow(
                    ['Device Name', \
                    'Serial', \
                    'Network Id', \
                    'Device Model', \
                    'Public Ip', \
                    'WAN1 Ip', \
                    'Using Cellular', \
                    'Status']
                    )
        for item in dataset:
            writer.writerow(
                [item['name'], \
                item['serial'], \
                item['networkId'], \
                item['model'], \
                item['publicIp'], \
                item['wan1Ip'], \
                item['usingCellularFailover'], \
                item['status']
            ])

def print_stats(dataset):
    for device in dataset:
        if device['status'] == 'online':
            print('{},{},{}'.format(device['name'], device['publicIp'], device['wan1Ip']))


# This is our main function that will run in order
def main():
    # Lets run the 'get_inventory' functions
    inventory = get_inventory()
    # Now lets run the 'filter_devices' function to get specific data we want
    # 'filtered' will the data we specifically want and is return by the function
    # 'filter_devices' is our function, and requires two variables/data points
    # 'inventory' is the dataset we got back from 'get_inventory'
    # 'filter=device_type' is going to tell the function we only want devices of type X
    filtered = filter_devices(inventory, filter=device_type)
    # To limit API calls we will get a list of every devices uplink status
    uplinks = get_uplinks()
    # Now lets run the 'find_matches' function
    matches = find_matches(filtered, uplinks)
    # Now we will run 'output_to_csv'
    # This will take the matches and output it to a CSV file
    # You can commit the next line out if you don't want a CSV
    output_to_csv(matches)
    # Optional but print the devices online to terminal
    # You can commit the next line out if you don't want it printed out on the screen
    print_stats(matches)



main()