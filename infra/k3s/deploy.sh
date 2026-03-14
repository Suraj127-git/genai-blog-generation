#!/bin/bash
# k3d Deployment Script for Blog Generation Application

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}Blog Generation - k3d Deployment${NC}"
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
    echo -e "${YELLOW}Please start k3d cluster first: k3d cluster start dev${NC}"
    exit 1
fi

echo -e "${YELLOW}Step 1: Creating Namespaces${NC}"
kubectl apply -f namespaces.yaml
echo -e "${GREEN}✓ Namespaces created${NC}"
echo ""

echo -e "${YELLOW}Step 2: Creating Local Secrets${NC}"
if kubectl get secret backend-secrets -n blog-backend &> /dev/null; then
    echo -e "${GREEN}✓ Backend secrets already exist${NC}"
else
    echo -e "${YELLOW}Creating backend secrets with local defaults...${NC}"
    kubectl create secret generic backend-secrets \
        --from-literal=MONGODB_URL='mongodb://host.k3d.internal:27017' \
        --from-literal=CHROMADB_HOST='localhost' \
        --from-literal=GROQ_API_KEY='gsk_your-groq-api-key-here' \
        --from-literal=JWT_SECRET_KEY='local-development-secret-key-change-this' \
        --namespace=blog-backend
    echo -e "${GREEN}✓ Backend secrets created${NC}"
    echo -e "${RED}⚠ Please update the secrets with your actual values!${NC}"
fi
echo ""

echo -e "${YELLOW}Step 3: Deploying Backend${NC}"
kubectl apply -f backend/configmap.yaml
kubectl apply -f backend/deployment.yaml
kubectl apply -f backend/service.yaml
# Skip HPA for local development
kubectl apply -f backend/middleware.yaml
kubectl apply -f backend/ingress.yaml
echo -e "${GREEN}✓ Backend deployed${NC}"
echo ""

echo -e "${YELLOW}Step 4: Deploying Frontend${NC}"
kubectl apply -f frontend/configmap.yaml
kubectl apply -f frontend/deployment.yaml
kubectl apply -f frontend/service.yaml
# Skip HPA for local development
kubectl apply -f frontend/middleware.yaml
kubectl apply -f frontend/ingress.yaml
echo -e "${GREEN}✓ Frontend deployed${NC}"
echo ""

echo -e "${YELLOW}Step 5: Waiting for Deployments${NC}"
echo "Waiting for backend..."
kubectl rollout status deployment/backend -n blog-backend --timeout=300s
echo "Waiting for frontend..."
kubectl rollout status deployment/frontend -n blog-frontend --timeout=300s
echo -e "${GREEN}✓ All deployments ready${NC}"
echo ""

echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}k3d Deployment Complete!${NC}"
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

echo -e "${BLUE}Local Access URLs:${NC}"
echo "1. Add these entries to your /etc/hosts file:"
echo "   127.0.0.1 blog.local.k3s api.local.k3s"
echo ""
echo "2. Access the application:"
echo "   - Frontend: http://blog.local.k3s"
echo "   - Backend API: http://api.local.k3s/docs"
echo ""

echo -e "${BLUE}Build Local Images:${NC}"
echo "To build and use local images, run:"
echo "  cd backend && docker build -t blog-backend:local ."
echo "  cd frontend && docker build -t blog-frontend:local ."
echo "  # If using Minikube: eval \$(minikube docker-env) before building"
echo ""

echo -e "${BLUE}Update Secrets:${NC}"
echo "Don't forget to update the backend secrets:"
echo "  kubectl edit secret backend-secrets -n blog-backend"
echo ""

echo -e "${GREEN}Done!${NC}"
