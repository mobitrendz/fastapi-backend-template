---
icon: lucide/rocket
---

# CI/CD Deployment

This project includes an automated CI/CD pipeline using GitHub Actions to streamline testing, quality assurance, and deployment for staging and production environments.

## 🏗️ Pipeline Overview

The pipeline is defined in `.github/workflows/deploy.yml` and triggers on every push to the `stage` and `master` branches.

### Workflow Stages

1. **Build and Push**:
   - Automatically builds the project using the multi-stage `Dockerfile`.
   - Pushes the production-ready image to the [GitHub Container Registry (GHCR)](https://ghcr.io).
   - Uses `docker/metadata-action` to tag images with the specific Git commit SHA.

2. **Deploy**:
   - Orchestrated based on the target environment:
     - **Staging**: Triggered by pushes to the `stage` branch.
     - **Production**: Triggered by pushes to the `master` branch.
   - Leverages GitHub Environments to manage secret injection and deployment protection rules.

## ⚙️ Configuration

### GitHub Environments
To use the deployment pipeline, you must configure the following in your repository's **Settings > Environments**:
*   **staging**: Create this environment and add any required deployment secrets (e.g., cloud credentials, host IP).
*   **production**: Create this environment and add your production-specific secrets.

### Security
- **OIDC Authentication**: We recommend configuring OpenID Connect (OIDC) between GitHub Actions and your cloud provider (e.g., AWS IAM roles) to avoid the use of long-lived access keys.

## 🛠️ Extending Deployment
The current deployment job contains a placeholder command. To finalize your CD pipeline, update the `Deploy` step in `.github/workflows/deploy.yml` with your infrastructure's specific CLI commands:

```yaml
- name: Deploy
  run: |
    # Example: Update AWS ECS Service
    aws ecs update-service --cluster my-cluster --service my-service --force-new-deployment

    # Example: Update Kubernetes Deployment
    kubectl rollout restart deployment/fastapi-app -n production
```
