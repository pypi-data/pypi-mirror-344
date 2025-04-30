

from .c_xml_display_elements import f_display_elements
from .c_xml_manager import main as xml_manager
from .c_xml_xslt_logic import f_test_logic
from .c_xml_structure import f_get_unique_column_names
from .c_single_test_csv import f_test_csv_columns
from .c_pipeline_xml_to_csv import f_xml_2_csv_namespace
import argparse
import sys

# Hardcoded version information
VERSION = "0.0.32"

# Hardcoded dependencies information
DEPENDENCIES = {
    "python": "^3.10",
    "lxml": "^5.3.0",
    "requests": "^2.32.3",
    "python-dateutil": "^2.9.0.post0",
    "pandas": "^2.2.3"}

# --xml is the name of the argument.  -> This argument is a flag (also known as a boolean option).
# action='store_true' means that if the argument --xml is provided in the command line, its value will be set to True.
# help='input name of the xmld' provides a description of the argument which is shown when the help message is displayed.
# Example usage: script.py --xml (Sets the xml argument to True).

def cli_main():
    parser = argparse.ArgumentParser(description='xml_discovery CLI Tool')
    parser.add_argument('--version', action='store_true', help='Show current version')
    parser.add_argument('--dependencies', action='store_true', help='Show project dependencies')
    parser.add_argument('--display', action='store_true', help='quick utility to shows child attributes of a choosen xml')
    parser.add_argument('--xmlmanager', action='store_true', help='manage known xml files locations and thier stylesheet document')
    parser.add_argument('--logic', action='store_true', help='test logic between xml and xslt document')
    parser.add_argument('--columnmatch', action='store_true', help='test column number match as input provided')
    parser.add_argument('--structure', action='store_true', help='gives you the unique column names used as per the choosen xslt document')
    parser.add_argument('-xml', type=str, help='Path to the XML file') 
    parser.add_argument('-xslt', type=str, help='Path to the XSLT file')
    parser.add_argument('-file', type=str, help='Path to the file with filename and file extention') 
    parser.add_argument('-colnum', type=str, help='input number of column to test against')
    parser.add_argument('-xmlconfig', type=str, help='input name of the xml config file name to be processed')

    # parser.add_argument('--yamldir', action='store_true', help='Show location of connection.yaml file')
    
    args = parser.parse_args()

    if args.version:
        print(f'xmlvault version: {VERSION}')
        sys.exit(0)

    if args.dependencies:
        print("Project Dependencies:")
        for dep, version in DEPENDENCIES.items():
            print(f"{dep}: {version}")


    if args.display:
        f_display_elements()

    if args.xmlmanager:
        xml_manager()

    if args.logic:
        if not args.xml or not args.xslt:
            print("Both --xml and --xslt arguments are required for --logic")
            sys.exit(1) 
        f_test_logic(args.xml, args.xslt) 
        sys.exit(0)

    if args.structure:
        if not args.xml or not args.xslt:
            print("Both --xml and --xslt arguments are required for --structure")
            sys.exit(1) 
        f_get_unique_column_names(args.xml, args.xslt) 
        sys.exit(0)

    if args.columnmatch:
        if not args.file or not args.colnum:
            print("Both --file and --colnum arguments are required for --columnmatch")
            sys.exit(1) 
        f_test_csv_columns(args.file, args.colnum) 
        sys.exit(0)

    if args.xmlconfig:
        f_xml_2_csv_namespace(args.xmlconfig)


    # If no argument is provided, you might want to show the help message 
    if not any(vars(args).values()): 
        parser.print_help()

if __name__ == '__main__':
    cli_main() 
