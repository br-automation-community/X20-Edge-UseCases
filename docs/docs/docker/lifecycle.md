---
sidebar_position: 5
---

# Pulling images from registries

This section explains the Docker lifecycle on the X20 Edge, specifically focusing on pulling Docker images.

## Pulling Docker Images

Docker images are the foundation of containers. They are lightweight, standalone, and executable software packages that include everything needed to run an application. Below are the steps for pulling Docker images.

:::info

Before proceeding, ensure you have the following installed on your system, these come preinstalled on the X20 Edge:

- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)

Also make sure that your device has internet connectivity to access Docker Hub or a custom registry.

:::

### Pulling Images from Docker Hub

Docker Hub is a cloud-based repository where Docker users push and pull container images.

1. **Open Terminal**: Connect to your X20 Edge and open the terminal.

2. **Log in to Docker Hub (Optional)**: You can pull public images without logging in, but for private repositories, you need to authenticate.
   ```bash
   docker login
   ```
   Enter your Docker Hub username and password when prompted.

3. **Search for Images**: To find available images, use the `docker search` command.
   ```bash
   docker search <image-name>
   ```
   Example:
   ```bash
   docker search ubuntu
   ```

4. **Pull an Image**: To download an image to your device, use the `docker pull` command.
   ```bash
   docker pull <image-name>:<tag>
   ```
   Example:
   ```bash
   docker pull ubuntu:latest
   ```

5. **Verify the Image**: After pulling, verify that the image is available locally.
   ```bash
   docker images
   ```

### Using a Custom Registry

If your organization hosts private images in a custom registry, follow these steps:

1. **Log in to Custom Registry**: Authenticate to your custom Docker registry.
   ```bash
   docker login <registry-url>
   ```
   Enter your registry username and password when prompted.

2. **Pull an Image from the Custom Registry**: Specify the registry URL along with the image name.
   ```bash
   docker pull <registry-url>/<image-name>:<tag>
   ```
   Example:
   ```bash
   docker pull myregistry.com/myapp:latest
   ```

3. **Verify the Image**: Check that the pulled image is listed among your local Docker images.
   ```bash
   docker images
   ```

### Example: Pulling a Python Image

Here’s a practical example of pulling a Python image and running a simple Python container:

1. **Pull the Python Image**:
   ```bash
   docker pull python:3.9
   ```

2. **Run a Python Container**:
   ```bash
   docker run -it python:3.9 python
   ```
   This command will start an interactive Python session inside the container.

### Additional Resources

- [Docker Hub](https://hub.docker.com/)
- [Docker Documentation: Pulling Images](https://docs.docker.com/engine/reference/commandline/pull/)

