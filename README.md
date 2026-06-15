# GuMED Medical Data Platform

Kubernetes-based medical data platform built with FastAPI, PostgreSQL, Metabase and Helm.

## Stack
- **Backend**: FastAPI (Python async)
- **Database**: PostgreSQL via Bitnami Helm chart
- **Analytics**: Metabase BI dashboard
- **Orchestration**: Kubernetes (minikube) + Helm
- **CI/CD**: GitHub Actions
- **Security**: Sealed Secrets, NetworkPolicies, Pod Security Standards
## Local Docker Compose deployment

Build and start the local Docker Compose stack:

```bash
docker compose build --no-cache
docker compose up -d postgres
docker compose up data-loader
docker compose up -d backend metabase
