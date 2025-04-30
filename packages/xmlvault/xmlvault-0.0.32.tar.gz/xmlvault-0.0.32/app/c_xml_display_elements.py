import xml.etree.ElementTree as ET
from .xml_connect import f_load_xml

# xml_display_elements.py --> xml_connect.py


def f_display_elements():
    xml_data1 = f_load_xml()

    root = ET.fromstring(xml_data1)
    # Recursively display elements and their attributes
    
    elem_count = 1
    for elem in root.iter():
        # print(f"Element {elem_count}: {elem.tag}, Attributes: {elem.attrib}")
        elem_count += 1

    print("f_display_elements: Number of rows in the selected xml are: ", elem_count)
    # limit = input("f_display_elements: enter number of records to show: ")
    # limit = 1

    def display_parents(elem, level=0):
        if list(elem):  # Check if the element has children
            indent = '  ' * level
            print(f"{indent}Parent Element: {elem.tag}, Attributes: {elem.attrib}")
            for child in elem:
                display_parents(child, level + 1)


    # y=1
    # for x in root.iter():
    #     display_parents(root)
    #     # print(f"f_display_elements: Element: {x.tag}, Attributes: {x.attrib}")
    #     if y == int(limit):
    #         break
    #     y+=1
    
    display_parents(root)
    return xml_data1

if __name__ == "__main__":
    f_display_elements()
###########################################################################



# def f_display_elements():
#     xml_data1 = f_load_xml()

#     root = ET.fromstring(xml_data1)
#     # Recursively display elements and their attributes
    
#     elem_count = 1
#     for elem in root.iter():
#         # print(f"Element {elem_count}: {elem.tag}, Attributes: {elem.attrib}")
#         elem_count += 1

#     print("f_display_elements: Number of rows in the selected xml are: ", elem_count)
#     limit = input("f_display_elements: enter number of records to show: ")
  
#     y=1
#     for x in root.iter():
#         print(f"f_display_elements: Element: {x.tag}, Attributes: {x.attrib}")
#         if y == int(limit):
#             break
#         y+=1
#     return xml_data1

# if __name__ == "__main__":
#     f_display_elements()
