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
```

Verify the backend API:

```bash
curl http://localhost:8000/health
curl "http://localhost:8000/api/v1/patients/stats/summary"
```

Expected summary:

```json
{
  "total_records": 303,
  "heart_disease_positive": 165,
  "heart_disease_negative": 138,
  "average_age": 54.4
}
```

Metabase is available at:

```text
http://localhost:3000
```

Docker Compose Metabase database connection:

```text
Host: postgres
Port: 5432
Database: medicaldb
Username: medicaluser
Password: medical123
SSL: disabled
```

---

## Local Kubernetes deployment with k3s and Helm

Verify Kubernetes deployment:

```bash
kubectl get pods -n medical-platform
helm status medical-platform -n medical-platform
```

Expected pods:

```text
medical-platform-backend      1/1 Running
medical-platform-metabase     1/1 Running
medical-platform-postgresql   1/1 Running
```

Verify PostgreSQL data:

```bash
kubectl exec -it -n medical-platform medical-platform-postgresql-0 -- \
  env PGPASSWORD=medical123 \
  psql -h 127.0.0.1 -U medicaluser -d medicaldb \
  -c "SELECT COUNT(*) FROM heart_disease;"
```

Expected result:

```text
303
```

Port-forward FastAPI:

```bash
kubectl port-forward -n medical-platform --address 0.0.0.0 \
  svc/medical-platform-backend 8080:80
```

Verify API:

```bash
curl http://localhost:8080/health
curl "http://localhost:8080/api/v1/patients/stats/summary"
```

Port-forward Metabase:

```bash
kubectl port-forward -n medical-platform --address 0.0.0.0 \
  svc/medical-platform-metabase 3001:80
```

Open Metabase:

```text
http://<VM_IP>:3001
```

Kubernetes Metabase database connection:

```text
Host: medical-platform-postgresql
Port: 5432
Database: medicaldb
Username: medicaluser
Password: medical123
SSL: disabled
```

Example Metabase validation query:

```sql
SELECT target, COUNT(*) AS patients
FROM heart_disease
GROUP BY target
ORDER BY target;
```

Expected result:

```text
target 0 = 138
target 1 = 165
```

---

## Container images

The default Helm values use images published to GitHub Container Registry:

```text
ghcr.io/xwuwux/gumed-medical-api:latest
ghcr.io/xwuwux/gumed-data-loader:latest
```

Images are built and pushed automatically by GitHub Actions using:

```text
.github/workflows/build-ghcr.yml
```

For local k3s development without pulling backend and data-loader images from GHCR, use:

```bash
helm upgrade --install medical-platform ./helm/medical-platform \
  --namespace medical-platform \
  --create-namespace \
  -f helm/medical-platform/values-local.yaml \
  --wait=false
```

For GHCR-based deployment, use:

```bash
helm upgrade --install medical-platform ./helm/medical-platform \
  --namespace medical-platform \
  --create-namespace \
  --wait=false
```

---

## CI/CD status

![CI/CD Pipeline](https://github.com/xWuWux/GuMED-Data-Postgres-Kaggle/actions/workflows/ci-cd.yml/badge.svg)

![Build and Push Images to GHCR](https://github.com/xWuWux/GuMED-Data-Postgres-Kaggle/actions/workflows/build-ghcr.yml/badge.svg)
