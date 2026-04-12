#!/bin/bash
# Verification script for local K3s setup

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}Verifying Local Setup${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to check Kubernetes connection
check_kubernetes() {
    echo -e "${YELLOW}Checking Kubernetes connection...${NC}"
    
    if ! kubectl cluster-info >/dev/null 2>&1; then
        echo -e "${RED}❌ Cannot connect to Kubernetes cluster${NC}"
        return 1
    else
        echo -e "${GREEN}✓ Kubernetes cluster accessible${NC}"
        kubectl cluster-info | head -3
        echo ""
        return 0
    fi
}

# Function to check namespaces
check_namespaces() {
    echo -e "${YELLOW}Checking namespaces...${NC}"
    
    if kubectl get namespace blog-backend >/dev/null 2>&1; then
        echo -e "${GREEN}✓ blog-backend namespace exists${NC}"
    else
        echo -e "${RED}❌ blog-backend namespace not found${NC}"
        return 1
    fi
    
    if kubectl get namespace blog-frontend >/dev/null 2>&1; then
        echo -e "${GREEN}✓ blog-frontend namespace exists${NC}"
    else
        echo -e "${RED}❌ blog-frontend namespace not found${NC}"
        return 1
    fi
    
    echo ""
}

# Function to check deployments
check_deployments() {
    echo -e "${YELLOW}Checking deployments...${NC}"
    
    # Check backend
    if kubectl get deployment backend -n blog-backend >/dev/null 2>&1; then
        echo -e "${GREEN}✓ Backend deployment exists${NC}"
        
        # Check replica status
        backend_ready=$(kubectl get deployment backend -n blog-backend -o jsonpath='{.status.readyReplicas}' 2>/dev/null || echo "0")
        backend_desired=$(kubectl get deployment backend -n blog-backend -o jsonpath='{.spec.replicas}' 2>/dev/null || echo "1")
        
        if [ "$backend_ready" = "$backend_desired" ] && [ "$backend_ready" != "0" ]; then
            echo -e "${GREEN}✓ Backend deployment ready ($backend_ready/$backend_desired replicas)${NC}"
        else
            echo -e "${YELLOW}⚠ Backend deployment not ready ($backend_ready/$backend_desired replicas)${NC}"
        fi
    else
        echo -e "${RED}❌ Backend deployment not found${NC}"
    fi
    
    # Check frontend
    if kubectl get deployment frontend -n blog-frontend >/dev/null 2>&1; then
        echo -e "${GREEN}✓ Frontend deployment exists${NC}"
        
        # Check replica status
        frontend_ready=$(kubectl get deployment frontend -n blog-frontend -o jsonpath='{.status.readyReplicas}' 2>/dev/null || echo "0")
        frontend_desired=$(kubectl get deployment frontend -n blog-frontend -o jsonpath='{.spec.replicas}' 2>/dev/null || echo "1")
        
        if [ "$frontend_ready" = "$frontend_desired" ] && [ "$frontend_ready" != "0" ]; then
            echo -e "${GREEN}✓ Frontend deployment ready ($frontend_ready/$frontend_desired replicas)${NC}"
        else
            echo -e "${YELLOW}⚠ Frontend deployment not ready ($frontend_ready/$frontend_desired replicas)${NC}"
        fi
    else
        echo -e "${RED}❌ Frontend deployment not found${NC}"
    fi
    
    echo ""
}

# Function to check pods
check_pods() {
    echo -e "${YELLOW}Checking pods...${NC}"
    
    echo "Backend pods:"
    kubectl get pods -n blog-backend -o custom-columns=NAME:.metadata.name,STATUS:.status.phase,READY:.status.containerStatuses[0].ready 2>/dev/null || echo "No pods found"
    
    echo ""
    echo "Frontend pods:"
    kubectl get pods -n blog-frontend -o custom-columns=NAME:.metadata.name,STATUS:.status.phase,READY:.status.containerStatuses[0].ready 2>/dev/null || echo "No pods found"
    
    echo ""
}

# Function to check services
check_services() {
    echo -e "${YELLOW}Checking services...${NC}"
    
    if kubectl get service backend -n blog-backend >/dev/null 2>&1; then
        echo -e "${GREEN}✓ Backend service exists${NC}"
        backend_port=$(kubectl get service backend -n blog-backend -o jsonpath='{.spec.ports[0].port}')
        echo "   Port: $backend_port"
    else
        echo -e "${RED}❌ Backend service not found${NC}"
    fi
    
    if kubectl get service frontend -n blog-frontend >/dev/null 2>&1; then
        echo -e "${GREEN}✓ Frontend service exists${NC}"
        frontend_port=$(kubectl get service frontend -n blog-frontend -o jsonpath='{.spec.ports[0].port}')
        echo "   Port: $frontend_port"
    else
        echo -e "${RED}❌ Frontend service not found${NC}"
    fi
    
    echo ""
}

# Function to check ingress
check_ingress() {
    echo -e "${YELLOW}Checking ingress routes...${NC}"
    
    if kubectl get ingressroute backend-http -n blog-backend >/dev/null 2>&1; then
        echo -e "${GREEN}✓ Backend ingress route exists${NC}"
        backend_host=$(kubectl get ingressroute backend-http -n blog-backend -o jsonpath='{.spec.routes[0].match}' | grep -o 'Host([^)]*)' | sed 's/Host(\([^)]*\))/\1/')
        echo "   Host: $backend_host"
    else
        echo -e "${RED}❌ Backend ingress route not found${NC}"
    fi
    
    if kubectl get ingressroute frontend-http -n blog-frontend >/dev/null 2>&1; then
        echo -e "${GREEN}✓ Frontend ingress route exists${NC}"
        frontend_host=$(kubectl get ingressroute frontend-http -n blog-frontend -o jsonpath='{.spec.routes[0].match}' | grep -o 'Host([^)]*)' | sed 's/Host(\([^)]*\))/\1/')
        echo "   Host: $frontend_host"
    else
        echo -e "${RED}❌ Frontend ingress route not found${NC}"
    fi
    
    echo ""
}

# Function to check secrets
check_secrets() {
    echo -e "${YELLOW}Checking secrets...${NC}"
    
    if kubectl get secret backend-secrets -n blog-backend >/dev/null 2>&1; then
        echo -e "${GREEN}✓ Backend secrets exist${NC}"
        echo -e "${YELLOW}⚠ Make sure to update with actual values${NC}"
    else
        echo -e "${RED}❌ Backend secrets not found${NC}"
    fi
    
    echo ""
}

# Function to check Docker images
check_images() {
    echo -e "${YELLOW}Checking Docker images...${NC}"
    
    if docker images | grep -q "blog-backend.*local"; then
        echo -e "${GREEN}✓ blog-backend:local image exists${NC}"
    else
        echo -e "${RED}❌ blog-backend:local image not found${NC}"
        echo "   Run: cd backend && docker build -t blog-backend:local -f ../infra/docker/backend.Dockerfile ."
    fi
    
    if docker images | grep -q "blog-frontend.*local"; then
        echo -e "${GREEN}✓ blog-frontend:local image exists${NC}"
    else
        echo -e "${RED}❌ blog-frontend:local image not found${NC}"
        echo "   Run: cd frontend && docker build -t blog-frontend:local -f ../infra/docker/frontend.Dockerfile ."
    fi
    
    echo ""
}

# Function to test connectivity
test_connectivity() {
    echo -e "${YELLOW}Testing connectivity...${NC}"
    
    # Test backend health endpoint
    echo "Testing backend health endpoint..."
    if curl -s -f http://api.local.k3s/api/health > /dev/null 2>&1; then
        echo -e "${GREEN}✓ Backend health endpoint accessible${NC}"
    else
        echo -e "${YELLOW}⚠ Backend health endpoint not accessible${NC}"
        echo "   Make sure DNS is configured and pods are running"
        echo "   Try: kubectl port-forward svc/backend 8000:8000 -n blog-backend"
    fi
    
    # Test frontend
    echo "Testing frontend..."
    if curl -s -o /dev/null -w "%{http_code}" http://blog.local.k3s 2>/dev/null | grep -q "200\|404"; then
        echo -e "${GREEN}✓ Frontend responding${NC}"
    else
        echo -e "${YELLOW}⚠ Frontend not accessible${NC}"
        echo "   Make sure DNS is configured and pods are running"
    fi
    
    echo ""
}

# Function to show summary
show_summary() {
    echo -e "${BLUE}========================================${NC}"
    echo -e "${BLUE}Setup Verification Summary${NC}"
    echo -e "${BLUE}========================================${NC}"
    echo ""
    echo -e "${GREEN}If everything looks good, you can access:${NC}"
    echo "Frontend: http://blog.local.k3s"
    echo "Backend:  http://api.local.k3s/docs"
    echo ""
    echo -e "${YELLOW}If there are issues, check:${NC}"
    echo "1. Pod logs: kubectl logs -f deployment/backend -n blog-backend"
    echo "2. Events: kubectl get events -n blog-backend --sort-by='.lastTimestamp'"
    echo "3. Secrets: kubectl edit secret backend-secrets -n blog-backend"
    echo ""
    echo -e "${BLUE}For detailed troubleshooting, see LOCAL_DEVELOPMENT.md${NC}"
}

# Main execution
main() {
    # Check if running from project root
    if [ ! -d "backend" ] || [ ! -d "frontend" ] || [ ! -d "infra" ]; then
        echo -e "${RED}Error: Please run this script from the project root directory${NC}"
        exit 1
    fi
    
    check_kubernetes || exit 1
    check_namespaces || exit 1
    check_images
    check_secrets
    check_deployments
    check_pods
    check_services
    check_ingress
    test_connectivity
    show_summary
}

# Run main function
main
