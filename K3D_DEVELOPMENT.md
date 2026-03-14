# k3d Development Guide - Blog Generation Platform

This guide will help you set up the AI-powered blog generation platform locally using k3d.

## What is k3d?

k3d is a lightweight wrapper that runs k3s (Rancher Lab's lightweight Kubernetes distribution) in Docker containers. It provides a fast and easy way to run Kubernetes clusters locally.

## Prerequisites

### Required Software
- **Docker** - Container runtime
- **k3d** - Kubernetes in Docker
- **kubectl** - Kubernetes CLI

### Cloud Services (Free Tiers Available)
- **MongoDB Atlas** - Database (M0 free tier)
- **GroqAI** - AI API key (free tier)
- **ChromaDB** - Vector database (self-hosted or cloud)

## Quick Setup with k3d

### 1. Install k3d (if not already installed)

```bash
# Install k3d
curl -s https://raw.githubusercontent.com/k3d-io/k3d/main/install.sh | bash

# Verify installation
k3d version
```

### 2. Run the k3d Setup Script

```bash
# Navigate to project root
cd /Users/suraj/code/genai-blog-generation

# Run the k3d setup script
./setup-local-k3d.sh
```

This script will:
- ✅ Check if k3d cluster exists and is running
- ✅ Build Docker images for backend and frontend
- ✅ Import images into k3d cluster
- ✅ Configure local DNS entries
- ✅ Show next steps

### 3. Configure Cloud Services

#### MongoDB Atlas
1. Sign up at https://cloud.mongodb.com/
2. Create a free M0 cluster
3. Get connection string: `mongodb+srv://username:password@cluster.mongodb.net/blog_generation`

#### GroqAI
1. Sign up at https://console.groq.com/
2. Get API key: `gsk_your_api_key_here`

#### ChromaDB (Optional - can use local)
1. Either use ChromaDB Cloud or self-host
2. For local: `pip install chromadb` and run on localhost:8000

### 4. Update Kubernetes Secrets

```bash
# Edit the backend secrets with your actual values
kubectl edit secret backend-secrets -n blog-backend
```

Update these values:
- `MONGODB_URL`: Your MongoDB Atlas connection string
- `GROQ_API_KEY`: Your GroqAI API key  
- `CHROMADB_HOST`: Your ChromaDB host (localhost for self-hosted)
- `JWT_SECRET_KEY`: Generate a secure secret (change from default)

### 5. Deploy the Application

```bash
# Deploy to k3d
cd infra/k3s
./deploy-local.sh

# Verify deployment
cd ../..
./verify-setup.sh
```

### 6. Access the Application

- **Frontend**: http://blog.local.k3s
- **Backend API**: http://api.local.k3s/docs
- **API Health**: http://api.local.k3s/health

## k3d-Specific Features

### Image Management

With k3d, images are imported into the cluster:

```bash
# Build and import backend image
cd backend
docker build -t blog-backend:local -f ../infra/docker/backend.Dockerfile .
k3d image import blog-backend:local -c k3d-dev

# Build and import frontend image
cd ../frontend
docker build -t blog-frontend:local -f ../infra/docker/frontend.Dockerfile .
k3d image import blog-frontend:local -c k3d-dev
```

### Cluster Management

```bash
# List clusters
k3d cluster list

# Stop cluster
k3d cluster stop k3d-dev

# Start cluster
k3d cluster start k3d-dev

# Delete cluster
k3d cluster delete k3d-dev

# Create new cluster with port mappings
k3d cluster create dev --port "8080:80@loadbalancer" --port "8000:8000@loadbalancer"
```

### Networking

k3d uses Docker networking. The special hostname `host.k3d.internal` allows containers to reach services on the host machine.

## Development Workflow

### Making Changes

#### Backend Changes
```bash
# Rebuild backend image
cd backend
docker build -t blog-backend:local -f ../infra/docker/backend.Dockerfile .
k3d image import blog-backend:local -c k3d-dev

# Restart deployment
kubectl rollout restart deployment/backend -n blog-backend
```

#### Frontend Changes
```bash
# Rebuild frontend image
cd frontend  
docker build -t blog-frontend:local -f ../infra/docker/frontend.Dockerfile .
k3d image import blog-frontend:local -c k3d-dev

# Restart deployment
kubectl rollout restart deployment/frontend -n blog-frontend
```

### Viewing Logs

```bash
# Backend logs
kubectl logs -f deployment/backend -n blog-backend

# Frontend logs
kubectl logs -f deployment/frontend -n blog-frontend

# All pods
kubectl get pods --all-namespaces
```

### Debugging

```bash
# Check pod status
kubectl describe pod <pod-name> -n blog-backend

# Access pod shell
kubectl exec -it <pod-name> -n blog-backend -- /bin/bash

# Port forward for testing
kubectl port-forward svc/backend 8000:8000 -n blog-backend
kubectl port-forward svc/frontend 8080:80 -n blog-frontend
```

## Troubleshooting

### Common k3d Issues

#### Cluster Not Running
```bash
# Check cluster status
k3d cluster list

# Start cluster if stopped
k3d cluster start k3d-dev

# Create new cluster
k3d cluster create dev --port "8080:80@loadbalancer" --port "8000:8000@loadbalancer"
```

#### Image Not Found
```bash
# Check if image is imported
k3d image list -c k3d-dev

# Import image manually
k3d image import blog-backend:local -c k3d-dev
```

#### DNS Issues
```bash
# Check /etc/hosts entries
cat /etc/hosts | grep k3s

# Get k3d server IP
docker inspect k3d-dev-server-0 | jq -r '.[0].NetworkSettings.Networks["k3d-dev"].IPAddress'
```

#### Pods Not Starting
```bash
# Check events
kubectl get events -n blog-backend --sort-by='.lastTimestamp'

# Check secrets
kubectl get secret backend-secrets -n blog-backend -o yaml

# Check configmaps
kubectl get configmap backend-config -n blog-backend -o yaml
```

### Reset Everything

```bash
# Delete namespaces
kubectl delete namespace blog-backend blog-frontend

# Delete and recreate k3d cluster
k3d cluster delete k3d-dev
k3d cluster create dev --port "8080:80@loadbalancer" --port "8000:8000@loadbalancer"

# Redeploy
cd infra/k3s
./deploy-local.sh
```

## Performance Tips

### k3d Optimizations
- Use local images with `k3d image import`
- Reduce resource limits for local development
- Use single replicas for development
- Enable debug mode for better logging

### Resource Usage
- k3d containers use fewer resources than full VMs
- Can run multiple clusters simultaneously
- Fast startup and shutdown times

## k3d vs Other Options

| Feature | k3d | Docker Desktop | Minikube |
|---------|-----|----------------|----------|
| Resource Usage | Low | Medium | High |
| Startup Time | Fast | Medium | Slow |
| Docker Integration | Native | Native | Good |
| Kubernetes Version | Latest | Configurable | Configurable |
| Port Forwarding | Easy | Easy | Manual |

## Configuration Files

The k3d setup uses these local configuration files:

```
infra/k3s/
├── backend/
│   ├── configmap-local.yaml     # Backend config (k3d)
│   ├── deployment-local.yaml   # Backend deployment (k3d)
│   ├── ingress-local.yaml      # Backend ingress (k3d)
│   └── middleware-local.yaml   # Traefik middleware (k3d)
├── frontend/
│   ├── configmap-local.yaml     # Frontend config (k3d)
│   ├── deployment-local.yaml   # Frontend deployment (k3d)
│   └── ingress-local.yaml      # Frontend ingress (k3d)
└── deploy-local.sh              # Local deployment script
```

## Next Steps

1. **Test the Application**
   - Create a user account
   - Upload a document
   - Generate a blog post

2. **Explore the Code**
   - Backend: `/backend/app/` - FastAPI application
   - Frontend: `/frontend/src/` - React TypeScript app

3. **Configure Production**
   - Review `/infra/k3s/README.md` for production deployment
   - Set up proper TLS certificates
   - Configure proper domains

## Support

For k3d-specific issues:
1. Check k3d documentation: https://k3d.io/
2. Verify cluster status: `k3d cluster list`
3. Check pod logs: `kubectl logs -f deployment/<name> -n <namespace>`
4. Review this guide first

---

**Happy k3d Development! 🐳🚀**
