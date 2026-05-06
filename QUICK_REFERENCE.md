# Quick Reference - Enable Jenkins Status Checks

## Essential Steps

### 1️⃣ Install Jenkins Plugins
```
Manage Jenkins → Manage Plugins → Available
- GitHub Plugin
- GitHub Branch Source Plugin  
- Pipeline Plugin
- Git Plugin
```

### 2️⃣ Create GitHub Token
```
GitHub → Settings → Developer settings → Personal access tokens
Scopes: repo, admin:repo_hook
Save token: ghp_xxxxxxxxxxxxxxxxxxxx
```

### 3️⃣ Add Credentials to Jenkins
```
Manage Jenkins → Manage Credentials → Global → Add Credentials
Kind: Secret text
Secret: [Your GitHub Token]
ID: github-token
```

### 4️⃣ Configure GitHub Server
```
Manage Jenkins → Configure System → GitHub
Add GitHub Server:
- Name: GitHub
- Credentials: github-token
- Manage hooks: ✅
Test connection ✅
```

### 5️⃣ Add Webhook in GitHub
```
Repository → Settings → Webhooks → Add webhook
Payload URL: http://172.30.47.147:8090/github-webhook/
Content type: application/json
Events: Pull requests, Pushes
```

### 6️⃣ Create Multibranch Pipeline
```
New Item → Multibranch Pipeline
Branch Sources → GitHub:
- Credentials: github-token
- Repository: https://github.com/pavan-msys/Sample-Jenkins-GitHub-integration
- Discover branches ✅
- Discover pull requests ✅
Build Configuration: Jenkinsfile
```

### 7️⃣ Test with PR
```bash
git checkout -b test-branch
echo "test" >> README.md
git add .
git commit -m "Test Jenkins"
git push origin test-branch
# Create PR on GitHub
```

## URLs

- **Jenkins**: http://172.30.47.147:8090/
- **Repository**: https://github.com/pavan-msys/Sample-Jenkins-GitHub-integration
- **Webhook URL**: http://172.30.47.147:8090/github-webhook/

## Status Checks Expected

✅ `continuous-integration/jenkins/branch`
✅ `continuous-integration/jenkins/pr-merge`

## Troubleshooting

| Issue | Solution |
|-------|----------|
| No status checks | Check webhook deliveries in GitHub |
| Jenkins not triggered | Verify webhook URL and credentials |
| Build fails | Check Jenkinsfile syntax |
| Private IP issue | Use ngrok or public IP |

## ⚠️ Important Note

The IP `172.30.47.147` is private. GitHub.com cannot reach it directly.

**Solutions**:
1. Use ngrok: `ngrok http 8090`
2. Deploy Jenkins on public server
3. Use GitHub Enterprise on same network
