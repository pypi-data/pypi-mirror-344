import yaml
import os

# Retrieve and verify the environment variable 
conn_home = os.getenv('conn_home') 
print(f"conn_home: {conn_home}") 

# Define the path for the connections file 
connections_file = os.path.join(conn_home, 'xml_config.yaml') 


# Function to load the connections from the file
def load_connections():
    if os.path.exists(connections_file):
        with open(connections_file, 'r') as file:
            return yaml.safe_load(file) or {}
    return {}

# Function to save the connections to the file
def save_connections(connections):
    with open(connections_file, 'w') as file:
        yaml.safe_dump(connections, file)

# Function to add or update a connection
def add_or_update_connection(name, xml_url, xml_xslt, xml_xpath):
    connections = load_connections()
    # connections[name] = xml_url, xml_xslt
    connections[name] = [xml_url, xml_xslt, xml_xpath]  # Ensure it's stored as a list

    save_connections(connections)

# Function to delete a connection
def delete_connection(name):
    connections = load_connections()
    if name in connections:
        del connections[name]
        save_connections(connections)

# Function to display connections and return the mapping of numbers to connection names
def display_connections():
    connections = load_connections()
    if not connections:
        print("No connections available.")
        return []
    connection_list = list(connections.items())
    for i, (name, details) in enumerate(connection_list, 1):
        print(f'{i}: {name} - {details}')
    return connection_list

def main():
    while True:
        print("\nOptions: [0] Add New XML config [1] Update XML Config [2] Delete XML Config [3] Display XML Config [4] Exit")
        choice = input("Enter your choice: ")

        if choice == '0':

            name = input("Enter new xml config name: ")
            xml_url = input("Enter xml url or dir path (Win OS use back slash): ")
            xml_xslt = input("Enter xslt document name (with file ext / no path location required) (leave blank if not required):  ")
            xml_xpath = input("Enter xpath string (dont add '//'prefix)(leave blank if not required): ")
            add_or_update_connection(name, xml_url, xml_xslt, xml_xpath)
            print(f'Connection {name} added.')

        elif choice == '1':
            print("Select connection to update:")
            connection_list = display_connections()
            selection = int(input("Enter the connection number: "))
            if 1 <= selection <= len(connection_list):
                name = connection_list[selection - 1][0]
                xml_url = input("Enter new xml url or dir path (Win OS use back slash) (leave blank to keep current): ") or connection_list[selection - 1][1][0]
                xml_xslt = input("Enter new xslt document name (with file ext / no path location required) (leave blank to keep current): ") or connection_list[selection - 1][1][1]
                xml_xpath = input("Enter new xpath string (dont add '//'prefix) (leave blank to keep current): ") or connection_list[selection - 1][1][2]
                add_or_update_connection(name, xml_url, xml_xslt, xml_xpath)
                print(f'Connection {name} updated.')
            else:
                print("Invalid selection.")

        elif choice == '2':
            print("Select connection to delete:")
            connection_list = display_connections()
            selection = int(input("Enter the connection number: "))
            if 1 <= selection <= len(connection_list):
                name = connection_list[selection - 1][0]
                delete_connection(name)
                print(f'Connection {name} deleted.')
            else:
                print("Invalid selection.")

        elif choice == '3':
            print("Current connections:")
            display_connections()

        elif choice == '4':
            break

        else:
            print("Invalid choice. Please try again.")

if __name__ == '__main__':
    main()
