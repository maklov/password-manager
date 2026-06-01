# Password Manager API

This repository contains the backend API component for a personal password management system. It is designed as a modular, containerized service to ensure high portability and ease of deployment.

## Architecture & Design
The project follows a **Separation of Concerns** principle. This repository focuses exclusively on the backend API logic and containerization, keeping it decoupled from the client-side implementation (Swift/SwiftUI).

## Tech Stack
* **Framework:** [FastAPI](https://fastapi.tiangolo.com/) (Python) – chosen for its high performance and automatic interactive API documentation.
* **Containerization:** Docker & Docker Compose.
* **Infrastructure:** Designed to run on a self-hosted Proxmox environment with LXC containers.

## Getting Started

### Prerequisites
* Docker & Docker Compose installed on your machine.
* Python 3.10+

### Running the Service
1. Clone the repository:
   ```bash
   git clone https://github.com/maklov/password-manager.git
   cd password-manager
   ```
2. Build and run using Docker Compose:
   ```bash
   docker-compose up --build
   ```
3. The API will be available at http://localhost:8000 (or your configured port).

## Project Status

The project is under active development.
- [x] Core API endpoints skeleton
- [x] Dockerization & environment configuration
- [ ] Implementation of cryptographic modules
- [ ] Database integration and schema design
- [ ] Unit testing (pytest)

## Note on Architecture
This repository focuses solely on the backend API and container configuration. Client-side applications (mobile/desktop) are developed in separate repositories to maintain a clean codebase and facilitate independent deployment cycles.
