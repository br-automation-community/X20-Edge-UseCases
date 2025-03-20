---
title: Docker Compose Watch
description: Learn how to use `docker compose watch` for live updates in your development workflow.
sidebar_position: 3
---

# Docker Compose Watch

`docker compose watch` is a feature that enables **automatic rebuilds and restarts** of services when files change. This is useful in **development environments**, where frequent code modifications require a quick feedback loop.

## 🚀 Why Use It?
- **Automatically detects changes** in your source files.
- **Rebuilds and restarts services** when necessary.
- **Reduces manual effort** in development workflows.

## 🔧 Basic Usage

To enable file watching, define a `watch` section in `docker-compose.yml`:

```yaml
services:
  app:
    build: .
    volumes:
      - .:/app
    develop:
      watch:
        - path: ./src
          action: sync
        - path: ./Dockerfile
          action: rebuild
```

### Explanation:
- `sync`: Synchronizes changes **without restarting** the container.
- `rebuild`: Triggers a **full image rebuild** and restart.

### Starting the Watch Mode
Run the following command to enable live watching:

```sh
docker compose watch
```

This starts the services (if they are not already running) and monitors file changes.

## ⚙️ Watch Actions

| Action   | Description |
|----------|------------|
| `sync`   | Syncs file changes **into the running container** without restarting. |
| `rebuild` | Triggers a **full rebuild** when files change. |
| `restart` | Restarts the container without rebuilding. |

## 🎯 Use Cases
### 1️⃣ Live Code Sync Without Restart
For interpreted languages (e.g., **Python, JavaScript**), use `sync` to reflect changes without downtime.

### 2️⃣ Automatic Rebuilds for Configuration Changes
Use `rebuild` to trigger updates when modifying **Dockerfiles or dependency files** (e.g., `requirements.txt`, `package.json`).

### 3️⃣ Auto-Restart for Configuration Updates
If config files change (e.g., `.env`, `.yaml`), `restart` ensures the container reloads them.

## 🔄 Comparison: `docker compose watch` vs. Bind Mounts

| Feature | `docker compose watch` | Bind Mounts (`volumes`) |
|---------|------------------------|-------------------------|
| Updates files in container | ✅ | ✅ |
| Triggers rebuild on changes | ✅ | ❌ |
| Works across OS platforms | ✅ | Some issues on Windows/macOS |
| Auto-restarts services | ✅ | ❌ |

## 🏗️ When Should You Use It?
✅ **Development workflows** that require live updates.
✅ **Containerized applications** where code needs frequent rebuilding.
✅ **Projects with dependency management**, such as Python (`requirements.txt`) or Node.js (`package.json`).

## 📌 Conclusion
`docker compose watch` simplifies containerized development by eliminating the need for manual rebuilds and restarts. It’s especially useful when working on **IoT edge devices, microservices, or cloud applications**.

---

### 💡 Need More Help?
Check out the official Docker documentation: [Docker Compose Watch](https://docs.docker.com/compose/how-tos/file-watch/).
