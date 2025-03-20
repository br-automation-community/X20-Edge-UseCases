---
sidebar_position: 2
---

# Docker Compose

Docker Compose is a tool for defining and running multi-container Docker applications. With Compose, you use a YAML file to configure your application's services. Then, with a single command, you create and start all the services from your configuration.

:::info

Before proceeding, ensure you have the following installed on your system, these come preinstalled on the X20 Edge:

- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)

Also make sure that your device has internet connectivity to access Docker Hub or a custom registry.

:::

## Step-by-Step Tutorial

### Step 1: Set Up Project Directory

Create a new directory for your project and navigate into it via your terminal.

```
mkdir docker-flask-postgres
cd docker-flask-postgres
```

### Step 2: Create Python Flask Application

Create a directory named ```app``` and create a file named ```app.py``` inside it.

```
mkdir app
touch app/app.py
```

Edit ```app/app.py``` to include a simple Flask app:

```python
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{os.getenv("POSTGRES_USER")}:{os.getenv("POSTGRES_PASSWORD")}@db:5432/{os.getenv("POSTGRES_DB")}'
db = SQLAlchemy(app)

@app.route('/')
def hello():
    return "Hello, World!"

if __name__ == "__main__":
    app.run(host='0.0.0.0')
```

### Step 3: Create Dockerfile for Flask Application

Create a ```Dockerfile``` in the ```app``` directory to build the Docker image for the Flask app.

```
touch app/Dockerfile
```

Edit ```app/Dockerfile``` with the following content:

```Dockerfile
# Use the official Python image as a base image from Docker Hub.
FROM python:3.9-slim

# Set the working directory in the container to '/app'.
# This means all subsequent instructions will be run in this directory.
WORKDIR /app

# Copy the 'requirements.txt' file from the local machine to the container's working directory.
COPY requirements.txt requirements.txt

# Install the Python dependencies specified in 'requirements.txt' using pip.
RUN pip install -r requirements.txt

# Copy all the files from the current directory on the local machine to the container's working directory.
# This includes the Flask app code and any other necessary files.
COPY . .

# Define the command to start the Flask application.
CMD ["python", "app.py"]
```

### Step 4: Create requirements.txt for Flask Dependencies

Create a ```requirements.txt``` file in the ```app``` directory.

```
touch app/requirements.txt
```

Add the following dependencies to ```app/requirements.txt```:

```
flask
flask_sqlalchemy
psycopg2-binary
```

### Step 5: Define Services in Docker Compose File

Create a ```docker-compose.yml``` file in the project directory.

```
touch docker-compose.yml
```

Edit ```docker-compose.yml``` with the following content:

```yaml
services:
  web:
    build: ./app
    ports:
      - "5000:5000"
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
      POSTGRES_DB: mydatabase
    depends_on:
      - db
  db:
    image: postgres:13
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
      POSTGRES_DB: mydatabase
```

### Step 6: Build and Run Your Application

In your terminal, navigate to your project directory and run the following command:

```
docker-compose up
```

This command will build the Docker image for the Flask app, start the ```web``` and ```db``` services as defined in your ```docker-compose.yml``` file. 

### Step 7: Interact with Your Application

You can verify that your services are running by visiting ```http://<X20-Edge-IP>:5000``` in your web browser. You should see "Hello, World!" displayed.

### Step 8: Managing Your Containers

To stop your services, you can press ```Ctrl+C``` in the terminal where you ran ```docker-compose up```.

To stop and remove all containers defined in the ```docker-compose.yml``` file, run:

```
docker-compose down
```

### Best Practices

Here are some best practices for using Docker Compose:

- **Use environment variables:** Define environment variables in a ```.env``` file and reference them in your ```docker-compose.yml``` to keep sensitive data like passwords out of your configuration file.
  
- **Leverage Docker networks:** Use Docker networks to allow your services to communicate with each other securely.

- **Volume Mounting:** Use volumes to persist your data by defining them in your ```docker-compose.yml```.

- **Keep it simple:** Start small and scale your Compose file slowly. Begin with a few containers and build on that.

- **Optimize for rebuilds:** Take advantage of Docker's layered architecture to minimize rebuild times by ordering your Dockerfile's ```COPY``` and ```RUN``` instructions from least to most frequently changing.

### Example with Environment Variables

Create a ```.env``` file in your project directory:

```
POSTGRES_PASSWORD=mysecretpassword
POSTGRES_USER=myuser
POSTGRES_DB=mydatabase
```

Update your ```docker-compose.yml``` to use these variables:

```yaml
services:
  web:
    build: ./app
    ports:
      - "5000:5000"
    environment:
      POSTGRES_USER: ${POSTGRES_USER}
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
      POSTGRES_DB: ${POSTGRES_DB}
    depends_on:
      - db
  db:
    image: postgres:13
    environment:
      POSTGRES_USER: ${POSTGRES_USER}
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
      POSTGRES_DB: ${POSTGRES_DB}
```

Run ```docker-compose up``` again and Docker Compose will use the values from your ```.env``` file.

## Conclusion

Docker Compose simplifies the process of managing multi-container applications. By following this step-by-step tutorial and applying best practices, you can efficiently run and manage your Docker applications. For more in-depth information, refer to the [Docker Compose documentation](https://docs.docker.com/compose/).