# k3d Infrastructure

This directory contains the Kubernetes manifests for deploying the Blog Generation Platform on k3d.

## Structure

```
infra/k3s/
├── README.md              # This file
├── deploy.sh              # Deployment script
├── namespaces.yaml         # Namespace definitions
├── backend/               # Backend resources
│   ├── configmap.yaml     # Backend configuration
│   ├── deployment.yaml    # Backend deployment
│   ├── service.yaml       # Backend service
│   ├── middleware.yaml    # Traefik middlewares
│   ├── ingress.yaml       # Traefik ingress route
│   └── secrets.yaml.example # Example secrets
└── frontend/              # Frontend resources
    ├── configmap.yaml     # Frontend configuration
    ├── deployment.yaml    # Frontend deployment
    ├── service.yaml       # Frontend service
    ├── middleware.yaml    # Traefik middlewares
    └── ingress.yaml       # Traefik ingress route
```

## Quick Start

1. Set up the k3d cluster and build images:
   ```bash
   ./setup-local-k3d.sh
   ```

2. Deploy the application:
   ```bash
   cd infra/k3s
   ./deploy.sh
   ```

3. Verify the deployment:
   ```bash
   ./verify-setup.sh
   ```

4. Access the application:
   - Frontend: http://blog.local.k3s
   - Backend API: http://api.local.k3s/docs

## Teardown

To remove all resources from the cluster:
```bash
./teardown-k3d.sh
```

## Configuration

### Backend Secrets

Update the backend secrets with your actual values:
```bash
kubectl edit secret backend-secrets -n blog-backend
```

Required secrets:
- `MONGODB_URL`: MongoDB connection string
- `CHROMADB_HOST`: ChromaDB host
- `GROQ_API_KEY`: GroqAI API key
- `JWT_SECRET_KEY`: JWT signing secret

### DNS Configuration

The setup script automatically adds entries to `/etc/hosts`:
```
192.168.107.2 blog.local.k3s api.local.k3s
```

## Development Workflow

1. Make changes to the code
2. Rebuild Docker images:
   ```bash
   ./setup-local-k3d.sh
   ```
3. Restart deployments:
   ```bash
   kubectl rollout restart deployment/backend -n blog-backend
   kubectl rollout restart deployment/frontend -n blog-frontend
   ```

## Troubleshooting

Check pod logs:
```bash
kubectl logs -f deployment/backend -n blog-backend
kubectl logs -f deployment/frontend -n blog-frontend
```

Check events:
```bash
kubectl get events -n blog-backend --sort-by='.lastTimestamp'
kubectl get events -n blog-frontend --sort-by='.lastTimestamp'
```
