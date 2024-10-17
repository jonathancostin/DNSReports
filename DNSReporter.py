import os
import csv
import requests
import ipinfo

def main():
    # Grab keys
    api_key = os.getenv('DNS_TWISTER_API_KEY')
    if not api_key:
        print("API key not found")
        exit()
    
    access_token = os.getenv('IP_INFO_API')
    if not access_token:
        choice = input("Access Token not found for Geo Location. Continue? (Y/N): ").strip().upper()
        if choice == "N":
            exit()
        else:
            access_token = None  # Proceed without Geo Location data

    # Define output Directory
    output_dir = "Results"
    os.makedirs(output_dir, exist_ok=True)

    # Define Output path
    output_csv_file = os.path.join(output_dir, "DNSReport.csv")

    # Grab data and store
    resolved_data = get_resolved_data(api_key)
    if resolved_data:
        create_csv(resolved_data, output_csv_file, access_token)
        print("CSV report generated successfully.")
    else:
        print("No data to generate CSV.")

# Function for grabbing DNS Twister data
def get_resolved_data(api_key):
    url = f'https://subscriber-api.dnstwister.report/reports/resolved.json?auth={api_key}'
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Error fetching DNSTwister Data: {e}")
        return None

# Function for grabbing Geo Locations for each IP in IP list
def get_geo_location(ip_list, access_token):
    if not access_token:
        return {ip: {'country': 'Unknown'} for ip in ip_list}
    
    handler = ipinfo.getHandler(access_token)
    country_details = {}
    
    for ip_address in ip_list:
        try:
            details = handler.getDetails(ip_address)
            country_details[ip_address] = details.all
        except Exception as e:
            print(f"Error fetching Geo Location for {ip_address}: {e}")
            country_details[ip_address] = {'country': 'Unknown'}
        
    return country_details

def create_csv(resolved_data, output_file, access_token):
    # Extract IPs
    ip_list = []
    for item in resolved_data:
        for resolved_item in item.get('resolved', []):
            ip = resolved_item.get('ip')
            if ip:
                ip_list.append(ip)

    # Remove duplicate IPs
    ip_list = list(set(ip_list))

    # Get Geo Location details
    geo_details = get_geo_location(ip_list, access_token)

    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        # Write header
        writer.writerow(['Subscribed Domain', 'Domain', 'IP', 'MX Record Exists', 'Newly Monitored', 'Geo Location'])
        # Write data
        for item in resolved_data:
            subscribed_domain = item.get('subscribed_domain_ascii', '')
            for resolved_item in item.get('resolved', []):
                domain_ascii = resolved_item.get('domain_ascii', '')
                ip = resolved_item.get('ip', '')
                mx_record_exists = resolved_item.get('mx_record_exists', '')
                newly_monitored = resolved_item.get('newly_monitored', '')
                geo_info = geo_details.get(ip, {})
                geo_location = geo_info.get('country', 'Unknown')
                writer.writerow([subscribed_domain, domain_ascii, ip, mx_record_exists, newly_monitored, geo_location])

if __name__ == "__main__":
    main()
