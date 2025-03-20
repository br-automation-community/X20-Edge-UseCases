---
sidebar_position: 1
---

# Getting started

Welcome to the Docker basics guide for X20 Edge! This guide will help you get started with Docker, a powerful tool for managing containers. Let's dive in! 🚀

## 🛠 Introduction to Docker

Docker is a platform that allows you to develop, ship, and run applications inside containers. Containers are lightweight, portable, and ensure that your application runs consistently across different environments.

- **What is a Container?** 
  A container is a lightweight, stand-alone, executable package that includes everything needed to run an application: code, runtime, system tools, libraries, and settings.
  
- **Why Docker?**
  - Consistency across multiple development, testing, and production environments
  - Simplified dependency management
  - Better resource utilization

## 📥 Installing Docker

X20 edge comes preinstalled with docker.

## 🚀 Basic Docker Commands

Here's a quick rundown of some essential Docker commands:

| Command                          | Description                             |
|----------------------------------|-----------------------------------------|
| ```docker --version```               | Check Docker installation               |
| ```docker pull <image-name>```       | Pull an image from a repository         |
| ```docker run <image-name>```        | Run a container                         |
| ```docker ps```                      | List running containers                 |
| ```docker stop <container-id>```     | Stop a running container                |
| ```docker rm <container-id>```       | Remove a container                      |
| ```docker images```                  | List all images                         |

## 🖼 Using Docker Images

Docker images are the building blocks of containers. They contain the application and its dependencies.

### 🔍 Searching for an Image

To find available images on Docker Hub:
```bash
docker search <image-name>
```

Example:
```bash
docker search ubuntu
```

### 📥 Pulling an Image

To pull an image (download it to your device):
```bash
docker pull <image-name>:<tag>
```

Example:
```bash
docker pull ubuntu:latest
```

### 📜 Listing Images

To list all downloaded images:
```bash
docker images
```

## 📦 Running Docker Containers

Containers are instances of Docker images. Let's run a simple container.

1. **Run a Container**:
   ```bash
   docker run -it ubuntu:latest
   ```
   This command starts an interactive shell in an Ubuntu container.

2. **List Running Containers**:
   ```bash
   docker ps
   ```

3. **Stop a Container**:
   ```bash
   docker stop <container-id>
   ```

4. **Remove a Container**:
   ```bash
   docker rm <container-id>
   ```

### 🌟 Example: Running a Python Container

Let's pull and run a Python container.

1. **Pull the Python Image**:
   ```bash
   docker pull python:3.9
   ```

2. **Run the Python Container**:
   ```bash
   docker run -it python:3.9 python
   ```
   This command will start an interactive Python session inside the container.

## 📚 Conclusion

Congratulations! 🎉 You've successfully learned the basics of Docker on the X20 Edge. This guide covered installing Docker, basic commands, using images, and running containers. Docker is a powerful tool that can streamline your development and deployment processes.

For more information, check out these additional resources:
- [Docker Documentation](https://docs.docker.com/)
- [Docker Hub](https://hub.docker.com/)
