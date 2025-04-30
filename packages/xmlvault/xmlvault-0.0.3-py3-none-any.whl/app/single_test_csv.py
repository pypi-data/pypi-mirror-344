import os
import csv
import sys

# Retrieve and verify the environment variable 
v_file_out = os.getenv('file_out') 


def f_test_csv_columns(v_selected_file, v_expected_column):
    with open(os.path.join(v_file_out, v_selected_file), 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter='~')  # Specify the pipe delimiter
        for row in reader:
            if len(row) == v_expected_column:
                print(f"File {v_selected_file} matches the expected number of columns: {v_expected_column}")
            else:
                print(f"File {v_selected_file} does not match the expected number of columns: {v_expected_column}")
                sys.exit(1) # signifies error ~ exit(0) is pass
            # break  # Check only the first row for column count

if __name__ == '__main__':
    f_test_csv_columns('cctvSnapshot_local_root_2025-01-07_20-20-24-778414.csv',6)
