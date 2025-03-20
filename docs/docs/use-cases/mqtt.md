---
title: "Mosquitto MQTT"
---

## Overview
This guide explains how to set up the Mosquitto MQTT broker inside a Docker container on a B&R X20 Edge device. Optionally, we include MQTTX Web for testing MQTT messages through a web interface.

:::info

Before proceeding, ensure you have the following installed on your system, these come preinstalled on the X20 Edge:

- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)

:::

## Docker Compose Configuration
Create a `docker-compose.yml` file with the following content:

```yaml
services:
  mosquitto:
    image: eclipse-mosquitto:latest
    container_name: mosquitto
    restart: unless-stopped
    ports:
      - "1883:1883"  # Standard MQTT
      - "9001:9001"  # WebSockets
    volumes:
      - ./mosquitto.conf:/mosquitto/config/mosquitto.conf

  mqttx: # MQTTX Web UI (Optional)
    image: emqx/mqttx-web:latest
    container_name: mqttx
    restart: unless-stopped
    ports:
      - "8083:80"
```

### **Mosquitto Configuration**
Create a `mosquitto.conf` file in the same directory:

```ini
listener 1883 0.0.0.0
allow_anonymous true

listener 9001 0.0.0.0
protocol websockets
allow_anonymous true
```

This configuration allows anonymous connections and enables both standard MQTT and WebSockets.

:::warning

## **Security Considerations**
For production use, authentication should be enabled by setting up a password file and configuring `mosquitto.conf` accordingly. More details can be found in the [Mosquitto authentication documentation](https://mosquitto.org/documentation/authentication-methods/).

:::

## **Starting Mosquitto**
Run the following command to start the containers:

```sh
docker-compose up -d
```

## **Testing the MQTT Broker**
To test the broker, you can use MQTTX Web, which is available in a browser at `http://<X20-Edge-IP>:8083`. You can also use any other MQTT client.


## **Stopping the Containers**
To stop and remove the containers, use:

```sh
docker-compose down
```

This will also remove MQTTX if it was included.

