#!/bin/bash

# Local K3s Deployment Script
# This script deploys the application to a local k3d cluster

set -e

echo "🚀 Deploying to local K3s cluster..."

# Apply namespaces
echo "📦 Applying namespaces..."
kubectl apply -f namespaces.yaml

# Deploy backend
echo "🔧 Deploying backend..."
kubectl apply -f backend/

# Deploy frontend
echo "🎨 Deploying frontend..."
kubectl apply -f frontend/

# Wait for deployments to be ready
echo "⏳ Waiting for deployments to be ready..."
kubectl wait --for=condition=available --timeout=300s deployment/backend -n blog-backend
kubectl wait --for=condition=available --timeout=300s deployment/frontend -n blog-frontend

# Show status
echo "📊 Deployment status:"
kubectl get pods -n blog-backend
kubectl get pods -n blog-frontend

echo "✅ Local deployment complete!"
echo "🌐 Frontend: http://blog.local.k3s"
echo "🔌 Backend API: http://api.local.k3s/docs"
