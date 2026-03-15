#!/bin/bash
# k3s Deployment Script for Blog Generation Application

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}Blog Generation - K8s Deployment${NC}"
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
    echo -e "${YELLOW}Please start your Kubernetes cluster first${NC}"
    exit 1
fi

# Ask user which environment to deploy to
echo -e "${YELLOW}Select deployment environment:${NC}"
echo "1) Local (k3d/localhost)"
echo "2) Production Server"
echo ""
read -p "Enter your choice (1 or 2): " choice

case $choice in
    1)
        echo -e "${GREEN}Deploying to LOCAL environment...${NC}"
        ./local/deploy-local.sh
        ;;
    2)
        echo -e "${GREEN}Deploying to PRODUCTION environment...${NC}"
        ./server/deploy-server.sh
        ;;
    *)
        echo -e "${RED}Invalid choice. Exiting.${NC}"
        exit 1
        ;;
esac
