
[![Upload Python Package](https://github.com/ankit48365/xmlvault/actions/workflows/python-publish.yml/badge.svg)](https://github.com/ankit48365/xmlvault/actions/workflows/python-publish.yml)
![Latest Release](https://img.shields.io/badge/release-v0.0.33-blue)

# xmlvault

```python
    pip install xmlvault
    xmlvault --help

```    

## Purpose

This python package is usefull, if XML data is required to be ingested or consumed as a data source, it creates a central xml_config.yaml file (as YAML) on a user's machine. this yaml will store xml path/url, xslt, xpath query etc. explore more utilites with {xmlvault --help}

## Running the Project

To run this project, you need to define and save a path with the name `conn_home`. This is where you’ll save the `xml_config.yaml` file, which stores your source xml files.

## For Windows (CMD):

```
# Define and save the path
setx conn_home "C:\path\outside\your\project\preferably"

# Check the path
echo %conn_home%

# Define and save the path
setx conn_home "C:\path\outside\your\project\preferably"

# Check the path
echo %conn_home%
```
## For Windows Powershell:

```
# Define and save the path
[System.Environment]::SetEnvironmentVariable('conn_home', 'C:\path\outside\your\project\preferably', 'User')

# Check the path
$env:conn_home
```

### For Linux:

```bash
# Define and save the path in your .bashrc
echo 'export conn_home="path/outside/your/project/preferably"' >> ~/.bashrc

# Source the .bashrc to apply changes
source ~/.bashrc
```
