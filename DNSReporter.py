import os
import csv
import requests
import ipinfo

# Grab keys
api_key = os.getenv('DNS_TWISTER_API_KEY')
if api_key is None:
    print("API key not found")
    exit()
access_token = os.getenv('IP_INFO_API')
if access_token is None:
    choice = input("Access Token not found for Geo Location. Continue? (Y/N)")
    if choice == "N":
        exit()

# Define output Directory
output_dir = "Results"
os.makedirs(output_dir, exist_ok=True)

# Deine Output path
output_csv_file = os.path.join(output_dir, "DNSReport.csv")

# Function for grabbing DNS Twister data
def GetResolvedData(api_key):
    url = f'https://subscriber-api.dnstwister.report/reports/resolved.json?auth={api_key}'
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error fetching DNSTwister Data: {response.status_code} - {response.text}")
        return None

# Grab data and store
resolvedData = GetResolvedData(api_key)

# Init ip list
ip_list = []

# Function for grabbing Geo Locations for each IP in IP list
def getGeoLocation(ip_list):
    handler = ipinfo.getHandler(access_token)
    country_details = {}  
    
    for ip_address in ip_list:
        details = handler.getDetails(ip_address)
        country_details[ip_address] = details.all 
        
    return country_details


country_details_dict = getGeoLocation(ip_list)

def createCSV(resolvedData, output_file):
    
    ip_list = []
    for item in resolvedData:
        for resolved_item in item.get('resolved', []):
            ip = resolved_item.get('ip', '')
            if ip:
                ip_list.append(ip)

    
    geo_details = getGeoLocation(ip_list)
    
    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        # Write header
        writer.writerow(['Subscribed Domain', 'Domain', 'IP', 'MX Record Exists', 'Newly Monitored', 'Geo Location'])
        # Write data
        for item in resolvedData:
            subscribed_domain = item.get('subscribed_domain_ascii', '')
            for resolved_item in item.get('resolved', []):
                domain_ascii = resolved_item.get('domain_ascii', '')
                ip = resolved_item.get('ip', '')
                mx_record_exists = resolved_item.get('mx_record_exists', '')
                newly_monitored = resolved_item.get('newly_monitored', '')
                geo_location = geo_details.get(ip, {}).get('country', '')
                writer.writerow([subscribed_domain, domain_ascii, ip, mx_record_exists, newly_monitored, geo_location])
                
    return ip_list


if resolvedData:
    createCSV(resolvedData, output_csv_file)
    ip_list = createCSV(resolvedData, output_csv_file)
    print("CSV report generated successfully.")














