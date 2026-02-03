# GitHub Actions Secrets Setup Guide

This guide explains how to configure all required secrets for the CI/CD pipeline.

## Required Secrets

### 1. GitHub Container Registry (GHCR)
**No setup needed** - `GITHUB_TOKEN` is automatically provided by GitHub Actions.

### 2. Kubernetes Configuration

#### `KUBE_CONFIG_STAGING`
Base64 encoded kubeconfig for staging cluster.

```bash
# Get kubeconfig from your K3s cluster
# On K3s server:
cat /etc/rancher/k3s/k3s.yaml

# Or if using kubectl locally:
cat ~/.kube/config

# Base64 encode it
cat ~/.kube/config | base64 -w 0

# Add to GitHub:
# Repository → Settings → Secrets → Actions → New repository secret
# Name: KUBE_CONFIG_STAGING
# Value: <paste base64 encoded config>
```

#### `KUBE_CONFIG_PRODUCTION`
Same as above but for production cluster.

```bash
cat ~/.kube/config-prod | base64 -w 0

# Add to GitHub as KUBE_CONFIG_PRODUCTION
```

### 3. Slack Notifications

#### `SLACK_WEBHOOK_URL`
Webhook URL for Slack notifications.

```bash
# Create Slack App:
# 1. Go to https://api.slack.com/apps
# 2. Create New App → From scratch
# 3. Add "Incoming Webhooks" feature
# 4. Activate incoming webhooks
# 5. Add New Webhook to Workspace
# 6. Copy Webhook URL

# Add to GitHub:
# Name: SLACK_WEBHOOK_URL
# Value: https://hooks.slack.com/services/YOUR/WEBHOOK/URL
```

### 4. Discord Notifications

#### `DISCORD_WEBHOOK`
Webhook URL for Discord notifications.

```bash
# Create Discord Webhook:
# 1. Go to your Discord server
# 2. Server Settings → Integrations → Webhooks
# 3. New Webhook
# 4. Copy Webhook URL

# Add to GitHub:
# Name: DISCORD_WEBHOOK
# Value: https://discord.com/api/webhooks/YOUR_WEBHOOK
```

### 5. Security Scanning

#### `SNYK_TOKEN`
Snyk API token for security scanning.

```bash
# Get Snyk token:
# 1. Sign up at https://snyk.io
# 2. Account Settings → General → Auth Token
# 3. Copy token

# Add to GitHub:
# Name: SNYK_TOKEN
# Value: <your-snyk-token>
```

### 6. Code Coverage (Optional)

#### `CODECOV_TOKEN`
Token for uploading coverage reports to Codecov.

```bash
# Get Codecov token:
# 1. Sign up at https://codecov.io
# 2. Add your repository
# 3. Copy upload token

# Add to GitHub:
# Name: CODECOV_TOKEN
# Value: <your-codecov-token>
```

## Environment Variables in Workflow

These are configured in the workflow file `.github/workflows/ci-cd.yml`:

```yaml
env:
  REGISTRY: ghcr.io
  BACKEND_IMAGE: ${{ github.repository }}/backend
  FRONTEND_IMAGE: ${{ github.repository }}/frontend
```

No changes needed unless you want to use a different registry.

## Testing Secrets

### Test Kubernetes Connection

```bash
# Decode and test kubeconfig
echo "$KUBE_CONFIG_PRODUCTION" | base64 -d > /tmp/kubeconfig
export KUBECONFIG=/tmp/kubeconfig
kubectl get nodes
```

### Test Slack Webhook

```bash
curl -X POST -H 'Content-type: application/json' \
  --data '{"text":"Test message from GitHub Actions"}' \
  YOUR_SLACK_WEBHOOK_URL
```

### Test Discord Webhook

```bash
curl -X POST -H 'Content-Type: application/json' \
  --data '{"content":"Test message from GitHub Actions"}' \
  YOUR_DISCORD_WEBHOOK
```

## Security Best Practices

1. **Never commit secrets** to version control
2. **Use environment-specific secrets** for staging/production
3. **Rotate secrets regularly** (every 90 days)
4. **Limit secret access** to necessary workflows only
5. **Use GitHub Environments** for additional protection
6. **Enable audit logs** for secret access

## GitHub Environments Setup

For better security, create environments:

```bash
# Repository → Settings → Environments → New environment

# Create "staging" environment:
- Name: staging
- Required reviewers: (optional)
- Deployment branches: develop

# Create "production" environment:
- Name: production
- Required reviewers: ✓ (recommended)
- Deployment branches: main
- Wait timer: 5 minutes (optional)
```

Add environment-specific secrets:
- `KUBE_CONFIG_STAGING` → staging environment
- `KUBE_CONFIG_PRODUCTION` → production environment

## Troubleshooting

### Secret not found error

```bash
# Check secret exists:
# Repository → Settings → Secrets → Actions

# Verify secret name matches workflow exactly
```

### Base64 decode error

```bash
# Test decoding locally
echo "YOUR_BASE64_STRING" | base64 -d

# If error, re-encode:
cat file | base64 -w 0  # Linux
cat file | base64      # macOS
```

### Kubernetes connection failed

```bash
# Verify kubeconfig is valid
kubectl config view --kubeconfig=/path/to/config

# Check server URL is accessible
curl -k https://your-k3s-server:6443
```

## Complete Setup Checklist

- [ ] `GITHUB_TOKEN` (automatic)
- [ ] `KUBE_CONFIG_STAGING`
- [ ] `KUBE_CONFIG_PRODUCTION`
- [ ] `SLACK_WEBHOOK_URL`
- [ ] `DISCORD_WEBHOOK`
- [ ] `SNYK_TOKEN`
- [ ] `CODECOV_TOKEN` (optional)
- [ ] GitHub Environments configured
- [ ] Test all webhooks
- [ ] Test Kubernetes connection
- [ ] Run workflow to verify

## Next Steps

After configuring secrets:

1. **Push to develop** - Test staging deployment
2. **Create PR to main** - Test build and security scans
3. **Merge to main** - Deploy to production
4. **Verify notifications** - Check Slack/Discord

## Support

If you encounter issues:
- Check workflow logs in Actions tab
- Verify secret names match exactly
- Test secrets manually before adding to GitHub
- Contact DevOps team for help

---

**Remember:** Keep secrets secure and never share them publicly!
