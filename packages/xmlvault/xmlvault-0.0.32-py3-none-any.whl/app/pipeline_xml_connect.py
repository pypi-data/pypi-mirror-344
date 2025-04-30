import os
import requests
import yaml
import lxml.etree as ET
import io
import glob

#externally call this function like below
# xml_data, xml_xslt, xpath_string = f_pipe_load_xml(config_name)


def _wildcard_xml(xml_url: str):     # this function _wildcard was introduced to distinguish between file name with wildcrd or absolute file name in xml_config
    # Check if xml_url contains a wildcard
    if '*' in xml_url:
        # Use glob to find matching files
        matching_files = glob.glob(xml_url)
        
        # If no matching files found, print error and exit
        if not matching_files:
            print(f"No matching files found for pattern: {xml_url}")
            exit(1)
        
        # Sort matching files by modification time to get the oldest file
        matching_files.sort(key=os.path.getmtime)
        selected_file = matching_files[0]
        print(f"Selected file: {selected_file}")
    else:
        selected_file = xml_url

    # Check if the selected file exists
    if not os.path.exists(selected_file):
        print(f"XML file not found: {selected_file}")
        exit(1)
    else:
        xml_tree = ET.parse(selected_file)
        # Process the XML tree as needed
        # Example:
        print(f"Successfully parsed: {selected_file}")
        print(xml_tree)
        # return xml_tree
    return xml_tree
    
        



def f_pipe_load_xml(config_name: str) -> tuple:
    # Get the directory path from the environment variable
    conn_home = os.getenv('conn_home')
    
    # Construct the full path to the YAML file
    config_file = os.path.join(conn_home, 'xml_config.yaml')
    
    # Load the YAML file
    with open(config_file, 'r') as file:
        config = yaml.safe_load(file)
    
    # Get the configuration details for the specified config_name
    if config_name in config:
        xml_url = config[config_name][0]
        xml_xslt = config[config_name][1]
        xpath_string = config[config_name][2]
    else:
        print(f"Configuration '{config_name}' not found.")
        return None, None, None
    
    # Read XML data from the URL or local file
    if xml_url.startswith('http://') or xml_url.startswith('https://'):
        # Remote URL
        try:
            # response = requests.get(xml_url)
            response = requests.get(xml_url)
            # response = requests.get(xml_url, verify='D:\\MYGIT\\.conns\\ForcepointCloudCA.crt')  # for windows
            response.raise_for_status()  # Check for HTTP errors
            xml_content = response.content
            xml_tree = ET.fromstring(xml_content)
        except requests.exceptions.RequestException as e:
            print(f"Error fetching XML from URL: {e}")
            exit(1)
        
    else:
        xml_tree =_wildcard_xml(xml_url)  # we used to do this like {xml_tree = ET.parse(xml_url) }  but then this function _wildcard was introduced to distinguish between file name with wildcrd or absolute file name in xml_config

        # # check if xml file and on the path exist
        # if not os.path.exists(xml_url):
        #     print(f"XML file not found: {xml_url}")
        #     exit(1)
        # else:
        #     # xml_tree = ET.parse(xml_url) 
        #     xml_tree =_wildcard_xml(xml_url)  # we used to do this like {xml_tree = ET.parse(xml_url) }  but then this function _wildcard was introduced to distinguish between file name with wildcrd or absolute file name in xml_config
 
    
    return xml_tree, xml_xslt, xpath_string




if __name__ == "__main__":
    # Example usage
    config_name = 'm5_J1Crash_root_v4'
    xml_tree, xml_xslt, xpath_string = f_pipe_load_xml(config_name)

    if xml_tree:
        print(f"XML Data: {xml_tree[:100]}...")  # Print the first 100 characters of the XML data
        print(f"Parent Node: {xml_xslt}")
        print(f"XPath String: {xpath_string}")



