---

# DNS Report Generator

This Python script fetches DNS resolution data from the **DNSTwister** API and generates a comprehensive CSV report. Optionally, it can also retrieve geolocation information for each resolved IP address using the **IPinfo** API.

## Table of Contents

- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Output](#output)
- [Error Handling](#error-handling)
- [Dependencies](#dependencies)
- [License](#license)
- [Contact](#contact)

## Features

- **Fetches DNS Resolution Data**: Retrieves data from DNSTwister API based on your subscribed domains.
- **Generates CSV Report**: Creates a CSV file containing detailed information about each resolved domain.
- **Optional Geolocation Data**: Incorporates country information for each IP address using the IPinfo API.
- **Error Handling**: Includes robust error handling for missing API keys and network issues.
- **User Interaction**: Prompts the user to decide whether to continue if the IPinfo API key is missing.

## Prerequisites

- **Python**: Version 3.6 or higher.
- **API Keys**:
  - **DNSTwister API Key**: Required for fetching DNS data.
  - **IPinfo Access Token**: Optional, required for geolocation data.

## Installation

1. **Clone or Download the Repository**

   ```bash
   git clone https://github.com/yourusername/dns-report-generator.git
   cd dns-report-generator
   ```

2. **Create a Virtual Environment (Recommended)**

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install Required Packages**

   ```bash
   pip install -r requirements.txt
   ```

   If you don't have a `requirements.txt`, create one with the following content:

   ```text
   requests
   ipinfo
   ```

## Configuration

### Setting Up Environment Variables

The script uses environment variables to access API keys for security reasons.

- **DNSTwister API Key**: Set the `DNS_TWISTER_API_KEY` environment variable.
- **IPinfo Access Token**: Set the `IP_INFO_API` environment variable (optional).

#### On Unix/Linux/macOS:

```bash
export DNS_TWISTER_API_KEY='your_dnstwister_api_key'
export IP_INFO_API='your_ipinfo_access_token'  # Optional
```

#### On Windows Command Prompt:

```cmd
set DNS_TWISTER_API_KEY=your_dnstwister_api_key
set IP_INFO_API=your_ipinfo_access_token  # Optional
```

#### On Windows PowerShell:

```powershell
$env:DNS_TWISTER_API_KEY='your_dnstwister_api_key'
$env:IP_INFO_API='your_ipinfo_access_token'  # Optional
```

## Usage

Run the script using the following command:

```bash
python dns_report_generator.py
```

### Script Flow

1. **API Key Verification**: The script checks for the `DNS_TWISTER_API_KEY`. If not found, it exits.
2. **Optional Geolocation**: If `IP_INFO_API` is missing, the script prompts:

   ```
   Access Token not found for Geo Location. Continue? (Y/N):
   ```

   - Enter `Y` to continue without geolocation data.
   - Enter `N` to exit the script.

3. **Data Retrieval**: Fetches DNS resolution data from DNSTwister.
4. **CSV Generation**: Creates a `DNSReport.csv` file in the `Results` directory.

## Output

- **Directory**: All results are saved in the `Results` directory.
- **CSV File**: The `DNSReport.csv` file contains:

  | Subscribed Domain | Domain           | IP            | MX Record Exists | Newly Monitored | Geo Location |
  |-------------------|------------------|---------------|------------------|-----------------|--------------|
  | example.com       | www.example.com  | 93.184.216.34 | True             | False           | United States|

- **Fields**:
  - **Subscribed Domain**: The domain you are monitoring.
  - **Domain**: The resolved domain.
  - **IP**: IP address of the resolved domain.
  - **MX Record Exists**: Indicates if an MX record exists (`True`/`False`).
  - **Newly Monitored**: Indicates if the domain is newly monitored (`True`/`False`).
  - **Geo Location**: Country associated with the IP address (if available).

## Error Handling

- **Missing API Keys**: The script will exit if the DNSTwister API key is missing. For the IPinfo token, it prompts the user to continue or exit.
- **Network Errors**: Handles exceptions during API calls and prints relevant error messages.
- **Geolocation Errors**: If geolocation data can't be fetched, the country is marked as `Unknown`.

## Dependencies

- **Python Standard Libraries**:
  - `os`: For environment variables and file path operations.
  - `csv`: For CSV file creation.
- **Third-Party Libraries**:
  - `requests`: For making HTTP requests to APIs.
  - `ipinfo`: For fetching geolocation data.

Install third-party libraries using:

```bash
pip install requests ipinfo
```

