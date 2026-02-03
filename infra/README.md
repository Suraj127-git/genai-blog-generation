# Blog Generation - K3s Infrastructure

Production-ready Kubernetes (K3s) infrastructure with Traefik ingress, auto-scaling, and cloud-native services.

## Architecture Overview

```
┌─────────────────┐
│   Traefik       │ ← HTTPS/TLS (Let's Encrypt)
│   Ingress       │
└────────┬────────┘
         │
    ┌────┴─────┐
    │          │
┌───▼───┐  ┌──▼────┐
│Frontend│  │Backend│
│(React) │  │(FastAPI)
└───┬───┘  └──┬────┘
    │         │
    │    ┌────┴──────┬───────────┐
    │    │           │           │
    │  ┌─▼──────┐ ┌─▼────────┐ ┌▼──────┐
    │  │MongoDB │ │ChromaDB  │ │GroqAI │
    │  │ Atlas  │ │  Cloud   │ │  API  │
    │  └────────┘ └──────────┘ └───────┘
    │
    └─ Static Assets (CDN)
```

## Prerequisites

### Required
- **K3s cluster** (v1.28+)
- **kubectl** configured
- **Traefik** (installed with K3s by default)
- **MongoDB Atlas** account (or cloud MongoDB)
- **ChromaDB Cloud** account (or self-hosted)
- **GroqAI** API key
- **Domain names** (blog.yourdomain.com, api.yourdomain.com)

### Optional
- **cert-manager** for automatic TLS certificates
- **Prometheus + Grafana** for monitoring
- **GitHub Container Registry** access

## Quick Start

### 1. Setup Cloud Services

#### MongoDB Atlas
```bash
# Create cluster at https://cloud.mongodb.com
# Get connection string:
mongodb+srv://username:password@cluster.mongodb.net/blog_generation
```

#### ChromaDB Cloud
```bash
# Sign up at https://www.trychroma.com/
# Or self-host ChromaDB and get endpoint
```

#### GroqAI
```bash
# Get API key from https://console.groq.com/
```

### 2. Configure Kubernetes Secrets

```bash
# Create namespace
kubectl apply -f k3s/namespace.yaml

# Create secrets
kubectl create secret generic app-secrets \
  --from-literal=MONGODB_URL='mongodb+srv://user:pass@cluster.mongodb.net/blog_generation' \
  --from-literal=GROQ_API_KEY='gsk_your_groq_api_key' \
  --from-literal=JWT_SECRET_KEY="$(openssl rand -base64 32)" \
  --namespace=blog-generation

# Verify secrets
kubectl get secrets -n blog-generation
```

### 3. Install cert-manager (for TLS)

```bash
# Install cert-manager
kubectl apply -f https://github.com/cert-manager/cert-manager/releases/download/v1.13.0/cert-manager.yaml

# Wait for cert-manager pods
kubectl wait --for=condition=Ready pods --all -n cert-manager --timeout=300s
```

### 4. Create Let's Encrypt ClusterIssuer

```bash
cat <<EOF | kubectl apply -f -
apiVersion: cert-manager.io/v1
kind: ClusterIssuer
metadata:
  name: letsencrypt-prod
spec:
  acme:
    server: https://acme-v02.api.letsencrypt.org/directory
    email: your-email@example.com
    privateKeySecretRef:
      name: letsencrypt-prod
    solvers:
    - http01:
        ingress:
          class: traefik
EOF
```

### 5. Create TLS Certificate

```bash
cat <<EOF | kubectl apply -f -
apiVersion: cert-manager.io/v1
kind: Certificate
metadata:
  name: blog-tls-cert
  namespace: blog-generation
spec:
  secretName: blog-tls-cert
  issuerRef:
    name: letsencrypt-prod
    kind: ClusterIssuer
  dnsNames:
  - blog.yourdomain.com
  - api.yourdomain.com
EOF

# Wait for certificate
kubectl get certificate -n blog-generation -w
```

### 6. Update ConfigMaps

Edit `k3s/backend-deployment.yaml` and `k3s/frontend-deployment.yaml`:

```yaml
# backend-deployment.yaml
data:
  MONGODB_URL: "<your-real-mongodb-url>"
  CHROMADB_HOST: "<your-chromadb-host>"

# frontend-deployment.yaml
data:
  VITE_API_BASE_URL: "https://api.yourdomain.com/api/v1"
```

### 7. Update Ingress Domains

Edit `k3s/ingress.yaml`:

```yaml
# Replace yourdomain.com with your actual domain
- match: Host(`blog.yourdomain.com`)
- match: Host(`api.yourdomain.com`)
```

### 8. Deploy Application

```bash
# Apply all manifests
kubectl apply -f k3s/

# Verify deployments
kubectl get all -n blog-generation

# Check pods are running
kubectl get pods -n blog-generation

# Check services
kubectl get svc -n blog-generation

# Check ingress routes
kubectl get ingressroute -n blog-generation
```

### 9. Verify Deployment

```bash
# Check pod logs
kubectl logs -f deployment/backend -n blog-generation
kubectl logs -f deployment/frontend -n blog-generation

# Check if HPA is working
kubectl get hpa -n blog-generation

# Test health endpoints
kubectl run test --rm -it --image=curlimages/curl -- \
  http://backend.blog-generation.svc.cluster.local:8000/health
```

### 10. Access Application

```bash
# Check ingress
kubectl get ingressroute -n blog-generation

# Access application
# https://blog.yourdomain.com
# https://api.yourdomain.com/docs (Swagger UI)
```

## DNS Configuration

Point your domains to your K3s cluster IP:

```bash
# Get Traefik service IP
kubectl get svc -n kube-system traefik

# Add DNS A records:
# blog.yourdomain.com    → <TRAEFIK_IP>
# api.yourdomain.com     → <TRAEFIK_IP>
```

## Scaling

### Manual Scaling

```bash
# Scale backend
kubectl scale deployment backend --replicas=5 -n blog-generation

# Scale frontend
kubectl scale deployment frontend --replicas=3 -n blog-generation
```

### Auto-Scaling (HPA)

HPA is configured automatically. Check status:

```bash
# View HPA status
kubectl get hpa -n blog-generation

# Backend: min=3, max=10, target CPU=70%
# Frontend: min=2, max=5, target CPU=70%
```

## Monitoring

### View Logs

```bash
# Backend logs
kubectl logs -f deployment/backend -n blog-generation --tail=100

# Frontend logs
kubectl logs -f deployment/frontend -n blog-generation --tail=100

# All pods
kubectl logs -f -l app=backend -n blog-generation
```

### Resource Usage

```bash
# Pod resources
kubectl top pods -n blog-generation

# Node resources
kubectl top nodes
```

### Events

```bash
# Recent events
kubectl get events -n blog-generation --sort-by='.lastTimestamp'
```

## Troubleshooting

### Pods Not Starting

```bash
# Describe pod
kubectl describe pod <pod-name> -n blog-generation

# Check events
kubectl get events -n blog-generation

# Check logs
kubectl logs <pod-name> -n blog-generation
```

### Database Connection Issues

```bash
# Test MongoDB connection from pod
kubectl exec -it deployment/backend -n blog-generation -- \
  python -c "from pymongo import MongoClient; print(MongoClient('$MONGODB_URL').server_info())"

# Check secrets
kubectl get secret app-secrets -n blog-generation -o jsonpath='{.data.MONGODB_URL}' | base64 -d
```

### Ingress Not Working

```bash
# Check Traefik logs
kubectl logs -n kube-system -l app.kubernetes.io/name=traefik

# Check ingress routes
kubectl get ingressroute -n blog-generation -o yaml

# Verify DNS
nslookup blog.yourdomain.com
```

### TLS Certificate Issues

```bash
# Check certificate status
kubectl describe certificate blog-tls-cert -n blog-generation

# Check cert-manager logs
kubectl logs -n cert-manager -l app=cert-manager

# Force renewal
kubectl delete secret blog-tls-cert -n blog-generation
```

## Updating Application

### Rolling Update

```bash
# Update backend image
kubectl set image deployment/backend \
  backend=ghcr.io/username/blog-backend:v2.0.0 \
  -n blog-generation

# Update frontend image
kubectl set image deployment/frontend \
  frontend=ghcr.io/username/blog-frontend:v2.0.0 \
  -n blog-generation

# Check rollout status
kubectl rollout status deployment/backend -n blog-generation
kubectl rollout status deployment/frontend -n blog-generation
```

### Rollback

```bash
# Rollback backend
kubectl rollout undo deployment/backend -n blog-generation

# Rollback to specific revision
kubectl rollout undo deployment/backend --to-revision=2 -n blog-generation
```

## Backup & Restore

### Application State

**MongoDB Atlas** provides automatic backups.

### Kubernetes Resources

```bash
# Backup all manifests
kubectl get all,configmap,secret,ingressroute -n blog-generation -o yaml > backup.yaml

# Restore
kubectl apply -f backup.yaml
```

## Security Best Practices

1. **Use Secrets** - Never hardcode credentials
2. **Enable RBAC** - Limit service account permissions
3. **Network Policies** - Restrict pod-to-pod communication
4. **Pod Security** - Run as non-root user
5. **TLS Everywhere** - Force HTTPS
6. **Rate Limiting** - Configured in Traefik middleware
7. **Security Headers** - Configured in Traefik middleware

## Performance Optimization

1. **Resource Requests/Limits** - Set appropriate values
2. **HPA** - Auto-scale based on load
3. **Caching** - Frontend static assets cached
4. **CDN** - Use for static assets (optional)
5. **Connection Pooling** - MongoDB connection pooling enabled

## Cost Optimization

1. **Right-size resources** - Monitor and adjust
2. **Use spot instances** - For non-critical workloads
3. **Auto-scaling** - Scale down during low traffic
4. **MongoDB Atlas** - M0 Free tier for development
5. **ChromaDB Cloud** - Free tier available

## CI/CD Integration

GitHub Actions automatically deploys on push to main branch.

Required secrets:
- `KUBE_CONFIG_PRODUCTION` - Base64 encoded kubeconfig
- `SLACK_WEBHOOK_URL` - Slack notifications
- `DISCORD_WEBHOOK` - Discord notifications
- `SNYK_TOKEN` - Security scanning

## Useful Commands

```bash
# Get all resources
kubectl get all -n blog-generation

# Port forward for testing
kubectl port-forward svc/backend 8000:8000 -n blog-generation
kubectl port-forward svc/frontend 8080:80 -n blog-generation

# Execute commands in pod
kubectl exec -it deployment/backend -n blog-generation -- /bin/bash

# Copy files from pod
kubectl cp blog-generation/<pod-name>:/path/to/file ./local-file

# Delete all resources
kubectl delete namespace blog-generation
```

## Support

For issues:
1. Check logs: `kubectl logs -f deployment/<name> -n blog-generation`
2. Check events: `kubectl get events -n blog-generation`
3. Check pod status: `kubectl describe pod <pod> -n blog-generation`

## License

MIT
