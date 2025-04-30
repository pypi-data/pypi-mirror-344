import os
import lxml.etree as ET
import pandas as pd
import io

# # File paths for XML and XSLT
# xml_file_path = r'D:\MYGIT\files\in\dms_data.xml'
# xslt_file_path = r'D:\MYGIT\files\xslt_dms_v3.xslt'
# xml_file_path = 'https://nec-por.ne-compass.com/NEC.XmlDataPortal/api/c2c?networks=NewHampshire&dataTypes=dmsData'
# xslt_file_path = 'D:\\MYGIT\\files\\xslt\\dms_root_v3.xslt'
# local_dms_equiloc_v3     local_dms_root_v3    local_dms_equiploc_n_id_v3


from lxml import etree

def f_test_logic(xml_file_path, xslt_file_path):

    # Check if both XML and XSLT files exist
    if not os.path.exists(xml_file_path):
        print(f"XML file not found: {xml_file_path}")
        exit(1)
    if not os.path.exists(xslt_file_path):
        print(f"XSLT file not found: {xslt_file_path}")
        exit(1)

    print(" \nBoth XML and XSLT files exist.")

    # Parse the XML and XSLT files
    try:
        xml_tree = ET.parse(xml_file_path)
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
    print('\n Result tree  printed :', csv_output[:1000], '\n')

if __name__ == "__main__":
    # f_test_logic(xml_file_path, xslt_file_path)
    f_test_logic('https://nec-por.ne-compass.com/NEC.XmlDataPortal/api/c2c?networks=NewHampshire&dataTypes=dmsData', 'D:\\MYGIT\\files\\xslt\\dms_root_v3.xslt')
