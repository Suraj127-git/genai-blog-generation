#!/bin/bash
# k3d Local Setup Script for Blog Generation Platform

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}Blog Generation Platform - k3d Setup${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to check k3d setup
check_k3d() {
    echo -e "${YELLOW}Checking k3d setup...${NC}"
    
    if ! command_exists k3d; then
        echo -e "${RED}❌ k3d is not installed${NC}"
        echo "Install k3d with: curl -s https://raw.githubusercontent.com/k3d-io/k3d/main/install.sh | bash"
        exit 1
    fi
    
    if ! kubectl cluster-info >/dev/null 2>&1; then
        echo -e "${RED}❌ Cannot connect to Kubernetes cluster${NC}"
        echo "Make sure k3d cluster is running:"
        echo "k3d cluster list"
        echo "k3d cluster start dev"
        exit 1
    else
        echo -e "${GREEN}✓ k3d cluster accessible${NC}"
        kubectl get nodes
        echo ""
    fi
}

# Function to build Docker images for k3d
build_images() {
    echo -e "${YELLOW}Building Docker images for k3d...${NC}"
    
    # Import images into k3d
    echo "Building and importing backend image..."
    cd backend
    docker build -t blog-backend:local -f ../infra/docker/backend.Dockerfile .
    k3d image import blog-backend:local -c dev
    
    echo "Building and importing frontend image..."
    cd ../frontend
    docker build -t blog-frontend:local -f ../infra/docker/frontend-simple.Dockerfile .
    k3d image import blog-frontend:local -c dev
    
    cd ..
    echo -e "${GREEN}✓ Docker images built and imported to k3d${NC}"
}

# Function to setup hosts file
setup_hosts() {
    echo -e "${YELLOW}Setting up local DNS...${NC}"
    
    # Get k3d server IP
    K3D_IP=$(docker inspect k3d-dev-serverlb 2>/dev/null | jq -r '.[0].NetworkSettings.Networks["k3d-dev"].IPAddress' || echo "127.0.0.1")
    
    if ! grep -q "blog.local.k3s" /etc/hosts; then
        echo -e "${BLUE}Adding entries to /etc/hosts (requires sudo)${NC}"
        echo "$K3D_IP blog.local.k3s api.local.k3s" | sudo tee -a /etc/hosts
        echo -e "${GREEN}✓ DNS entries added for IP: $K3D_IP${NC}"
    else
        echo -e "${GREEN}✓ DNS entries already exist${NC}"
    fi
}

# Function to create k3d cluster if needed
create_cluster() {
    echo -e "${YELLOW}Checking k3d cluster...${NC}"
    
    if k3d cluster list | grep -q "dev.*running"; then
        echo -e "${GREEN}✓ k3d cluster already running${NC}"
    elif k3d cluster list | grep -q "dev"; then
        echo -e "${YELLOW}Starting existing k3d cluster...${NC}"
        k3d cluster start dev
        echo -e "${GREEN}✓ k3d cluster started${NC}"
    else
        echo -e "${YELLOW}Creating k3d cluster...${NC}"
        k3d cluster create dev --port "8080:80@loadbalancer" --port "8000:8000@loadbalancer"
        echo -e "${GREEN}✓ k3d cluster created${NC}"
    fi
    
    # Wait for cluster to be ready
    echo "Waiting for cluster to be ready..."
    kubectl wait --for=condition=Ready nodes --all --timeout=300s
}

# Function to show next steps
show_next_steps() {
    echo -e "${BLUE}========================================${NC}"
    echo -e "${BLUE}k3d Setup Complete! Next Steps:${NC}"
    echo -e "${BLUE}========================================${NC}"
    echo ""
    echo -e "${YELLOW}1. Configure your cloud services:${NC}"
    echo "   - MongoDB Atlas: https://cloud.mongodb.com/"
    echo "   - GroqAI: https://console.groq.com/"
    echo "   - ChromaDB: https://www.trychroma.com/"
    echo ""
    echo -e "${YELLOW}2. Update Kubernetes secrets:${NC}"
    echo "   kubectl edit secret backend-secrets -n blog-backend"
    echo ""
    echo -e "${YELLOW}3. Deploy the application:${NC}"
    echo "   cd infra/k3s"
    echo "   ./deploy.sh"
    echo ""
    echo -e "${YELLOW}4. Access the application:${NC}"
    echo "   Frontend: http://blog.local.k3s"
    echo "   Backend API: http://api.local.k3s/docs"
    echo ""
    echo -e "${YELLOW}5. For detailed guide, see:${NC}"
    echo "   LOCAL_DEVELOPMENT.md"
    echo ""
    echo -e "${GREEN}Happy coding with k3d! 🚀${NC}"
}

# Main execution
main() {
    # Check if running from project root
    if [ ! -d "backend" ] || [ ! -d "frontend" ] || [ ! -d "infra" ]; then
        echo -e "${RED}Error: Please run this script from the project root directory${NC}"
        exit 1
    fi
    
    # Check prerequisites
    if ! command_exists docker; then
        echo -e "${RED}❌ Docker is not installed${NC}"
        echo "Please install Docker first: https://docs.docker.com/get-docker/"
        exit 1
    fi
    
    create_cluster
    check_k3d
    build_images
    setup_hosts
    show_next_steps
}

# Run main function
main
