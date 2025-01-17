import json
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

with open('ips.json', 'r') as file:
    ips = [json.loads(line) for line in file]

def make_request(host):
    if not host.startswith(('http://', 'https://')):
        host = 'http://' + host
    
    url = host + '/api/user/login'
    
    data = {
        "username": "admin",
        "password": "123456"
    }
    
    try:
        response = requests.post(url, json=data, verify=False, timeout=5)
        return url, response.status_code, response.text
    except requests.exceptions.RequestException as e:
        return url, "Error", str(e)

with ThreadPoolExecutor(max_workers=10) as executor:
    futures = {executor.submit(make_request, ip['host']): ip['host'] for ip in ips}
    
    with open('result.txt', 'w') as result_file:
        for future in as_completed(futures):
            host = futures[future]
            try:
                url, status, response = future.result()
                output = f"URL: {url}\nResponse: {status} {response}\n\n"
                print(output)
                result_file.write(output)
            except Exception as e:
                error_output = f"URL: {host}\nError: {e}\n\n"
                print(error_output)
                result_file.write(error_output)