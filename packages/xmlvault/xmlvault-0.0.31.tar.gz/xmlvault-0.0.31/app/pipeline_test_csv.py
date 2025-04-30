import os
import re
import csv
import sys

# Retrieve and verify the environment variable 
v_file_out = os.getenv('file_out') 
# v_file_in = os.getenv('file_in') 
# v_xslt_path = os.getenv('xslt_path')
v_xpath = os.getenv('XML_CONFIG_NAME')
# conn_home = os.getenv('conn_home') 
# v_db_connection = os.getenv('DB_CONFIG_NAME')
# v_batch_id = os.getenv('LAST_BATCH_ID', 'LOCAL_RUN')
v_expected_column = os.getenv('column_number')


def test_csv_columns():
    # Pattern to match the filename (XML_NAME followed by date and time)
    pattern = re.compile(rf'{v_xpath}_\d{{4}}-\d{{2}}-\d{{2}}_\d{{2}}-\d{{2}}-\d{{2}}-\d{{6}}')
    print(pattern)

    # List all files in the directory
    files = os.listdir(v_file_out)

    # Find the file that matches the pattern
    matching_files = [f for f in files if pattern.match(f)]

    # Assuming you want the latest file if there are multiple matches
    if matching_files:
        matching_files.sort()  # Sort to get the latest file by name
        selected_file = matching_files[-1]
        print(f"Selected file: {selected_file}")

        # Check the number of columns in the selected file
        with open(os.path.join(v_file_out, selected_file), 'r') as csvfile:
            reader = csv.reader(csvfile, delimiter='~')  # Specify the pipe delimiter
            for row in reader:
                if len(row) == v_expected_column:
                    print(f"File {selected_file} matches the expected number of columns: {v_expected_column}")
                else:
                    print(f"File {selected_file} does not match the expected number of columns: {v_expected_column}")
                    sys.exit(1) # signifies error ~ exit(0) is pass
                # break  # Check only the first row for column count
    else:
        print(f"No matching files found for {v_xpath}.")

if __name__ == '__main__':
    test_csv_columns()
