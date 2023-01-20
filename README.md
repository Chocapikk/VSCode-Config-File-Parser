# vscode.py

This script is used to parse vscode configuration files from websites, it will extract information such as host, port, username, and password. This information can be used to compromise the machine.

## Usage

To use this script, you will need to provide an input file containing a list of URLs to parse, and an output file to save the parsed information.

```bash
python vscode.py input_file.txt output_file.txt [-f file_format]
```

### Optional arguments

```bash
-f, --file_format : Output file format (combolist or csv) (default: combolist)
```

### Example

```bash
python vscode.py urls.txt parsed_data.txt -f csv
```
## Vulnerability

This script takes advantage of a critical vulnerability (http://www.securityspace.com/smysecure/catid.html?id=1.3.6.1.4.1.25623.1.0.108346) that allows attackers to access sensitive information from vscode configuration files. It is important to note that this information can be used to compromise the machine.

## Disclaimer

This script is for educational and research purposes only. The author is not responsible for any misuse or damage caused by this script.
