AI Stock Agent: Production-Ready CI/CD on Azure
A containerized Web Application integrated with Google Search API and LangSmith for LLM observability, deployed via a fully automated GitHub Actions pipeline.
🚀 Architecture Overview
This project follows a modern DevOps workflow to ensure zero-downtime deployments and secure secret management:
CI/CD Pipeline: GitHub Actions builds a Docker image on every push to main.
Container Registry: Images are versioned using Git SHA tags and stored in Azure Container Registry (ACR).
Cloud Hosting: Hosted on Azure App Service (Linux).
Security: Uses "keyless" AcrPull authentication via Managed Identity.
🛠 Tech Stack
Backend: Python (LangChain / FastAPI)
Infrastructure: Docker & Azure Container Registry
DevOps: GitHub Actions & Azure App Service
Observability: LangSmith Tracing
📦 Deployment Workflow
The deploy.yml workflow automates the following:
Build: Creates a Docker image on every commit.
Push: Uploads the image to ACR with a unique ${{ github.sha }} tag.
Trigger: Signals the Azure App Service to pull and restart with the fresh image.
📈 Key Learnings
Configured RBAC (Role-Based Access Control) to allow secure communication between cloud resources.
Implemented Managed Identities to eliminate the need for hardcoded registry passwords.
Optimized Azure App Service container settings (WEBSITES_PORT) for custom Docker environments.
