#!/bin/bash
# k3d Teardown Script for Blog Generation Platform
# This script removes all resources from the k3d cluster

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${RED}========================================${NC}"
echo -e "${RED}Blog Generation Platform - k3d Teardown${NC}"
echo -e "${RED}========================================${NC}"
echo ""

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to remove DNS entries
remove_dns() {
    echo -e "${YELLOW}Removing DNS entries from /etc/hosts...${NC}"
    
    # Check if running with sudo
    if [ "$EUID" -ne 0 ]; then
        echo -e "${YELLOW}Note: You may need to enter your password to edit /etc/hosts${NC}"
    fi
    
    # Remove entries if they exist
    if grep -q "blog.local.k3s\|api.local.k3s" /etc/hosts; then
        sudo sed -i '' '/blog\.local\.k3s/d' /etc/hosts 2>/dev/null || \
        sed -i '' '/blog\.local\.k3s/d' /etc/hosts 2>/dev/null || true
        
        sudo sed -i '' '/api\.local\.k3s/d' /etc/hosts 2>/dev/null || \
        sed -i '' '/api\.local\.k3s/d' /etc/hosts 2>/dev/null || true
        
        echo -e "${GREEN}✓ DNS entries removed${NC}"
    else
        echo -e "${YELLOW}⚠ No DNS entries found${NC}"
    fi
}

# Function to delete Kubernetes resources
delete_k8s_resources() {
    echo -e "${YELLOW}Removing Kubernetes resources...${NC}"
    
    # Delete namespaces (this will cascade delete all resources in them)
    kubectl delete namespace blog-backend --ignore-not-found=true || true
    kubectl delete namespace blog-frontend --ignore-not-found=true || true
    
    # Wait for namespaces to be fully deleted
    echo "Waiting for namespaces to be deleted..."
    kubectl wait --for=delete namespace/blog-backend --timeout=60s || true
    kubectl wait --for=delete namespace/blog-frontend --timeout=60s || true
    
    echo -e "${GREEN}✓ Kubernetes resources removed${NC}"
}

# Function to delete Docker images
delete_docker_images() {
    echo -e "${YELLOW}Removing Docker images...${NC}"
    
    # Remove local images
    docker rmi blog-backend:local 2>/dev/null || true
    docker rmi blog-frontend:local 2>/dev/null || true
    
    echo -e "${GREEN}✓ Docker images removed${NC}"
}

# Function to stop and delete k3d cluster
delete_k3d_cluster() {
    echo -e "${YELLOW}Removing k3d cluster...${NC}"
    
    if k3d cluster list | grep -q "dev"; then
        k3d cluster delete dev
        echo -e "${GREEN}✓ k3d cluster 'dev' deleted${NC}"
    else
        echo -e "${YELLOW}⚠ k3d cluster 'dev' not found${NC}"
    fi
}

# Function to clean up any remaining resources
cleanup_remaining() {
    echo -e "${YELLOW}Cleaning up remaining resources...${NC}"
    
    # Remove any lingering Docker containers
    docker ps -a | grep -E "blog-backend|blog-frontend" | awk '{print $1}' | xargs -r docker rm -f 2>/dev/null || true
    
    # Clean up Docker networks if any
    docker network ls | grep -E "blog-" | awk '{print $1}' | xargs -r docker network rm 2>/dev/null || true
    
    echo -e "${GREEN}✓ Cleanup completed${NC}"
}

# Function to verify cleanup
verify_cleanup() {
    echo -e "${YELLOW}Verifying cleanup...${NC}"
    
    # Check if namespaces are gone
    if kubectl get namespace | grep -q "blog-backend\|blog-frontend"; then
        echo -e "${RED}⚠ Some namespaces still exist${NC}"
    else
        echo -e "${GREEN}✓ All namespaces removed${NC}"
    fi
    
    # Check if cluster is gone
    if k3d cluster list | grep -q "dev"; then
        echo -e "${RED}⚠ k3d cluster still exists${NC}"
    else
        echo -e "${GREEN}✓ k3d cluster removed${NC}"
    fi
    
    # Check if DNS entries are gone
    if grep -q "blog.local.k3s\|api.local.k3s" /etc/hosts; then
        echo -e "${RED}⚠ DNS entries still exist${NC}"
    else
        echo -e "${GREEN}✓ DNS entries removed${NC}"
    fi
}

# Main execution
main() {
    # Check prerequisites
    if ! command_exists kubectl; then
        echo -e "${RED}Error: kubectl is not installed${NC}"
        exit 1
    fi
    
    if ! command_exists k3d; then
        echo -e "${RED}Error: k3d is not installed${NC}"
        exit 1
    fi
    
    if ! command_exists docker; then
        echo -e "${RED}Error: docker is not installed${NC}"
        exit 1
    fi
    
    # Confirm deletion
    echo -e "${RED}WARNING: This will completely remove the Blog Generation Platform from your k3d cluster.${NC}"
    echo -e "${RED}This includes:${NC}"
    echo "  - All Kubernetes resources (pods, services, ingress, etc.)"
    echo "  - All namespaces"
    echo "  - Docker images"
    echo "  - k3d cluster 'dev'"
    echo "  - DNS entries from /etc/hosts"
    echo ""
    read -p "Are you sure you want to continue? (y/N): " -n 1 -r
    echo ""
    
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo -e "${YELLOW}Teardown cancelled${NC}"
        exit 0
    fi
    
    # Execute teardown steps
    delete_k8s_resources
    delete_docker_images
    remove_dns
    delete_k3d_cluster
    cleanup_remaining
    verify_cleanup
    
    echo ""
    echo -e "${GREEN}========================================${NC}"
    echo -e "${GREEN}Teardown Complete!${NC}"
    echo -e "${GREEN}========================================${NC}"
    echo ""
    echo -e "${GREEN}All resources have been removed from your system.${NC}"
    echo ""
    echo "To set up the platform again, run:"
    echo -e "${BLUE}./setup-local-k3d.sh${NC}"
}

# Run main function
main "$@"
