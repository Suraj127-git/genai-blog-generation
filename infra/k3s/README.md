# K3s Deployment Guide - Organized Structure

## 📁 New Directory Structure

```
infra/k3s/
├── base/
│   ├── namespaces.yaml          # Both namespaces (blog-backend, blog-frontend)
│   ├── cluster-issuer.yaml      # Let's Encrypt ClusterIssuer
│   └── certificates.yaml        # TLS certificates for both domains
│
├── backend/
│   ├── configmap.yaml           # Backend configuration (non-sensitive)
│   ├── secrets.yaml.example     # Backend secrets template
│   ├── deployment.yaml          # Backend deployment
│   ├── service.yaml             # Backend service
│   ├── hpa.yaml                 # Horizontal Pod Autoscaler
│   ├── middleware.yaml          # Traefik middlewares (rate limit, CORS, etc.)
│   ├── ingress.yaml             # Traefik IngressRoute
│   └── tls-secret.yaml.example  # TLS certificate template
│
└── frontend/
    ├── configmap.yaml           # Frontend configuration
    ├── deployment.yaml          # Frontend deployment
    ├── service.yaml             # Frontend service
    ├── hpa.yaml                 # Horizontal Pod Autoscaler
    ├── middleware.yaml          # Traefik middlewares (security headers, etc.)
    ├── ingress.yaml             # Traefik IngressRoute
    └── tls-secret.yaml.example  # TLS certificate template
```

## 🎯 Key Features

### Separate Namespaces
- **blog-backend**: All backend resources
- **blog-frontend**: All frontend resources

### Separation of Concerns
Each component has its own file:
- **ConfigMap**: Non-sensitive configuration
- **Secrets**: Sensitive data (API keys, DB credentials)
- **Deployment**: Pod specifications
- **Service**: Network exposure
- **HPA**: Auto-scaling rules
- **Middleware**: Traefik middleware chain
- **Ingress**: Traffic routing rules

### Benefits
✅ **Clear Organization**: Easy to find and manage resources
✅ **Independent Scaling**: Backend and frontend scale separately
✅ **Namespace Isolation**: Better security and resource management
✅ **Modular Updates**: Update components independently
✅ **GitOps Ready**: Perfect for ArgoCD/Flux

## 🚀 Quick Deployment

### 1. Create Namespaces
```bash
kubectl apply -f infra/k3s/base/namespaces.yaml
```

### 2. Install cert-manager
```bash
kubectl apply -f https://github.com/cert-manager/cert-manager/releases/download/v1.13.0/cert-manager.yaml

# Wait for cert-manager to be ready
kubectl wait --for=condition=Ready pods --all -n cert-manager --timeout=300s
```

### 3. Create ClusterIssuer
```bash
# Edit email in cluster-issuer.yaml first!
kubectl apply -f infra/k3s/base/cluster-issuer.yaml
```

### 4. Create Backend Secrets
```bash
# Copy example and edit with real values
cp infra/k3s/backend/secrets.yaml.example infra/k3s/backend/secrets.yaml

# Edit secrets.yaml with your MongoDB URL, GroqAI key, etc.
# Then apply:
kubectl apply -f infra/k3s/backend/secrets.yaml

# Or create from command line:
kubectl create secret generic backend-secrets \
  --from-literal=MONGODB_URL='mongodb+srv://user:pass@cluster.mongodb.net' \
  --from-literal=CHROMADB_HOST='your-chromadb-host.com' \
  --from-literal=GROQ_API_KEY='gsk_your_key' \
  --from-literal=JWT_SECRET_KEY="$(openssl rand -base64 32)" \
  --namespace=blog-backend
```

### 5. Update Configurations
```bash
# Edit these files with your domain names:
# - infra/k3s/backend/ingress.yaml (api.yourdomain.com)
# - infra/k3s/frontend/ingress.yaml (blog.yourdomain.com)
# - infra/k3s/frontend/configmap.yaml (API URL)
# - infra/k3s/backend/middleware.yaml (CORS origins)
# - infra/k3s/base/certificates.yaml (domain names)
# - infra/k3s/base/cluster-issuer.yaml (your email)
```

### 6. Deploy Backend
```bash
kubectl apply -f infra/k3s/backend/
```

### 7. Deploy Frontend
```bash
kubectl apply -f infra/k3s/frontend/
```

### 8. Create TLS Certificates
```bash
# Update domains in certificates.yaml first!
kubectl apply -f infra/k3s/base/certificates.yaml

# Wait for certificates to be issued
kubectl get certificate -n blog-backend
kubectl get certificate -n blog-frontend

# Check cert-manager logs if issues
kubectl logs -n cert-manager -l app=cert-manager
```

## 📋 Verification

### Check All Resources
```bash
# Backend namespace
kubectl get all -n blog-backend
kubectl get configmap,secret,ingress route -n blog-backend

# Frontend namespace
kubectl get all -n blog-frontend
kubectl get configmap,secret,ingressroute -n blog-frontend
```

### Check Pods
```bash
kubectl get pods -n blog-backend
kubectl get pods -n blog-frontend
```

### Check Services
```bash
kubectl get svc -n blog-backend
kubectl get svc -n blog-frontend
```

### Check Ingress Routes
```bash
kubectl get ingressroute -n blog-backend
kubectl get ingressroute -n blog-frontend
```

### Check HPA
```bash
kubectl get hpa -n blog-backend
kubectl get hpa -n blog-frontend
```

### Check Certificates
```bash
kubectl get certificate -n blog-backend
kubectl get certificate -n blog-frontend
kubectl describe certificate frontend-cert -n blog-frontend
kubectl describe certificate backend-cert -n blog-backend
```

## 🔍 Troubleshooting

### Backend Pods Not Starting
```bash
# Check pod status
kubectl describe pod <pod-name> -n blog-backend

# Check logs
kubectl logs -f deployment/backend -n blog-backend

# Check secrets
kubectl get secret backend-secrets -n blog-backend
```

### Frontend Pods Not Starting
```bash
kubectl describe pod <pod-name> -n blog-frontend
kubectl logs -f deployment/frontend -n blog-frontend
```

### Ingress Not Working
```bash
# Check Traefik logs
kubectl logs -n kube-system -l app.kubernetes.io/name=traefik

# Check IngressRoute
kubectl describe ingressroute backend-https -n blog-backend
kubectl describe ingressroute frontend-https -n blog-frontend
```

### Certificate Issues
```bash
# Check certificate status
kubectl describe certificate backend-cert -n blog-backend
kubectl describe certificate frontend-cert -n blog-frontend

# Check cert-manager logs
kubectl logs -n cert-manager -l app=cert-manager

# Check challenges
kubectl get challenges --all-namespaces
```

## 🔄 Updates

### Update Backend
```bash
# Update image
kubectl set image deployment/backend \
  backend=ghcr.io/username/blog-backend:v2.0.0 \
  -n blog-backend

# Check rollout
kubectl rollout status deployment/backend -n blog-backend

# Rollback if needed
kubectl rollout undo deployment/backend -n blog-backend
```

### Update Frontend
```bash
kubectl set image deployment/frontend \
  frontend=ghcr.io/username/blog-frontend:v2.0.0 \
  -n blog-frontend

kubectl rollout status deployment/frontend -n blog-frontend
```

### Update ConfigMap
```bash
# Edit configmap
kubectl edit configmap backend-config -n blog-backend

# Restart deployment to pick up changes
kubectl rollout restart deployment/backend -n blog-backend
```

## 🗑️ Cleanup

### Delete Everything
```bash
# Delete backend
kubectl delete namespace blog-backend

# Delete frontend
kubectl delete namespace blog-frontend

# Or delete specific resources
kubectl delete -f infra/k3s/backend/
kubectl delete -f infra/k3s/frontend/
kubectl delete -f infra/k3s/base/
```

## 📊 Monitoring

### View Logs
```bash
# Backend logs
kubectl logs -f deployment/backend -n blog-backend --tail=100

# Frontend logs
kubectl logs -f deployment/frontend -n blog-frontend --tail=100

# All backend pods
kubectl logs -f -l app=backend -n blog-backend
```

### Resource Usage
```bash
kubectl top pods -n blog-backend
kubectl top pods -n blog-frontend
kubectl top nodes
```

### Events
```bash
kubectl get events -n blog-backend --sort-by='.lastTimestamp'
kubectl get events -n blog-frontend --sort-by='.lastTimestamp'
```

## 🎯 Production Checklist

- [ ] Update all domain names in manifests
- [ ] Create backend secrets with real values
- [ ] Update email in cluster-issuer.yaml
- [ ] Configure MongoDB Atlas connection
- [ ] Configure ChromaDB Cloud endpoint
- [ ] Add GroqAI API key
- [ ] Generate secure JWT secret
- [ ] Point DNS to K3s cluster IP
- [ ] Verify TLS certificates are issued
- [ ] Test both frontend and backend URLs
- [ ] Verify HPA is working
- [ ] Check resource limits are appropriate
- [ ] Enable monitoring (optional)
- [ ] Setup backups for secrets

## 🔐 Security Best Practices

1. **Never commit secrets.yaml** - Add to .gitignore
2. **Use strong JWT secret** - Min 32 characters
3. **Rotate secrets regularly** - Every 90 days
4. **Use RBAC** - Limit service account permissions
5. **Enable network policies** - Restrict pod-to-pod communication
6. **Keep images updated** - Regular security patches
7. **Monitor logs** - Watch for suspicious activity

## 📚 Additional Resources

- Traefik Docs: https://doc.traefik.io/traefik/
- cert-manager Docs: https://cert-manager.io/docs/
- K3s Docs: https://docs.k3s.io/
- Kubernetes Docs: https://kubernetes.io/docs/

---

**Your K3s deployment is now properly organized with separation of concerns!** 🎉
