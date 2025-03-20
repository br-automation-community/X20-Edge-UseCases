import time
from opcua import Client
import os
import mysql.connector

# SQL Server URL
SQL_SERVER = "192.168.30.128"
# OPC UA Server URL
OPC_UA_SERVER = "opc.tcp://192.168.30.108:4840"
# B&R Variable name space, use 'urn:B&R/pv/' for information model 1 and 'http://br-automation.com/OpcUa/PLC/PV/' for information model 2
VAR_NAMESPACE = "urn:B&R/pv/"
# Polling interval in seconds
POLLING_INTERVAL = 5

# Database credentials
DB_USER = "admin"
DB_PASSWORD = "bur4711"
DB_DATABASE = "data"

# Absolute path to varlist.txt
varlist_path = os.path.join(os.path.dirname(__file__), "varlist.txt")

# Read variable names and types from varlist.txt
variable_names = []
variable_types = []
with open(varlist_path, "r") as file:
    for line in file.readlines():
        if line.startswith("#"):
            continue
        name, var_type = line.strip().split(";")
        variable_names.append(name)
        variable_types.append(var_type)

# Create a client and connect to the server
client = Client(OPC_UA_SERVER)
try:
    client.connect()
    print("Connected to the OPC UA Server")

    # List all namespaces
    namespaces = client.get_namespace_array()
    print("Namespaces:")
    for i, namespace in enumerate(namespaces):
        print(f"{i}: {namespace}")

    # Get the namespace index for VAR_NAMESPACE
    namespace_index = client.get_namespace_index(VAR_NAMESPACE)
    print(f"Namespace index for {VAR_NAMESPACE}: {namespace_index}")

    # Create arrays for node IDs and nodes
    node_ids = [f"ns={namespace_index};s=::{var_name}" for var_name in variable_names]
    nodes = [client.get_node(node_id) for node_id in node_ids]

    # Connect to MySQL database
    db_connection = mysql.connector.connect(
        host=SQL_SERVER,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_DATABASE
    )
    cursor = db_connection.cursor()

    # Create the table PLC1 if it does not exist
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS PLC1 (
            id INT AUTO_INCREMENT PRIMARY KEY
        )
    """)
    db_connection.commit()

    # Check if columns exist and create them if they don't
    for var_name, var_type in zip(variable_names, variable_types):
        var_name = var_name.replace(":", "_")
        cursor.execute(f"SHOW COLUMNS FROM PLC1 LIKE '{var_name}'")
        result = cursor.fetchone()
        if not result:
            cursor.execute(f"ALTER TABLE PLC1 ADD COLUMN {var_name} {var_type}")
            db_connection.commit()
            print(f"Column '{var_name}' with type '{var_type}' added to the table 'PLC1'")

    # Read the value of the nodes cyclically
    while True:
        try:
            values = {}
            for node_id, node, var_name, var_type in zip(node_ids, nodes, variable_names, variable_types):
                value = node.get_value()
                values[var_name.replace(":", "_")] = value
                print(f"Value of the node {node_id}: {value}")

            # Construct the INSERT statement dynamically
            columns = ", ".join(values.keys())
            placeholders = ", ".join(["%s"] * len(values))
            sql = f"INSERT INTO PLC1 ({columns}) VALUES ({placeholders})"
            cursor.execute(sql, list(values.values()))
            db_connection.commit()
        except Exception as e:
            print(f"Error reading value: {e}")
        
        # Wait for the specified polling interval
        time.sleep(POLLING_INTERVAL)

except Exception as e:
    print(e)

finally:
    # Disconnect from the server
    client.disconnect()
    print("Disconnected from the OPC UA Server")

    # Close the database connection
    if db_connection.is_connected():
        cursor.close()
        db_connection.close()
        print("Disconnected from the MySQL database")