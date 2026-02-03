#!/bin/bash
# K3s Deployment Script for Blog Generation Application

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}Blog Generation - K3s Deployment${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""

# Check if kubectl is installed
if ! command -v kubectl &> /dev/null; then
    echo -e "${RED}Error: kubectl is not installed${NC}"
    exit 1
fi

# Check if cluster is accessible
if ! kubectl cluster-info &> /dev/null; then
    echo -e "${RED}Error: Cannot connect to Kubernetes cluster${NC}"
    exit 1
fi

echo -e "${YELLOW}Step 1: Creating Namespaces${NC}"
kubectl apply -f base/namespaces.yaml
echo -e "${GREEN}✓ Namespaces created${NC}"
echo ""

echo -e "${YELLOW}Step 2: Checking cert-manager${NC}"
if ! kubectl get namespace cert-manager &> /dev/null; then
    echo -e "${YELLOW}Installing cert-manager...${NC}"
    kubectl apply -f https://github.com/cert-manager/cert-manager/releases/download/v1.13.0/cert-manager.yaml
    echo "Waiting for cert-manager to be ready..."
    kubectl wait --for=condition=Ready pods --all -n cert-manager --timeout=300s
    echo -e "${GREEN}✓ cert-manager installed${NC}"
else
    echo -e "${GREEN}✓ cert-manager already installed${NC}"
fi
echo ""

echo -e "${YELLOW}Step 3: Creating ClusterIssuer${NC}"
kubectl apply -f base/cluster-issuer.yaml
echo -e "${GREEN}✓ ClusterIssuer created${NC}"
echo ""

echo -e "${YELLOW}Step 4: Checking Backend Secrets${NC}"
if kubectl get secret backend-secrets -n blog-backend &> /dev/null; then
    echo -e "${GREEN}✓ Backend secrets already exist${NC}"
else
    echo -e "${RED}⚠ Backend secrets not found!${NC}"
    echo -e "${YELLOW}Please create secrets first:${NC}"
    echo "  kubectl create secret generic backend-secrets \\"
    echo "    --from-literal=MONGODB_URL='mongodb+srv://...' \\"
    echo "    --from-literal=CHROMADB_HOST='your-host' \\"
    echo "    --from-literal=GROQ_API_KEY='gsk_...' \\"
    echo "    --from-literal=JWT_SECRET_KEY='\$(openssl rand -base64 32)' \\"
    echo "    --namespace=blog-backend"
    echo ""
    read -p "Continue anyway? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi
echo ""

echo -e "${YELLOW}Step 5: Deploying Backend${NC}"
kubectl apply -f backend/configmap.yaml
kubectl apply -f backend/deployment.yaml
kubectl apply -f backend/service.yaml
kubectl apply -f backend/hpa.yaml
kubectl apply -f backend/middleware.yaml
kubectl apply -f backend/ingress.yaml
echo -e "${GREEN}✓ Backend deployed${NC}"
echo ""

echo -e "${YELLOW}Step 6: Deploying Frontend${NC}"
kubectl apply -f frontend/configmap.yaml
kubectl apply -f frontend/deployment.yaml
kubectl apply -f frontend/service.yaml
kubectl apply -f frontend/hpa.yaml
kubectl apply -f frontend/middleware.yaml
kubectl apply -f frontend/ingress.yaml
echo -e "${GREEN}✓ Frontend deployed${NC}"
echo ""

echo -e "${YELLOW}Step 7: Creating TLS Certificates${NC}"
kubectl apply -f base/certificates.yaml
echo -e "${GREEN}✓ Certificate requests created${NC}"
echo ""

echo -e "${YELLOW}Step 8: Waiting for Deployments${NC}"
echo "Waiting for backend..."
kubectl rollout status deployment/backend -n blog-backend --timeout=300s
echo "Waiting for frontend..."
kubectl rollout status deployment/frontend -n blog-frontend --timeout=300s
echo -e "${GREEN}✓ All deployments ready${NC}"
echo ""

echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}Deployment Complete!${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""

echo -e "${YELLOW}Deployment Status:${NC}"
echo ""
echo "Backend:"
kubectl get pods -n blog-backend
echo ""
echo "Frontend:"
kubectl get pods -n blog-frontend
echo ""

echo -e "${YELLOW}Services:${NC}"
kubectl get svc -n blog-backend
kubectl get svc -n blog-frontend
echo ""

echo -e "${YELLOW}Ingress Routes:${NC}"
kubectl get ingressroute -n blog-backend
kubectl get ingressroute -n blog-frontend
echo ""

echo -e "${YELLOW}TLS Certificates:${NC}"
kubectl get certificate -n blog-backend
kubectl get certificate -n blog-frontend
echo ""

echo -e "${GREEN}Next Steps:${NC}"
echo "1. Point your DNS to the cluster IP"
echo "2. Wait for TLS certificates to be issued (check with: kubectl get certificate --all-namespaces)"
echo "3. Access your application:"
echo "   - Frontend: https://blog.yourdomain.com"
echo "   - Backend API: https://api.yourdomain.com/docs"
echo ""
echo -e "${GREEN}Done!${NC}"
