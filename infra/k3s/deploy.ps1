# K3s Deployment Script for Blog Generation Application (Windows PowerShell)
# Usage: .\deploy.ps1

$ErrorActionPreference = "Stop"

# Colors for output
function Write-ColorOutput($ForegroundColor) {
    $fc = $host.UI.RawUI.ForegroundColor
    $host.UI.RawUI.ForegroundColor = $ForegroundColor
    if ($args) {
        Write-Output $args
    }
    $host.UI.RawUI.ForegroundColor = $fc
}

Write-ColorOutput Green "========================================"
Write-ColorOutput Green "Blog Generation - K3s Deployment"
Write-ColorOutput Green "========================================"
Write-Output ""

# Check if kubectl is installed
try {
    kubectl version --client | Out-Null
} catch {
    Write-ColorOutput Red "Error: kubectl is not installed"
    exit 1
}

# Check if cluster is accessible
try {
    kubectl cluster-info | Out-Null
} catch {
    Write-ColorOutput Red "Error: Cannot connect to Kubernetes cluster"
    exit 1
}

Write-ColorOutput Yellow "Step 1: Creating Namespaces"
kubectl apply -f base/namespaces.yaml
Write-ColorOutput Green "✓ Namespaces created"
Write-Output ""

Write-ColorOutput Yellow "Step 2: Checking cert-manager"
try {
    kubectl get namespace cert-manager 2>$null | Out-Null
    Write-ColorOutput Green "✓ cert-manager already installed"
} catch {
    Write-ColorOutput Yellow "Installing cert-manager..."
    kubectl apply -f https://github.com/cert-manager/cert-manager/releases/download/v1.13.0/cert-manager.yaml
    Write-Output "Waiting for cert-manager to be ready..."
    kubectl wait --for=condition=Ready pods --all -n cert-manager --timeout=300s
    Write-ColorOutput Green "✓ cert-manager installed"
}
Write-Output ""

Write-ColorOutput Yellow "Step 3: Creating ClusterIssuer"
kubectl apply -f base/cluster-issuer.yaml
Write-ColorOutput Green "✓ ClusterIssuer created"
Write-Output ""

Write-ColorOutput Yellow "Step 4: Checking Backend Secrets"
try {
    kubectl get secret backend-secrets -n blog-backend 2>$null | Out-Null
    Write-ColorOutput Green "✓ Backend secrets already exist"
} catch {
    Write-ColorOutput Red "⚠ Backend secrets not found!"
    Write-ColorOutput Yellow "Please create secrets first:"
    Write-Output "  kubectl create secret generic backend-secrets \"
    Write-Output "    --from-literal=MONGODB_URL='mongodb+srv://...' \"
    Write-Output "    --from-literal=CHROMADB_HOST='your-host' \"
    Write-Output "    --from-literal=GROQ_API_KEY='gsk_...' \"
    Write-Output "    --from-literal=JWT_SECRET_KEY='<random-secret>' \"
    Write-Output "    --namespace=blog-backend"
    Write-Output ""
    $continue = Read-Host "Continue anyway? (y/n)"
    if ($continue -ne 'y' -and $continue -ne 'Y') {
        exit 1
    }
}
Write-Output ""

Write-ColorOutput Yellow "Step 5: Deploying Backend"
kubectl apply -f backend/configmap.yaml
kubectl apply -f backend/deployment.yaml
kubectl apply -f backend/service.yaml
kubectl apply -f backend/hpa.yaml
kubectl apply -f backend/middleware.yaml
kubectl apply -f backend/ingress.yaml
Write-ColorOutput Green "✓ Backend deployed"
Write-Output ""

Write-ColorOutput Yellow "Step 6: Deploying Frontend"
kubectl apply -f frontend/configmap.yaml
kubectl apply -f frontend/deployment.yaml
kubectl apply -f frontend/service.yaml
kubectl apply -f frontend/hpa.yaml
kubectl apply -f frontend/middleware.yaml
kubectl apply -f frontend/ingress.yaml
Write-ColorOutput Green "✓ Frontend deployed"
Write-Output ""

Write-ColorOutput Yellow "Step 7: Creating TLS Certificates"
kubectl apply -f base/certificates.yaml
Write-ColorOutput Green "✓ Certificate requests created"
Write-Output ""

Write-ColorOutput Yellow "Step 8: Waiting for Deployments"
Write-Output "Waiting for backend..."
kubectl rollout status deployment/backend -n blog-backend --timeout=300s
Write-Output "Waiting for frontend..."
kubectl rollout status deployment/frontend -n blog-frontend --timeout=300s
Write-ColorOutput Green "✓ All deployments ready"
Write-Output ""

Write-ColorOutput Green "========================================"
Write-ColorOutput Green "Deployment Complete!"
Write-ColorOutput Green "========================================"
Write-Output ""

Write-ColorOutput Yellow "Deployment Status:"
Write-Output ""
Write-Output "Backend:"
kubectl get pods -n blog-backend
Write-Output ""
Write-Output "Frontend:"
kubectl get pods -n blog-frontend
Write-Output ""

Write-ColorOutput Yellow "Services:"
kubectl get svc -n blog-backend
kubectl get svc -n blog-frontend
Write-Output ""

Write-ColorOutput Yellow "Ingress Routes:"
kubectl get ingressroute -n blog-backend
kubectl get ingressroute -n blog-frontend
Write-Output ""

Write-ColorOutput Yellow "TLS Certificates:"
kubectl get certificate -n blog-backend
kubectl get certificate -n blog-frontend
Write-Output ""

Write-ColorOutput Green "Next Steps:"
Write-Output "1. Point your DNS to the cluster IP"
Write-Output "2. Wait for TLS certificates to be issued (check with: kubectl get certificate --all-namespaces)"
Write-Output "3. Access your application:"
Write-Output "   - Frontend: https://blog.yourdomain.com"
Write-Output "   - Backend API: https://api.yourdomain.com/docs"
Write-Output ""
Write-ColorOutput Green "Done!"
