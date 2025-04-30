import requests
import xml.etree.ElementTree as ET

def f_load_xml():
    # Ask the user for their choice
    choice = int(input('f_load_xml: Choose 1 for URL or 2 for local dir path: '))

    if choice == 1:
        # Ask the user for the XML URL
        xml_url = input("f_load_xml: Enter the XML URL -  ex: https://www.w3schools.com/xml/simple.xml : ")
        response = requests.get(xml_url)
        xml_data = response.content
        return xml_data
        # xml_url_f(xml_url)
    elif choice == 2:
        # Ask the user for the local directory path
        xml_path = input("f_load_xml: Enter the local XML file path - ex: /home/admin/files/book.xml: ")
        with open(xml_path, 'r') as file:
            xml_data = file.read()
            return xml_data
        # xml_local_f(xml_path)
    else:
        print("f_load_xml: Invalid choice. Please choose 1 or 2.")

if __name__ == "__main__":
    f_load_xml()
