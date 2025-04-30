from .pipeline_xml_connect import f_pipe_load_xml
# import xml.etree.ElementTree as ET
import lxml.etree as ET
from datetime import datetime
import pandas as pd
import os
import io

# Retrieve and verify the environment variable 
v_file_out = os.getenv('file_out') 
v_file_in = os.getenv('file_in') 
v_xslt_path = os.getenv('xslt_path')
v_xpath = os.getenv('XML_CONFIG_NAME')
# v_xpath = 'cctvSnapshot_root'


# this is what ypu would pass onto AIRFLOW {XML_CONFIG_NAME}

def f_xml_2_csv_namespace():
    xml_tree, xml_xslt, xpath_string = f_pipe_load_xml(v_xpath)

    #  Construct XSLT full path with filename
    xslt_file_path = os.path.join(v_xslt_path, xml_xslt)

    if not os.path.exists(xslt_file_path):
        print(f"XSLT file not found: {xslt_file_path}")
        exit(1)

    # Parse the XML and XSLT files
    try:
        # xml_tree = ET.parse(xml_content)
        xslt_tree = ET.parse(xslt_file_path)
        print("XSLT file format is valid.")
    except ET.XMLSyntaxError as e:
        print(f"Error parsing XML/XSLT file: {e}")
        exit(1)

    # Apply the XSLT
    transform = ET.XSLT(xslt_tree)
    result_tree = transform(xml_tree)

    # Print the result for debugging purposes
    csv_output = str(result_tree)
    # print('\nResult tree  printed :', csv_output[:200], '\n')

    # Convert the transformed CSV output into a pandas DataFrame
    csv_data = io.StringIO(csv_output)
    df = pd.read_csv(csv_data, delimiter='~')
    # df = pd.read_csv(csv_data)


    _save_xml_df(v_xpath,df)


def _save_xml_df(v_xpath, df):

    # Get the current date and time 
    timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S-%f')
    
    # Construct the output filename
    csv_filename = f"{v_xpath}_{timestamp}.csv"
   
    # Construct the full file path 
    full_path = os.path.join(v_file_out, csv_filename)

    # Save the DataFrame to the specified location 
    df.to_csv(full_path, index=False, sep='~')
    # df.to_csv(full_path, index=False)
    
    print(f"Output saved to {full_path}")

def f_xml_2_csv_simple():
    xml_tree, xml_xslt, xpath_string = f_pipe_load_xml(v_xpath)
    xpath2 = f"//{xpath_string}"

    df = pd.read_xml(xml_tree, xpath=xpath2)

    # Add the new columns to the DataFrame as the first two columns 
    # df.insert(0, 'table_ID', v_xpath) 
    # df.insert(1, 'parent_ID', xml_xslt)

    # if print required on screen 
    print("\n f_xml_2_csv: your selected xml dataframe is below : ")
    print(df.head(3))

    # below funtion locally called will name the csv file and along with time stamp save it in v_file_out location
    _save_xml_df(xpath_string,df)

if __name__ == "__main__":
    f_xml_2_csv_namespace()
    # f_xml_2_csv_simple()


