# k3s Infrastructure

This directory contains the Kubernetes manifests for deploying the Blog Generation Platform on Kubernetes clusters.

## Structure

```
infra/k3s/
├── README.md              # This file
├── deploy.sh              # Main deployment script (environment selector)
├── local/                 # Local development configurations
│   ├── deploy-local.sh    # Local deployment script
│   ├── namespaces.yaml    # Namespace definitions
│   ├── backend/           # Backend resources for local dev
│   │   ├── configmap.yaml
│   │   ├── deployment.yaml
│   │   ├── service.yaml
│   │   ├── middleware.yaml
│   │   ├── ingress.yaml
│   │   └── secrets.yaml.example
│   └── frontend/          # Frontend resources for local dev
│       ├── configmap.yaml
│       ├── deployment.yaml
│       ├── service.yaml
│       ├── middleware.yaml
│       └── ingress.yaml
└── server/                # Production server configurations
    ├── deploy-server.sh   # Production deployment script
    ├── namespaces.yaml    # Namespace definitions
    ├── backend/           # Backend resources for production
    │   ├── configmap.yaml
    │   ├── deployment.yaml
    │   ├── service.yaml
    │   ├── middleware.yaml
    │   ├── ingress.yaml
    │   └── secrets.yaml.example
    └── frontend/          # Frontend resources for production
        ├── configmap.yaml
        ├── deployment.yaml
        ├── service.yaml
        ├── middleware.yaml
        └── ingress.yaml
```

## Quick Start

### Local Development

1. Set up the k3d cluster and build images:
   ```bash
   ./setup-local-k3d.sh
   ```

2. Deploy to local environment:
   ```bash
   cd infra/k3s
   ./deploy.sh
   # Select option 1 for Local
   ```

3. Verify the deployment:
   ```bash
   ./verify-setup.sh
   ```

4. Access the application:
   - Frontend: http://blog.local.k3s
   - Backend API: http://api.local.k3s/docs

### Production Server

1. Deploy to production server:
   ```bash
   cd infra/k3s
   ./deploy.sh
   # Select option 2 for Production Server
   ```

2. Update domain configurations:
   - Edit `server/backend/ingress.yaml` and `server/frontend/ingress.yaml`
   - Replace `yourdomain.com` with your actual domain
   - Configure TLS certificates

3. Access the application:
   - Frontend: https://yourdomain.com
   - Backend API: https://api.yourdomain.com/docs

## Teardown

To remove all resources from the cluster:
```bash
./teardown-k3d.sh
```

## Configuration Differences

### Local Environment
- Uses `.local.k3s` domains
- HTTP traffic only (no TLS)
- Local MongoDB and service endpoints
- Development-optimized settings

### Production Environment
- Uses custom domains (`yourdomain.com`)
- HTTPS with TLS certificates
- Production service endpoints
- Production-optimized settings
- Higher resource limits and replicas

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

**Local Development:**
The setup script automatically adds entries to `/etc/hosts`:
```
192.168.107.2 blog.local.k3s api.local.k3s
```

**Production:**
Configure your DNS to point:
- `yourdomain.com` → your cluster load balancer
- `api.yourdomain.com` → your cluster load balancer

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
