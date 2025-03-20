---
id: docker-compose-offline-setup
title: System without internet access
sidebar_label: System without internet access
sidebar_position: 4
---

# System without internet access

In this tutorial, you will learn how to set up a Docker Compose stack on a machine without internet access. We'll provide each step from having a Docker Compose file and related images on your local machine to getting them onto the remote machine.

:::info

Before proceeding, ensure you have the following installed on your system, these come preinstalled on the X20 Edge:

- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)

:::

## Steps

1. [Export Docker Images](#export-docker-images)
2. [Transfer Docker Images and Compose File](#transfer-docker-images-and-compose-file)
3. [Import Docker Images](#import-docker-images)
4. [Deploy Docker Compose Stack](#deploy-docker-compose-stack)

## Export Docker Images

First, you need to export the Docker images on your local machine.

1. Identify the images required for your Docker Compose setup. These usually can be identified from the `docker-compose.yml` file.
2. Export the images to tar files:

    ```sh
    docker save -o image1.tar image1:tag
    docker save -o image2.tar image2:tag
    ```

    **Example:**

    ```sh
    docker save -o nginx.tar nginx:latest
    docker save -o redis.tar redis:latest
    ```

:::info

If you are saving a Docker image on an **x86_64 (Intel/AMD) machine** and need to transfer it to a **B&R X20 Edge (ARM CPU)**, ensure you pull the correct architecture before saving:

```sh
docker pull --platform linux/arm64 my-image:latest
docker save -o my-image-arm64.tar my-image:latest
```

Without specifying --platform linux/arm64, the default architecture (amd64) may be pulled, causing an ```exec format error``` on the X20 Edge.

:::

## Transfer Docker Images and Compose File

Next, transfer the exported images and the `docker-compose.yml` file to the machine without internet access. You can use external storage devices like USB drives or use SCP if the machines are in the same network.

**Using SCP:**

    ```sh
    scp image1.tar user@remote_machine:/path/to/destination
    scp image2.tar user@remote_machine:/path/to/destination
    scp docker-compose.yml user@remote_machine:/path/to/destination
    ```

## Import Docker Images

On the remote machine, import the Docker images from the tar files.

    ```sh
    docker load -i /path/to/destination/image1.tar
    docker load -i /path/to/destination/image2.tar
    ```

    **Example:**

    ```sh
    docker load -i /home/user/nginx.tar
    docker load -i /home/user/redis.tar
    ```

## Deploy Docker Compose Stack

Finally, navigate to the directory containing the `docker-compose.yml` file and deploy the stack.

    ```sh
    cd /path/to/destination
    docker-compose up -d
    ```

That's it! Your Docker Compose stack should now be up and running on the remote machine without an internet connection.

## Conclusion

By following these steps, you can successfully set up a Docker Compose stack on a machine without internet access. This process involves exporting images from a local machine, transferring them along with the Docker Compose file to the remote machine, and then importing and deploying them.

For more information, refer to the [Docker documentation](https://docs.docker.com/) and [Docker Compose documentation](https://docs.docker.com/compose/).
