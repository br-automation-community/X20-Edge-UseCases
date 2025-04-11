# 🔗 OPC UA to SQL data logger with python

[**This**](https://github.com/br-automation-com/X20-Edge-UseCases/tree/main/Python/OPCUA2SQL) script connects to an OPC UA server, reads variable values, and logs them into a MySQL database. The variable names and types are read from a `varlist.txt` file.

## Prerequisites

- Python 3.x
- `opcua` library
- `mysql-connector-python` library
- MySQL server

## Installation

1. Install the required Python libraries:
    ```sh
    pip install opcua mysql-connector-python
    ```

2. Ensure you have a MySQL server running and accessible.

## Configuration

1. **OPC UA Server URL**: Update the `OPC_UA_SERVER` variable with the URL of your OPC UA server.
    ```python
    OPC_UA_SERVER = "opc.tcp://192.168.30.108:4840"
    ```

2. **Variable Namespace**: Update the `VAR_NAMESPACE` variable with the namespace of your OPC UA server.
    ```python
    VAR_NAMESPACE = "urn:B&R/pv/"
    ```

3. **Polling Interval**: Set the polling interval in seconds.
    ```python
    POLLING_INTERVAL = 60
    ```

4. **MySQL Database Connection**: Update the MySQL connection details.
    ```python
    db_connection = mysql.connector.connect(
        host="192.168.1.1",
        user="root",
        password="bur",
        database="data"
    )
    ```

## Variable list

Create a `varlist.txt` file in the same directory as the script. This file should contain the variable names and their types, separated by a semicolon (`;`). Lines starting with `#` are treated as comments.

Example:
```
# VariableName;Type
Temperature;FLOAT
Pressure;FLOAT
```

## Script Workflow

1. **Read Variable Names and Types**: The script reads variable names and types from `varlist.txt`.
2. **Connect to OPC UA Server**: The script connects to the OPC UA server using the provided URL.
3. **List Namespaces**: The script lists all namespaces available on the OPC UA server.
4. **Get Namespace Index**: The script retrieves the namespace index for the specified namespace.
5. **Create Node IDs and Nodes**: The script creates node IDs and nodes for each variable.
6. **Connect to MySQL Database**: The script connects to the MySQL database.
7. **Check and Create Columns**: The script checks if columns exist in the database table and creates them if they don't.
8. **Read and Log Values**: The script reads the values of the nodes cyclically and logs them into the MySQL database.
9. **Error Handling**: The script handles any errors that occur during the process.
10. **Disconnect**: The script disconnects from the OPC UA server and MySQL database when finished.

## Error Handling

The script includes basic error handling to catch and print exceptions that occur during the connection, reading, and logging processes.
