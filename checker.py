import sys
import csv
import socket
import paramiko
import concurrent.futures
from tqdm import tqdm
from ftplib import FTP

paramiko.util.log_to_file('/dev/null')

def check_ftp_connection(url, host, port, username, password):
    global output_file
    ftp = FTP(timeout=10)
    try:
        ftp.connect(host, int(port))
        ftp.login(user=username, passwd=password)
        output_file.write(f"{url} : lftp -u {username},{password} -e 'echo Connection Successful; quit' {host}\n")
    except:
        pass
        try:
            host = socket.gethostbyname(url)
            ftp.connect(host, port)
            ftp.login(user=username, passwd=password)
            output_file.write(f"{url} : lftp -u {username},{password} -e \"echo Connection Successful; quit\" {host}\n")
        except:
            pass
    ftp.close()

def check_sftp_connection(url, host, port, username, password, remote_path):
    global output_file
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        ssh.connect(host, port=port, username=username, password=password, timeout=1)
        output_file.write(f"{url} : [{password}] ssh {username}@{host} -P {port}\n")
    except:
        try:
            host = socket.gethostbyname(url)
            ssh.connect(host, port=port, username=username, password=password)
            output_file.write(f"{url} : [{password}] ssh {username}@{host} -P {port}\n")
        except:
            pass
    ssh.close()

def connect(url, name, host, port, protocol, username, password, remote_path=None, upload_on_save=None):
    if protocol == "ftp":
        check_ftp_connection(url, host, port, username, password)
    elif protocol == "sftp":
        check_sftp_connection(url, host, port, username, password, remote_path)
    else:
        pass

def main(csv_file, output_file):
    try:
        urls = []
        with open(csv_file, newline='') as f:
            reader = csv.reader(f)
            next(reader)
            for row in reader:
                urls.append(row)
        progress_bar = tqdm(total=len(urls), unit=' URL', bar_format='\033[32m{l_bar}{bar}| {n_fmt}/{total_fmt} [Elapsed: {elapsed}, Remaining: {remaining} {rate_fmt}]\033')
        with concurrent.futures.ThreadPoolExecutor(100) as executor:
            future_to_row = {executor.submit(connect, *(col.strip() for col in row)): row for row in urls}
            for future in concurrent.futures.as_completed(future_to_row):
                row = future_to_row[future]
                try:
                    future.result()
                except Exception as e:
                    pass
                progress_bar.update()
    except FileNotFoundError:
        print("File not found")

if __name__ == "__main__":
    banner = '''\u001b[35m
    ╦  ╦╔═╗╔═╗╔═╗╔╦╗╔═╗  ╔═╗╦ ╦╔═╗╔═╗╦╔═╔═╗╦═╗
    ╚╗╔╝╚═╗║  ║ ║ ║║║╣   ║  ╠═╣║╣ ║  ╠╩╗║╣ ╠╦╝
     ╚╝ ╚═╝╚═╝╚═╝═╩╝╚═╝  ╚═╝╩ ╩╚═╝╚═╝╩ ╩╚═╝╩╚═

                    Chocapikk
              (github.com/Chocapikk)
               Stay safe,stay legal
\033
'''
    print(banner)
    if len(sys.argv) < 3:
        print(f"\nUsage: python {sys.argv[0]} input_file output_file\n")
        exit(1)
    elif len(sys.argv) < 2:
        print("No CSV file provided as a parameter")
        exit(1)

    csv_file = sys.argv[1]
    output_file = open(sys.argv[2], "w")

    main(csv_file, output_file)
