from lxml import etree

def f_get_xpath_and_namespace(xslt_path):
    # Parse the XSLT document
    xslt_doc = etree.parse(xslt_path)
    xslt_root = xslt_doc.getroot()

    # Extract namespaces
    namespaces = {k: v for k, v in xslt_root.nsmap.items() if k}
    # Extract the first XPath expression (you can adjust this to handle multiple)
    xpath_expr = xslt_root.xpath('//xsl:for-each/@select', namespaces={'xsl': 'http://www.w3.org/1999/XSL/Transform'})[0]

    return xpath_expr, namespaces

def f_get_unique_column_names(xml_path, xslt_path):
    # Extract XPath and namespace from XSLT
    xpath, namespaces = f_get_xpath_and_namespace(xslt_path)

    # Parse the XML file
    tree = etree.parse(xml_path)
    root = tree.getroot()

    # Find all elements matching the XPath
    elements = root.xpath(xpath, namespaces=namespaces)

    # Extract column names
    column_names = set()
    for elem in elements:
        for child in elem:
            column_names.add(etree.QName(child).localname)

    print(column_names)
    #  if function is required to return value uncheck below
    # return column_names


if __name__ == "__main__":
    f_get_unique_column_names('D:\\MYGIT\\files\\in\\cctvStatus.xml', 'D:\\MYGIT\\files\\xslt\\cctvStatus_root_v3.xslt')
    # print("Unique column names:", unique_column_names)
