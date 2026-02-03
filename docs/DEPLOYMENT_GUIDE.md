# Deployment Guide - VPS/Cloud Deployment

This guide covers deploying the AI-Powered Blog Generation Platform to various cloud providers and VPS services including AWS, DigitalOcean, Hostinger, Linode, and others.

## 📋 Table of Contents

- [Prerequisites](#prerequisites)
- [Pre-Deployment Setup](#pre-deployment-setup)
- [Cloud Provider Setup](#cloud-provider-setup)
  - [AWS EC2](#aws-ec2)
  - [DigitalOcean](#digitalocean)
  - [Hostinger VPS](#hostinger-vps)
  - [Linode](#linode)
  - [Vultr](#vultr)
- [K3s Installation](#k3s-installation)
- [Application Deployment](#application-deployment)
- [Post-Deployment Configuration](#post-deployment-configuration)
- [Troubleshooting](#troubleshooting)

---

## Prerequisites

### Required Services
Before deployment, you need accounts and credentials for:

1. **MongoDB Atlas** (Free tier available)
   - Sign up at: https://www.mongodb.com/cloud/atlas
   - Create a cluster and get connection string

2. **ChromaDB Cloud** or self-hosted ChromaDB
   - Cloud: https://www.trychroma.com/
   - Or deploy your own ChromaDB instance

3. **GroqAI API Key** (Free tier available)
   - Sign up at: https://console.groq.com/
   - Get API key from dashboard

4. **Domain Name** (Optional but recommended)
   - For production deployment with TLS
   - Can use Cloudflare, Namecheap, GoDaddy, etc.

### Local Requirements
- Git
- kubectl (Kubernetes CLI)
- Docker (for building images locally, optional)
- SSH client

---

## Pre-Deployment Setup

### 1. Prepare Your Credentials

Create a file to store your credentials (DO NOT commit this):

```bash
# MongoDB
MONGODB_URL=mongodb+srv://username:password@cluster.mongodb.net/blog_generation?retryWrites=true&w=majority

# ChromaDB
CHROMADB_HOST=your-chromadb-host.com
CHROMADB_PORT=443

# GroqAI
GROQ_API_KEY=gsk_your_api_key_here

# JWT Secret (generate a random string)
JWT_SECRET_KEY=$(openssl rand -base64 32)

# Domain (if you have one)
FRONTEND_DOMAIN=blog.yourdomain.com
BACKEND_DOMAIN=api.yourdomain.com
```

### 2. Clone the Repository

```bash
git clone https://github.com/yourusername/genai-blog-generation.git
cd genai-blog-generation
```

---

## Cloud Provider Setup

Choose one of the following providers based on your preference and budget.

### AWS EC2

#### Recommended Instance
- **Type**: t3.medium or t3.large
- **OS**: Ubuntu 22.04 LTS
- **Storage**: 30GB+ SSD
- **RAM**: 4GB minimum, 8GB recommended

#### Setup Steps

1. **Launch EC2 Instance**
   ```bash
   # From AWS Console:
   # - Choose Ubuntu 22.04 LTS AMI
   # - Select t3.medium instance type
   # - Configure security group (ports: 22, 80, 443, 6443)
   # - Launch and download key pair
   ```

2. **Connect to Instance**
   ```bash
   chmod 400 your-key.pem
   ssh -i your-key.pem ubuntu@your-ec2-public-ip
   ```

3. **Configure Security Group**
   - Inbound Rules:
     - SSH (22) - Your IP
     - HTTP (80) - 0.0.0.0/0
     - HTTPS (443) - 0.0.0.0/0
     - K3s API (6443) - Your IP (for kubectl access)

4. **Update System**
   ```bash
   sudo apt update && sudo apt upgrade -y
   ```

---

### DigitalOcean

#### Recommended Droplet
- **Size**: Basic - 4GB RAM / 2 vCPUs ($24/month)
- **OS**: Ubuntu 22.04 LTS
- **Region**: Choose closest to your users

#### Setup Steps

1. **Create Droplet**
   ```bash
   # From DigitalOcean Console:
   # - Click "Create" → "Droplets"
   # - Choose Ubuntu 22.04
   # - Select 4GB/2vCPU plan
   # - Add SSH key
   # - Create Droplet
   ```

2. **Connect to Droplet**
   ```bash
   ssh root@your-droplet-ip
   ```

3. **Configure Firewall**
   ```bash
   # From DigitalOcean Console or using ufw:
   sudo ufw allow 22/tcp
   sudo ufw allow 80/tcp
   sudo ufw allow 443/tcp
   sudo ufw allow 6443/tcp
   sudo ufw enable
   ```

4. **Update System**
   ```bash
   apt update && apt upgrade -y
   ```

---

### Hostinger VPS

#### Recommended Plan
- **VPS 2 or higher**: 4GB RAM, 2 vCPUs
- **OS**: Ubuntu 22.04

#### Setup Steps

1. **Order VPS**
   - Go to Hostinger VPS plans
   - Select VPS 2 or higher
   - Choose Ubuntu 22.04 as OS
   - Complete purchase

2. **Access VPS**
   ```bash
   # Get credentials from Hostinger panel
   ssh root@your-vps-ip
   ```

3. **Configure Firewall**
   ```bash
   # Hostinger provides hPanel, but you can also use ufw
   sudo ufw allow 22/tcp
   sudo ufw allow 80/tcp
   sudo ufw allow 443/tcp
   sudo ufw allow 6443/tcp
   sudo ufw enable
   ```

4. **Update System**
   ```bash
   apt update && apt upgrade -y
   ```

---

### Linode

#### Recommended Linode
- **Plan**: Linode 4GB ($24/month)
- **OS**: Ubuntu 22.04 LTS
- **Region**: Choose closest to your users

#### Setup Steps

1. **Create Linode**
   ```bash
   # From Linode Cloud Manager:
   # - Click "Create" → "Linode"
   # - Choose Ubuntu 22.04
   # - Select Linode 4GB
   # - Add SSH key
   # - Create Linode
   ```

2. **Connect to Linode**
   ```bash
   ssh root@your-linode-ip
   ```

3. **Configure Firewall**
   ```bash
   # Use Linode Cloud Firewall or ufw
   sudo ufw allow 22/tcp
   sudo ufw allow 80/tcp
   sudo ufw allow 443/tcp
   sudo ufw allow 6443/tcp
   sudo ufw enable
   ```

4. **Update System**
   ```bash
   apt update && apt upgrade -y
   ```

---

### Vultr

#### Recommended Instance
- **Plan**: Cloud Compute - 4GB RAM / 2 vCPUs
- **OS**: Ubuntu 22.04 x64

#### Setup Steps

1. **Deploy Server**
   ```bash
   # From Vultr Console:
   # - Click "Deploy New Server"
   # - Choose Cloud Compute
   # - Select location
   # - Choose Ubuntu 22.04
   # - Select 4GB RAM plan
   # - Deploy
   ```

2. **Connect to Server**
   ```bash
   ssh root@your-vultr-ip
   ```

3. **Configure Firewall**
   ```bash
   sudo ufw allow 22/tcp
   sudo ufw allow 80/tcp
   sudo ufw allow 443/tcp
   sudo ufw allow 6443/tcp
   sudo ufw enable
   ```

4. **Update System**
   ```bash
   apt update && apt upgrade -y
   ```

---

## K3s Installation

After setting up your VPS, install K3s (lightweight Kubernetes).

### 1. Install K3s

```bash
# Install K3s with Traefik disabled (we'll use our own config)
curl -sfL https://get.k3s.io | sh -s - --write-kubeconfig-mode 644 --disable traefik

# Wait for K3s to be ready
sudo k3s kubectl get nodes
```

### 2. Install Traefik (Ingress Controller)

```bash
# Add Traefik Helm repository
sudo k3s kubectl apply -f https://raw.githubusercontent.com/traefik/traefik/v2.10/docs/content/reference/dynamic-configuration/kubernetes-crd-definition-v1.yml

# Install Traefik
sudo k3s kubectl apply -f https://raw.githubusercontent.com/traefik/traefik/v2.10/docs/content/reference/dynamic-configuration/kubernetes-crd-rbac.yml
```

Or use the built-in Traefik:

```bash
# Install K3s with Traefik enabled (default)
curl -sfL https://get.k3s.io | sh -s - --write-kubeconfig-mode 644
```

### 3. Install cert-manager (for TLS)

```bash
# Install cert-manager
sudo k3s kubectl apply -f https://github.com/cert-manager/cert-manager/releases/download/v1.13.0/cert-manager.yaml

# Wait for cert-manager to be ready
sudo k3s kubectl wait --for=condition=Ready pods --all -n cert-manager --timeout=300s
```

### 4. Configure kubectl Access

**On the server:**
```bash
# Copy kubeconfig
sudo cat /etc/rancher/k3s/k3s.yaml
```

**On your local machine:**
```bash
# Create .kube directory if it doesn't exist
mkdir -p ~/.kube

# Copy the content to your local kubeconfig
# Replace 127.0.0.1 with your server's public IP
nano ~/.kube/config

# Test connection
kubectl get nodes
```

---

## Application Deployment

### 1. Prepare Configuration Files

#### Update Domain Names

Edit the following files and replace `yourdomain.com` with your actual domain:

```bash
# Backend Ingress
nano infra/k3s/backend/ingress.yaml
# Change: api.yourdomain.com → api.youractual domain.com

# Frontend Ingress
nano infra/k3s/frontend/ingress.yaml
# Change: blog.yourdomain.com → blog.youractualdomain.com

# Cluster Issuer (for Let's Encrypt)
nano infra/k3s/base/cluster-issuer.yaml
# Change email address to your email

# Certificates
nano infra/k3s/base/certificates.yaml
# Update domain names
```

#### Update Backend ConfigMap

```bash
nano infra/k3s/backend/configmap.yaml
```

Update CORS origins:
```yaml
CORS_ORIGINS: '["https://blog.youractualdomain.com"]'
```

#### Update Frontend ConfigMap

```bash
nano infra/k3s/frontend/configmap.yaml
```

Update API URL:
```yaml
VITE_API_BASE_URL: "https://api.youractualdomain.com"
```

### 2. Create Kubernetes Secrets

```bash
# Create backend secrets
kubectl create secret generic backend-secrets \
  --from-literal=MONGODB_URL='mongodb+srv://user:pass@cluster.mongodb.net/blog_generation' \
  --from-literal=CHROMADB_HOST='your-chromadb-host.com' \
  --from-literal=CHROMADB_PORT='443' \
  --from-literal=GROQ_API_KEY='gsk_your_api_key' \
  --from-literal=JWT_SECRET_KEY="$(openssl rand -base64 32)" \
  --namespace=blog-backend
```

### 3. Deploy Application

#### Option A: Using Deployment Script (Recommended)

**Linux/Mac:**
```bash
cd infra/k3s
chmod +x deploy.sh
./deploy.sh
```

**Windows PowerShell:**
```powershell
cd infra\k3s
.\deploy.ps1
```

#### Option B: Manual Deployment

```bash
cd infra/k3s

# 1. Create namespaces
kubectl apply -f base/namespaces.yaml

# 2. Create ClusterIssuer
kubectl apply -f base/cluster-issuer.yaml

# 3. Deploy Backend
kubectl apply -f backend/configmap.yaml
kubectl apply -f backend/deployment.yaml
kubectl apply -f backend/service.yaml
kubectl apply -f backend/hpa.yaml
kubectl apply -f backend/middleware.yaml
kubectl apply -f backend/ingress.yaml

# 4. Deploy Frontend
kubectl apply -f frontend/configmap.yaml
kubectl apply -f frontend/deployment.yaml
kubectl apply -f frontend/service.yaml
kubectl apply -f frontend/hpa.yaml
kubectl apply -f frontend/middleware.yaml
kubectl apply -f frontend/ingress.yaml

# 5. Create TLS Certificates
kubectl apply -f base/certificates.yaml

# 6. Wait for deployments
kubectl rollout status deployment/backend -n blog-backend
kubectl rollout status deployment/frontend -n blog-frontend
```

### 4. Verify Deployment

```bash
# Check pods
kubectl get pods -n blog-backend
kubectl get pods -n blog-frontend

# Check services
kubectl get svc -n blog-backend
kubectl get svc -n blog-frontend

# Check ingress routes
kubectl get ingressroute -n blog-backend
kubectl get ingressroute -n blog-frontend

# Check certificates
kubectl get certificate -n blog-backend
kubectl get certificate -n blog-frontend

# Check certificate status
kubectl describe certificate backend-tls -n blog-backend
kubectl describe certificate frontend-tls -n blog-frontend
```

---

## Post-Deployment Configuration

### 1. DNS Configuration

Point your domain to your server's IP address:

**A Records:**
```
blog.yourdomain.com    → YOUR_SERVER_IP
api.yourdomain.com     → YOUR_SERVER_IP
```

**Or use a wildcard:**
```
*.yourdomain.com       → YOUR_SERVER_IP
```

### 2. Wait for TLS Certificates

```bash
# Monitor certificate issuance
kubectl get certificate --all-namespaces -w

# Check certificate details
kubectl describe certificate backend-tls -n blog-backend
kubectl describe certificate frontend-tls -n blog-frontend
```

Certificates should be ready in 1-5 minutes. Status should show `Ready: True`.

### 3. Test Application

```bash
# Test backend health
curl https://api.yourdomain.com/health

# Test backend API docs
# Visit: https://api.yourdomain.com/docs

# Test frontend
# Visit: https://blog.yourdomain.com
```

### 4. Create First User

1. Go to `https://blog.yourdomain.com/register`
2. Create an account
3. Login and start generating blogs!

---

## Monitoring & Maintenance

### View Logs

```bash
# Backend logs
kubectl logs -f deployment/backend -n blog-backend

# Frontend logs
kubectl logs -f deployment/frontend -n blog-frontend

# All pods in namespace
kubectl logs -f -l app=backend -n blog-backend
```

### Scale Deployments

```bash
# Manual scaling
kubectl scale deployment/backend --replicas=5 -n blog-backend
kubectl scale deployment/frontend --replicas=3 -n blog-frontend

# HPA will auto-scale based on CPU/Memory
kubectl get hpa -n blog-backend
kubectl get hpa -n blog-frontend
```

### Update Application

```bash
# Update backend image
kubectl set image deployment/backend backend=ghcr.io/yourusername/backend:latest -n blog-backend

# Update frontend image
kubectl set image deployment/frontend frontend=ghcr.io/yourusername/frontend:latest -n blog-frontend

# Or re-apply manifests
kubectl apply -f backend/deployment.yaml
kubectl apply -f frontend/deployment.yaml
```

### Backup MongoDB

```bash
# MongoDB Atlas has automatic backups
# Or use mongodump for manual backups
mongodump --uri="mongodb+srv://user:pass@cluster.mongodb.net/blog_generation" --out=./backup
```

---

## Troubleshooting

### Pods Not Starting

```bash
# Check pod status
kubectl get pods -n blog-backend
kubectl get pods -n blog-frontend

# Describe pod for events
kubectl describe pod <pod-name> -n blog-backend

# Check logs
kubectl logs <pod-name> -n blog-backend
```

**Common issues:**
- Missing secrets: Create backend-secrets
- Image pull errors: Check image name and registry
- Resource limits: Increase memory/CPU limits

### Certificate Not Issuing

```bash
# Check certificate status
kubectl describe certificate backend-tls -n blog-backend

# Check cert-manager logs
kubectl logs -n cert-manager deployment/cert-manager

# Check challenges
kubectl get challenges --all-namespaces
```

**Common issues:**
- DNS not propagated: Wait 5-10 minutes
- Port 80 blocked: Ensure port 80 is open for HTTP-01 challenge
- Rate limits: Let's Encrypt has rate limits (5 per week per domain)

### Application Not Accessible

```bash
# Check ingress
kubectl get ingressroute -n blog-backend
kubectl describe ingressroute backend-ingress -n blog-backend

# Check Traefik
kubectl get pods -n kube-system | grep traefik
kubectl logs -n kube-system <traefik-pod-name>
```

**Common issues:**
- DNS not pointing to server: Check DNS settings
- Firewall blocking ports: Ensure 80 and 443 are open
- Ingress misconfigured: Check domain names in ingress.yaml

### Database Connection Issues

```bash
# Check backend logs
kubectl logs deployment/backend -n blog-backend

# Test MongoDB connection
# Exec into pod
kubectl exec -it deployment/backend -n blog-backend -- /bin/bash
# Try connecting with mongo client
```

**Common issues:**
- Wrong MongoDB URL: Check secrets
- IP whitelist: Add server IP to MongoDB Atlas
- Network issues: Check firewall and security groups

### High Memory/CPU Usage

```bash
# Check resource usage
kubectl top pods -n blog-backend
kubectl top pods -n blog-frontend

# Check HPA status
kubectl get hpa -n blog-backend

# Increase resources if needed
# Edit deployment.yaml and increase limits
```

---

## Security Best Practices

1. **Change Default Secrets**
   - Generate strong JWT secret
   - Use strong MongoDB password
   - Rotate secrets regularly

2. **Firewall Configuration**
   - Only open necessary ports (22, 80, 443, 6443)
   - Restrict SSH to your IP
   - Use VPN for kubectl access

3. **Regular Updates**
   ```bash
   # Update system packages
   sudo apt update && sudo apt upgrade -y
   
   # Update K3s
   curl -sfL https://get.k3s.io | sh -
   ```

4. **Backup Strategy**
   - Enable MongoDB Atlas automatic backups
   - Backup Kubernetes manifests to Git
   - Export important data regularly

5. **Monitoring**
   - Set up monitoring (Prometheus/Grafana)
   - Configure alerts for downtime
   - Monitor resource usage

---

## Cost Optimization

### Recommended Configurations by Budget

**Budget: $10-15/month**
- DigitalOcean: Basic Droplet (2GB RAM)
- Reduce replicas: backend=1, frontend=1
- Disable HPA
- Use MongoDB Atlas free tier (M0)

**Budget: $20-30/month**
- DigitalOcean/Linode: 4GB RAM
- Current configuration (recommended)
- MongoDB Atlas M10 or free tier

**Budget: $50+/month**
- AWS t3.large or DigitalOcean 8GB
- Increase replicas for HA
- MongoDB Atlas M20+
- Add monitoring stack

---

## Additional Resources

- [K3s Documentation](https://docs.k3s.io/)
- [Traefik Documentation](https://doc.traefik.io/traefik/)
- [cert-manager Documentation](https://cert-manager.io/docs/)
- [MongoDB Atlas Documentation](https://docs.atlas.mongodb.com/)
- [GroqAI Documentation](https://console.groq.com/docs)

---

## Support

For issues or questions:
1. Check logs: `kubectl logs`
2. Review troubleshooting section
3. Check GitHub issues
4. Contact development team

---

**Last Updated**: January 2026  
**Version**: 2.0.0
