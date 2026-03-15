#!/bin/bash

# Production Server Deployment Script
# This script deploys the application to a production Kubernetes cluster

set -e

echo "🚀 Deploying to production server..."

# Check if we're in the right context
kubectl config current-context

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
kubectl wait --for=condition=available --timeout=600s deployment/backend -n blog-backend
kubectl wait --for=condition=available --timeout=600s deployment/frontend -n blog-frontend

# Show status
echo "📊 Deployment status:"
kubectl get pods -n blog-backend
kubectl get pods -n blog-frontend

echo "✅ Production deployment complete!"
echo "🌐 Frontend: https://yourdomain.com"
echo "🔌 Backend API: https://api.yourdomain.com/docs"
echo ""
echo "⚠️  Remember to:"
echo "   - Update yourdomain.com to your actual domain"
echo "   - Configure TLS certificates"
echo "   - Set up proper secrets and environment variables"
