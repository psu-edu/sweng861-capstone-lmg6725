# SWENG 861: Capstone Project Starter

This is the official starter repository for the **Course Capstone Project**.

Unlike the Weekly Assignments, this project is **Open Domain**. You will use this repository to build your flagship application (Web, Mobile, IoT, or AI) from Week 1 through Week 7.

## 📂 Repository Structure

You are required to maintain a clean structure to facilitate grading and architecture reviews:

/
├── .github/
│   └── workflows/          # [DevOps] CI/CD Pipelines (Build, Test, Deploy)
├── docs/                   # [Documentation] Architecture diagrams, Proposal
├── src/
│   ├── client/             # [Frontend] React / Vue / Mobile App source code
│   └── server/             # [Backend] API / Microservices source code
├── ops/                    # [SRE & Infrastructure]
│   ├── docker/             # Docker Compose & Container configs
│   └── observability/      # [Dashboard] Prometheus.yml, Grafana Dashboards, Screenshots
├── tests/                  # End-to-End (E2E) Test Suites
└── README.md               # The Main Project Documentation


# SWENG 861: Capstone Project Starter

This is the official starter repository for the **Course Capstone Project**.

This project requires a **Full-Stack Implementation** including Frontend, Backend, DevOps Automation, and SRE Observability.

## 📂 Repository Structure

| Folder | Purpose |
| :--- | :--- |
| **`.github/workflows`** | **DevOps:** Place your CI/CD YAML files here (e.g., `ci.yml`). |
| **`src/client`** | **Frontend:** Your Web or Mobile application code (React, Vue, Flutter). |
| **src/server`** | **Backend:** Your API and Database logic (Node, Python, Java). |
| **`ops/docker`** | **Infrastructure:** Dockerfiles and `docker-compose.yml` to run the stack. |
| **`ops/observability`** | **SRE/Dashboard:** Prometheus configs, Grafana JSON exports, or screenshots of your monitoring dashboard. |
| **`docs/`** | **Design:** Your Week 2 Proposal and Architecture diagrams. |

## 🚀 How to Start

### 1. Create Your Repo
1.  Click **"Use this template"** above.
2.  Name your repository: `sweng861-capstone-<yourPSUid>`
3.  Set visibility to **Public** (or Private + invite Instructor).

### 2. Update Your Project Info
Edit this README to include:
* **Project Name & Description**
* **Tech Stack** (e.g., React + Spring Boot + Postgres)
* **How to Run** (Instructions for Local & Docker execution)

---
*This repository is for academic use. Do not commit secrets/API keys.*
