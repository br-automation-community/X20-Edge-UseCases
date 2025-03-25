---
sidebar_position: 2
---

# 🚀 Getting Started

Welcome to the X20 Edge! This guide will help you set up your device, log in for the first time, and understand the initial configuration steps. Let's get started!

## 📦 Box Contents

When you unbox your X20 Edge, you should find the following items:

- X20 Edge Device
- microSD Card (pre-installed)

## 🌐 Connecting to X20 Edge

To connect to your X20 Edge, follow these steps:

1. **Find the IP Address**: By default, the ETH0 interface is configured with a static IP address (192.168.1.1). The ETH1 interface is set to DHCP. You can use a network scanning tool to locate the device if it's connected to a network with DHCP.

2. **Access the Web Interface**: Open a web browser and enter the IP address of the X20 Edge. For example:
   ```bash
   http://192.168.1.1
   ```

3. **Login Page**: The web interface login page will appear. Use the default credentials to log in:
   - **Username**: ```admin```
   - **Password**: ```admin```

   > **Note**: You will be prompted to change the default password upon the first login.

## 🔐 First Login and Password Change

1. **Login**: Enter the default username and password (both are ```admin```).

2. **Change Password**: You will be prompted to change the default password. Enter the new password and confirm it.

3. **Password Changed**: After changing the password, you will be redirected to the main dashboard.

## 🗺 Navigating the Web Interface

The web interface of the X20 Edge is divided into several sections:

- **Overview**: Provides basic system information such as hostname, serial number, network interfaces, and resource usage.
- **Network Settings**: Configure the network interfaces, choose between static IP and DHCP, and set network parameters.
- **Time Settings**: Adjust the device's date and time settings.
- **Account Management**: Manage user accounts and permissions.
- **System Management**: Perform system updates, backups, and view logs.
- **System Information**: Access detailed information about the system hardware and software.

## 📜 Initial Configuration

1. **Network Settings**:
   - Navigate to the "Network Settings" page.
   - Select the Ethernet interface you wish to configure (ETH0 or ETH1).
   - Choose between static IP and DHCP, and enter the corresponding settings.
   - Save the changes.

2. **Time Settings**:
   - Navigate to the "Time Settings" page.
   - Set the correct date and time or configure NTP (Network Time Protocol) to sync automatically.

3. **System Updates**:
   - Navigate to the "System Management" page.
   - Check for updates and install any available updates to ensure your device is up-to-date.

## 🐳 Next Steps

Now that your X20 Edge is set up, you can start using its powerful features:

- Learn how to [use Docker on X20 Edge](./docker/basics.md) to deploy applications.
- Understand how to clone and create [SD card images](./burning-new-image.md).

## 📚 Additional Resources

- [Official Documentation](https://www.br-automation.com/)
- [Community Support](https://community.br-automation.com/)
- [FAQs](https://www.br-automation.com/en/support/faq/)
