# Docker Installation Guide

This guide explains how to install Docker on different operating systems to run the cybersecurity portfolio website in containers.

## Windows

### Docker Desktop for Windows

1. **System Requirements**:
   - Windows 10 Pro, Enterprise, or Education (Build 15063 or later)
   - Enable Hyper-V and Containers Windows features
   - Enable BIOS-level hardware virtualization

2. **Installation Steps**:
   - Download Docker Desktop for Windows from [Docker Hub](https://hub.docker.com/editions/community/docker-ce-desktop-windows)
   - Run the installer as Administrator
   - Follow the installation wizard
   - Restart your computer if prompted

3. **Post-Installation**:
   - Start Docker Desktop from the Start menu
   - Wait for Docker to initialize
   - Verify installation by running:
     ```powershell
     docker --version
     docker-compose --version
     ```

### Windows Subsystem for Linux (WSL) 2

If you prefer to use WSL 2:

1. Install WSL 2:
   ```powershell
   wsl --install
   ```

2. Install Docker Desktop (which includes WSL 2 backend support)

## macOS

### Docker Desktop for Mac

1. **System Requirements**:
   - macOS 10.15 or newer
   - At least 4 GB of RAM

2. **Installation Steps**:
   - Download Docker Desktop for Mac from [Docker Hub](https://hub.docker.com/editions/community/docker-ce-desktop-mac)
   - Double-click Docker.dmg to open the installer
   - Drag the Docker icon to the Applications folder
   - Start Docker from the Applications folder

3. **Post-Installation**:
   - Start Docker from the Applications folder or Launchpad
   - Wait for Docker to initialize
   - Verify installation by running:
     ```bash
     docker --version
     docker-compose --version
     ```

## Linux (Ubuntu/Debian)

### Install Docker Engine

1. Update package index:
   ```bash
   sudo apt-get update
   ```

2. Install prerequisites:
   ```bash
   sudo apt-get install \
     apt-transport-https \
     ca-certificates \
     curl \
     gnupg \
     lsb-release
   ```

3. Add Docker's official GPG key:
   ```bash
   curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
   ```

4. Set up the stable repository:
   ```bash
   echo \
     "deb [arch=amd64 signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu \
     $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
   ```

5. Update package index again:
   ```bash
   sudo apt-get update
   ```

6. Install Docker Engine:
   ```bash
   sudo apt-get install docker-ce docker-ce-cli containerd.io
   ```

7. Add your user to the docker group:
   ```bash
   sudo usermod -aG docker $USER
   ```

8. Log out and log back in for the group changes to take effect.

### Install Docker Compose

1. Download the current stable release of Docker Compose:
   ```bash
   sudo curl -L "https://github.com/docker/compose/releases/download/v2.20.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
   ```

2. Apply executable permissions:
   ```bash
   sudo chmod +x /usr/local/bin/docker-compose
   ```

3. Create a symbolic link:
   ```bash
   sudo ln -s /usr/local/bin/docker-compose /usr/bin/docker-compose
   ```

4. Verify installation:
   ```bash
   docker-compose --version
   ```

## Verification

After installation, verify that Docker is working correctly:

```bash
docker run hello-world
```

This command downloads a test image and runs it in a container. When the container runs, it prints a message and exits.

## Troubleshooting

### Common Issues

1. **Permission denied**:
   - Make sure your user is in the docker group
   - Log out and log back in after adding your user to the docker group

2. **Cannot connect to the Docker daemon**:
   - Make sure Docker is running
   - On Linux, start Docker with: `sudo systemctl start docker`

3. **WSL 2 backend not working on Windows**:
   - Make sure WSL 2 is properly installed and set as default
   - Update WSL 2 kernel: https://aka.ms/wsl2kernel

### Resources

- [Docker Documentation](https://docs.docker.com/)
- [Docker Desktop](https://www.docker.com/products/docker-desktop)
- [Docker Compose](https://docs.docker.com/compose/)